import json

import redis


REDIS_HOST = "localhost"
REDIS_PORT = 6379


client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)


def save_incident(incident_id, state):
    key = f"incident:{incident_id}"

    client.set(
        key,
        json.dumps(state),
    )


def get_incident(incident_id):
    key = f"incident:{incident_id}"

    data = client.get(key)

    if data is None:
        return None

    return json.loads(data)


def update_incident(incident_id, updates):
    current = get_incident(incident_id) or {}

    current.update(updates)

    save_incident(
        incident_id,
        current,
    )

    return current

def list_incidents():
    incidents = []

    for key in client.scan_iter(match="incident:*"):
        data = client.get(key)

        if data is not None:
            incidents.append(json.loads(data))

    return incidents