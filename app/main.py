from app.incident_collector import (
    find_latest_failed_run,
    get_failed_incident,
)
from app.event_bus import publish_incident


# ============================================================
# FIND LATEST FAILED CI RUN
# ============================================================

failed_run = find_latest_failed_run()

run_id = failed_run["id"]
branch = failed_run["head_branch"]

print("Latest failed run:", run_id)
print("Branch:", branch)


# ============================================================
# COLLECT INCIDENT
# ============================================================

incident = get_failed_incident(run_id)


# ============================================================
# PUBLISH INCIDENT TO KAFKA
# ============================================================

event = publish_incident(
    incident,
    branch,
)

print("\n========== INCIDENT PUBLISHED ==========")
print("Kafka topic: ci-incidents")
print("Run ID:", event["run_id"])
print("Branch:", event["branch"])

print("\nWorker will now handle remediation.")