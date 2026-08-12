from app.incident_collector import find_latest_failed_run
from app.remediation import run_remediation


# Find the latest failed GitHub Actions run.
failed_run = find_latest_failed_run()

run_id = failed_run["id"]
branch = failed_run["head_branch"]

print("Latest failed run:", run_id)
print("Branch:", branch)


# Run the complete remediation workflow.
result = run_remediation(
    run_id,
    branch,
)


print("\n========== REMEDIATION COMPLETE ==========")
print("Run ID:", result["run_id"])
print("PR:", result["pr_url"])
print("CI:", result["ci_status"])
print("Status:", result["status"])