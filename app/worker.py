import json

from kafka import KafkaConsumer

from app.state_store import save_incident


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

    state = {
        "run_id": run_id,
        "job_id": event["job_id"],
        "job_name": event["job_name"],
        "status": "DETECTED",
        "conclusion": event["conclusion"],
        "failed_step": event["failed_step"],
        "commit_sha": event["commit_sha"],
    }

    save_incident(
        run_id,
        state,
    )

    print(
        f"Incident {run_id} stored in Redis."
    )