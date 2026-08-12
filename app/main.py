from app.incident_collector import get_failed_incident


RUN_ID = 31593832847


incident = get_failed_incident(RUN_ID)

print("\n========== CHANGED FILES ==========")

for file in incident.changed_files:
    print(
        f"{file['filename']} | "
        f"{file['status']} | "
        f"+{file['additions']} "
        f"-{file['deletions']}"
    )

print("\n========== DIFF ==========")
print(incident.diff)

print("========== CI INCIDENT ==========")
print("Run ID:", incident.run_id)
print("Job ID:", incident.job_id)
print("Job:", incident.job_name)
print("Conclusion:", incident.conclusion)
print("Failed step:", incident.failed_step)

print("Commit SHA:", incident.commit_sha)
print("Commit message:", incident.commit_message)
print("Author:", incident.author)

print("\n========== LOGS ==========")
print(incident.logs)