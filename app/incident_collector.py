from app.github_client import github_get
from app.incident import CIIncident


OWNER = "pruthviraj-m"
REPO = "ci-cd-intelligence-agent"


def get_failed_incident(run_id):
    # Get workflow run information
    run_url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPO}/actions/runs/{run_id}"
    )

    run = github_get(run_url)

    # Get jobs
    jobs_url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPO}/actions/runs/{run_id}/jobs"
    )

    data = github_get(jobs_url)

    failed_job = None

    for job in data["jobs"]:
        if job["conclusion"] == "failure":
            failed_job = job
            break

    if failed_job is None:
        raise RuntimeError("No failed job found.")

    # Find failed step
    failed_step = "Unknown"

    for step in failed_job["steps"]:
        if step["conclusion"] == "failure":
            failed_step = step["name"]
            break

    # Get logs
    logs_url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPO}/actions/jobs/"
        f"{failed_job['id']}/logs"
    )

    logs = github_get(logs_url)

    # Get commit
    commit_sha = run["head_sha"]

    commit_url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPO}/commits/{commit_sha}"
    )

    commit = github_get(commit_url)

    changed_files = []

    for file in commit["files"]:
        changed_files.append({
            "filename": file["filename"],
            "status": file["status"],
            "additions": file["additions"],
            "deletions": file["deletions"],
            "changes": file["changes"],
            "patch": file.get("patch", "")
        })

    return CIIncident(
        run_id=run_id,
        job_id=failed_job["id"],
        job_name=failed_job["name"],
        conclusion=failed_job["conclusion"],
        failed_step=failed_step,
        logs=logs,
        commit_sha=commit_sha,
        commit_message=commit["commit"]["message"],
        author=commit["commit"]["author"]["name"],
        changed_files=changed_files,
        diff="\n\n".join(
            f"FILE: {file['filename']}\n{file['patch']}"
            for file in changed_files
        ),
    )


def find_latest_failed_run():
    url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPO}/actions/runs"
    )

    data = github_get(
        url,
        params={
            "per_page": 10
        }
    )

    for run in data["workflow_runs"]:
        if run["conclusion"] == "failure":
            return run

    raise RuntimeError("No failed workflow run found.")