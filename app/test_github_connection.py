from app.github_client import github_get


OWNER = "pruthviraj-m"
REPO = "ci-cd-intelligence-agent"

JOB_ID = 94104594262

url = (
    f"https://api.github.com/repos/"
    f"{OWNER}/{REPO}/actions/jobs/{JOB_ID}/logs"
)

logs = github_get(url)

print(logs)