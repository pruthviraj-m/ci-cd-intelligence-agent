from google import genai

from app.diagnosis import Diagnosis
from app.patch import PatchProposal


client = genai.Client()

MODEL = "gemini-3.6-flash"


def diagnose_incident(incident):

    prompt = f"""
You are an expert software reliability engineer diagnosing a CI/CD failure.

Analyze ONLY the evidence provided below.

Do not invent files, errors, commits, or causes that are not supported by the evidence.

Your task is to determine:
1. What failed?
2. What is the most likely root cause?
3. What evidence proves or strongly supports the diagnosis?
4. Which files are affected?
5. What concrete fix should be applied?
6. How confident are you?
7. What is the risk level of applying the suggested fix?

Rules:

- Use ONLY the supplied evidence.
- Do not invent files, errors, commits, or code changes.
- Do not list a file as affected unless the evidence directly implicates it.
- Separate factual observations from conclusions.
- Evidence must identify its source.
- Confidence must reflect the strength of the available evidence.
- Use "low", "medium", or "high" for risk_level.
- If evidence is insufficient, say so instead of guessing.

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

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Diagnosis,
        },
    )

    return Diagnosis.model_validate_json(response.text)
def generate_patch(incident, diagnosis):

    prompt = f"""
You are an expert software engineer fixing a CI/CD failure.

You have already received a diagnosis.

Generate the smallest possible code change that fixes the diagnosed
problem.

IMPORTANT RULES:

- Only modify files directly supported by the evidence.
- Make the smallest change necessary.
- Do not rewrite unrelated code.
- Do not modify tests unless the diagnosis explicitly proves the test is wrong.
- The old_text MUST exactly match text that exists in the current file.
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

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": PatchProposal,
        },
    )

    return PatchProposal.model_validate_json(response.text)