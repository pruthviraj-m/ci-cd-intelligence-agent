import json

from kafka import KafkaProducer


KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
INCIDENT_TOPIC = "ci-incidents"


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)


def publish_incident(incident, branch):
    event = {
        "run_id": incident.run_id,
        "job_id": incident.job_id,
        "job_name": incident.job_name,
        "conclusion": incident.conclusion,
        "failed_step": incident.failed_step,
        "commit_sha": incident.commit_sha,
        "branch": branch,
    }

    producer.send(
        INCIDENT_TOPIC,
        value=event,
    )

    producer.flush()

    return event