# Giving Our CI Agent a Memory: What Changed When It Stopped Diagnosing Every Failure From Scratch

The first version of our CI/CD Intelligence Agent was smart in the moment and forgetful the second the moment passed. It could look at a failing pipeline, read the logs, read the diff, and hand back a reasonable root cause. Then it would do the exact same investigative work again the next time a nearly identical failure showed up, because it had no way of knowing it had ever seen anything like it before. That gap — an agent that reasons well but remembers nothing — is what pushed us to bolt on Hindsight, and it ended up being the most interesting part of the project.

## What the system actually does

The agent sits in the path between a CI failure and a fix. A Kafka event tells our worker that a pipeline run failed. The worker pulls the failure into Redis as an incident record and walks it through a defined lifecycle: `DETECTED → COLLECTING → DIAGNOSING → GENERATING_PATCH → APPLYING_PATCH → VALIDATING_PATCH → PATCH_VALIDATED → CREATING_PR → PR_CREATED → CI_VERIFYING → CI_PASSED`. Somewhere in the middle of that pipeline, an LLM looks at the failed step, the CI logs, and the code diff, and produces a structured diagnosis: root cause, evidence, affected files, a suggested fix, a confidence score, and a risk level. If the fix passes local tests and a real CI run on GitHub, the loop closes and a PR goes up.

None of that requires memory. You could ship that system exactly as I described it and it would work. What it wouldn't do is get any *better* over time, and that's the problem Hindsight solves.

## The core technical story: memory as a first-class part of diagnosis, not an afterthought

The easy way to bolt memory onto a system like this is to log everything to a database and call it a day. We didn't want that. We wanted the agent's past diagnoses to actually influence its current reasoning, and we wanted that influence to be visible and explainable, not a black box embedding lookup that occasionally does something useful.

That's what [Hindsight](https://github.com/vectorize-io/hindsight) gives you: a memory layer built specifically for agents, with an explicit retain/recall contract instead of "throw it in a vector store and hope." Reading through the [Hindsight docs](https://hindsight.vectorize.io/) early on, the framing that stuck with us was treating memory as part of the agent's reasoning loop rather than a logging side-effect — store what happened, recall what's relevant, and hand the recalled context to the model *before* it reasons, not after.

Our implementation lives across four files, and the flow through them is the whole story:

```
CI Failure
   ↓
Collect Incident
   ↓
Recall Similar Incidents   (state_store.py)
   ↓
AI Diagnosis                (llm_client.py, informed by recalled memory)
   ↓
Remediation → Verified CI Pass
   ↓
Retain Hindsight            (state_store.py, closing the loop)
```

`app/state_store.py` is where the memory lives. Redis backs it as persistent incident storage, and a handful of functions do the real work: `save_incident()` and `get_incident()` for basic state, `update_incident()` to move a record through its lifecycle, and two functions that matter more for the memory story than anything else — `recall_similar_incidents()` and `retain_hindsight()`.

## How memory is recalled

Before the LLM ever sees a new failure, we ask Hindsight what it remembers about anything similar.

```python
# app/remediation.py
similar_incidents = recall_similar_incidents(incident, limit=3)

diagnosis = diagnose_incident(
    incident,
    hindsight=similar_incidents,
)
```

`recall_similar_incidents()` extracts meaningful terms from the failed step, the CI logs, the code diff, and — crucially — the *previous* failure reasons, root causes, and suggested fixes stored on past incidents. It scores overlap between the current failure and everything sitting in Redis, and returns the top matches, capped at three. This is deliberately simple: it's overlapping-term similarity, not a fine-tuned embedding model, and I think that's the right call for a v1. It's inspectable. When it recalls the wrong incident, you can look at the matched terms and immediately see why, instead of debugging a vector index.

Each recalled incident carries forward the previous run ID, previous root cause, previous fix, previous verified outcome, and the specific evidence that made it match. That's the payload that reaches the model.

## How memory is retained

Retention doesn't happen on every diagnosis — only on a *verified* one. That distinction matters more than it looks like on paper.

```python
# app/remediation.py, after GitHub CI verification succeeds
retain_hindsight(
    run_id,
    diagnosis,
    outcome="CI_PASSED",
)
```

We only write a diagnosis into long-term memory once the proposed fix has passed local tests *and* a real CI run on GitHub. An unverified guess never becomes precedent. This was a conscious design decision after we thought about what happens if you retain everything: a wrong diagnosis gets stored, later gets recalled as "similar past experience," and the agent talks itself into repeating the same mistake with borrowed confidence. Gating retention on `CI_PASSED` means every memory in the system has already been proven correct once. The worker's lifecycle states exist specifically so we can make that distinction — an incident that was merely diagnosed and one whose remediation was actually verified are not the same thing, and only the second one gets to become a memory.

