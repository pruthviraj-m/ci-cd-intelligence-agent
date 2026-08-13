import os

from openai import OpenAI

from app.diagnosis import Diagnosis
from app.patch import PatchProposal


NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not NVIDIA_API_KEY:
    raise RuntimeError(
        "NVIDIA_API_KEY environment variable is not set."
    )


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY,
)

MODEL = "z-ai/glm-5.2"


def _generate_structured(model_class, prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.1,
            max_tokens=8192,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": model_class.__name__,
                    "schema": model_class.model_json_schema(),
                },
            },
        )

    except Exception as error:
        raise RuntimeError(
            f"NVIDIA LLM request failed: {error}"
        ) from error

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "NVIDIA LLM returned an empty response."
        )

    return model_class.model_validate_json(content)


def diagnose_incident(incident, hindsight=None):
    hindsight = hindsight or []

    hindsight_context = "No relevant previous incidents found."

    if hindsight:
        hindsight_context = "\n\n".join(
            f"""
Previous incident:
Run: {memory.get("run_id")}
Previous root cause: {memory.get("root_cause")}
Previous fix: {memory.get("suggested_fix")}
Previous outcome: {memory.get("status")}
Similarity evidence: {", ".join(memory.get("matched_terms", []))}
"""
            for memory in hindsight
        )

    prompt = f"""
You are an expert software reliability engineer diagnosing a CI/CD failure.

Analyze ONLY the evidence provided below.

Do not invent files, errors, commits, or causes that are not supported by the evidence.

Determine:

1. What failed?
2. Most likely root cause.
3. Evidence supporting the diagnosis.
4. Affected files.
5. Concrete fix.
6. Confidence.
7. Risk level.

Rules:

- Use ONLY supplied evidence.
- Do not invent files, errors, commits, or code changes.
- Do not list a file unless directly implicated.
- Separate observations from conclusions.
- Evidence must identify its source.
- Confidence must reflect the evidence.
- risk_level must be "low", "medium", or "high".
- If evidence is insufficient, say so.

========== HINDSIGHT MEMORY ==========

The following are previous incidents recalled from
the agent's persistent memory.

Use them only as historical context.
Do not assume the current incident has the same cause.
The current CI logs and diff remain the primary evidence.

{hindsight_context}

========== CI INCIDENT ==========

Repository:
{incident.repository if hasattr(incident, "repository") else "ci-cd-intelligence-agent"}

Run ID:
{incident.run_id}

Job:
{incident.job_name}

Failed step:
{incident.failed_step}

Commit SHA:
{incident.commit_sha}

Commit message:
{incident.commit_message}

Author:
{incident.author}

========== LOGS ==========

{incident.logs}

========== CHANGED FILES / DIFF ==========

{incident.diff}

========== END EVIDENCE ==========

Return a structured diagnosis based strictly on this evidence.
"""

    return _generate_structured(
        Diagnosis,
        prompt,
    )


def generate_patch(incident, diagnosis):

    prompt = f"""
You are an expert software engineer fixing a CI/CD failure.

Generate the smallest possible code change that fixes the diagnosed problem.

IMPORTANT RULES:

- Only modify files directly supported by the evidence.
- Make the smallest change necessary.
- Do not rewrite unrelated code.
- Do not modify tests unless explicitly justified.
- old_text MUST exactly match text in the current file.
- Do not invent file paths.
- Do not add unnecessary dependencies.

========== DIAGNOSIS ==========

Root cause:
{diagnosis.root_cause}

Suggested fix:
{diagnosis.suggested_fix}

========== CHANGED FILES ==========

{incident.diff}

========== END EVIDENCE ==========

Return the minimal patch proposal.
"""

    return _generate_structured(
        PatchProposal,
        prompt,
    )