import time

from app.github_client import github_get


OWNER = "pruthviraj-m"
REPO = "ci-cd-intelligence-agent"


def get_latest_run(branch):
    url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPO}/actions/runs"
    )

    data = github_get(
        url,
        params={
            "branch": branch,
            "per_page": 1,
        },
    )

    runs = data.get("workflow_runs", [])

    if not runs:
        return None

    return runs[0]


def wait_for_ci(branch, timeout=120, interval=5):

    start = time.time()

    while time.time() - start < timeout:

        run = get_latest_run(branch)

        if run is None:
            print("No workflow run found yet.")
            time.sleep(interval)
            continue

        print(
            f"CI status: {run['status']} | "
            f"Conclusion: {run['conclusion']}"
        )

        if run["status"] == "completed":
            return run

        time.sleep(interval)

    raise TimeoutError(
        "Timed out waiting for GitHub Actions."
    )