What gets retained isn't raw log text either. `app/diagnosis.py` defines a structured `Diagnosis` model — root cause, evidence, affected files, suggested fix, confidence, risk level — and that's what `retain_hindsight()` stores. Structured memory instead of a text blob means recall doesn't need to re-parse anything; it can hand the model a clean previous root cause and previous fix directly.

## How recalled memory reaches the model

The part I was most worried about getting wrong was prompt design. It's easy to hand an LLM "here's what happened last time" and have it just default to the old answer even when the current evidence doesn't support it. So the prompt in `app/llm_client.py` is explicit about the hierarchy: analyze the current incident's evidence first, and treat historical incidents as *additional* context, not a substitute for looking at what's actually in front of it.

```python
# app/llm_client.py
def diagnose_incident(incident, hindsight=None):
    # current CI evidence: failed step, logs, diff
    # + hindsight: prior root causes, fixes, verified outcomes
    # prompt instructs the model to reason from current evidence
    # and use hindsight only as supporting context, not as ground truth
    ...
```

Current evidence plus historical incident evidence goes into the model, and a current diagnosis comes out. The distinction we kept enforcing in the prompt — don't invent causes the current evidence doesn't support — is what keeps memory from turning into confirmation bias.

## What you actually see happen

The dashboard makes this loop visible instead of invisible, which turned out to matter for trust as much as for debugging. When a new failure comes in, the Hindsight panel shows something like:

```
HINDSIGHT MEMORY
Recalled 3 similar previous incidents

Previous Run #2291
Root cause: syntax error introduced in test fixture

Matched: error, syntax, test, tests
Similarity: 5
```

That's a small thing, but it changes how the tool feels to use. Instead of an agent that confidently states a root cause with no visible reasoning, you get an agent that shows you *why* it's confident: it's seen this pattern before, here's the run ID, here's what fixed it, here's the term overlap that triggered the match. If the recall was garbage, you know immediately, because the matched terms will look wrong.

## What changes with memory versus without it

Without Hindsight, every CI failure is an isolated investigation. A flaky dependency version bump that broke the build three weeks ago and a nearly identical one today get diagnosed independently, at full cost, with no guarantee the agent converges on the same (correct) answer twice.

With Hindsight, the second occurrence starts from a head start: three candidate precedents, their verified fixes, and a similarity score explaining the match — all before the model does a single token of fresh reasoning. The agent still has to confirm the current evidence supports the same conclusion, but it's not starting from zero.

The honest caveat here is that we're bound by simple term-overlap similarity right now, which means recall quality depends heavily on how distinctive the failure signatures are. Two unrelated failures that happen to share common CI vocabulary — "error," "failed," "test" — can produce noisy matches if a distinguishing term isn't present. It's the kind of limitation you accept in exchange for a system you can actually reason about, and it's a natural place to grow toward embedding-based similarity without giving up the explainability that made this useful in the first place. There's a good breakdown of that broader design space in Vectorize's writeup on [what agent memory actually is](https://vectorize.io/what-is-agent-memory) and why retain/recall as an explicit contract beats implicit context stuffing.

## Lessons learned

**Gate retention on verification, not on generation.** An agent that remembers its guesses as confidently as its proven fixes will compound its own mistakes. Only write to memory once an external system — CI, in our case — has confirmed the outcome.

**Structured memory beats text-blob memory.** Storing a typed diagnosis object instead of raw logs means recall doesn't need a second reasoning pass just to figure out what a memory *means*. It also makes memories directly renderable in a UI, which we didn't originally plan for but ended up relying on.

**Tell the model explicitly how to weigh memory against current evidence.** Recall is only safe if the prompt treats history as supporting context, not as the answer key. Skipping this is the fastest way to get an agent that pattern-matches to the past instead of actually diagnosing the present.

**Simple similarity is a legitimate starting point.** Term overlap isn't glamorous, but it's debuggable in a way that a raw vector similarity score isn't. If a match looks wrong, you can see exactly why, which matters a lot more than incremental recall accuracy when you're still building trust in the system.

**Make memory visible, not just functional.** The dashboard's Hindsight panel didn't change the agent's behavior at all, but it changed how much we — and anyone watching a demo of the tool — trusted its output. An invisible memory system is indistinguishable from no memory system as far as the user is concerned.

The bigger takeaway, for us, was less about CI specifically and more about agent design in general: an agent that reasons well but forgets everything is only ever as good as its worst day. Retain/recall, backed by verified outcomes, is what turns a one-shot diagnostic tool into something that actually improves the more it runs.
