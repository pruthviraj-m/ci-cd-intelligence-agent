import json

from kafka import KafkaConsumer

from app.state_store import save_incident
from app.remediation import run_remediation


KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
INCIDENT_TOPIC = "ci-incidents"


consumer = KafkaConsumer(
    INCIDENT_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    group_id="ci-remediation-worker",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    ),
)


print("CI remediation worker started.")
print("Waiting for incidents...")


for message in consumer:
    event = message.value

    run_id = event["run_id"]
    branch = event.get("branch", "")

    state = {
        "run_id": run_id,
        "job_id": event["job_id"],
        "job_name": event["job_name"],
        "status": "DETECTED",
        "conclusion": event["conclusion"],
        "failed_step": event["failed_step"],
        "commit_sha": event["commit_sha"],
        "branch": branch,
    }

    save_incident(
        run_id,
        state,
    )

    print(
        f"Incident {run_id} detected."
    )

    try:
        result = run_remediation(
            run_id,
            branch,
        )

        print(
            f"Incident {run_id} completed."
        )

        print(
            f"Status: {result['status']}"
        )

    except Exception as error:
        print(
            f"Incident {run_id} failed:"
            f" {error}"
        )