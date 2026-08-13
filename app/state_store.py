import json
import os
from datetime import datetime, timezone

import redis


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

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

    current["updated_at"] = datetime.now(
        timezone.utc
    ).isoformat()

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

    incidents.sort(
        key=lambda incident: incident.get(
            "updated_at",
            "",
        ),
        reverse=True,
    )

    return incidents


# ============================================================
# HINDSIGHT MEMORY
# ============================================================

def recall_similar_incidents(current_incident, limit=3):
    """
    Recall previous incidents that share meaningful
    failure characteristics with the current incident.
    """

    # Support both CIIncident objects and demo dictionaries.
    if isinstance(current_incident, dict):
        current_run_id = current_incident.get(
            "run_id",
            "",
        )
        current_failed_step = current_incident.get(
            "failed_step",
            "",
        )
        current_logs = current_incident.get(
            "logs",
            "",
        )
        current_diff = current_incident.get(
            "diff",
            "",
        )
    else:
        current_run_id = getattr(
            current_incident,
            "run_id",
            "",
        )
        current_failed_step = getattr(
            current_incident,
            "failed_step",
            "",
        )
        current_logs = getattr(
            current_incident,
            "logs",
            "",
        )
        current_diff = getattr(
            current_incident,
            "diff",
            "",
        )

    current_text = " ".join(
        [
            str(current_failed_step),
            str(current_logs),
            str(current_diff),
        ]
    ).lower()

    current_terms = set(
        word.strip(".,:;()[]{}'\"")
        for word in current_text.split()
        if len(word.strip(".,:;()[]{}'\"")) >= 4
    )

    memories = []

    for incident in list_incidents():

        # Never recall the current incident itself.
        if str(incident.get("run_id")) == str(
            current_run_id
        ):
            continue

        hindsight = incident.get(
            "hindsight",
            {},
        )

        historical_text = " ".join(
            [
                str(incident.get("failed_step", "")),
                str(incident.get("failure_reason", "")),
                str(hindsight.get("root_cause", "")),
                str(hindsight.get("suggested_fix", "")),
            ]
        ).lower()

        historical_terms = set(
            word.strip(".,:;()[]{}'\"")
            for word in historical_text.split()
            if len(word.strip(".,:;()[]{}'\"")) >= 4
        )

        overlap = current_terms.intersection(
            historical_terms
        )

        if not overlap:
            continue

        score = len(overlap)

        memories.append(
            {
                "run_id": incident.get("run_id"),
                "root_cause": hindsight.get(
                    "root_cause",
                    incident.get(
                        "root_cause",
                        "",
                    ),
                ),
                "suggested_fix": hindsight.get(
                    "suggested_fix",
                    incident.get(
                        "suggested_fix",
                        "",
                    ),
                ),
                "status": incident.get(
                    "status",
                    "",
                ),
                "matched_terms": sorted(
                    list(overlap)
                ),
                "similarity_score": score,
            }
        )

    memories.sort(
        key=lambda memory: memory[
            "similarity_score"
        ],
        reverse=True,
    )

    return memories[:limit]


def retain_hindsight(
    incident_id,
    diagnosis,
    outcome,
):
    """
    Store the diagnosis and verified outcome of an
    incident so future incidents can recall it.
    """

    update_incident(
        incident_id,
        {
            "hindsight": {
                "root_cause": diagnosis.root_cause,
                "suggested_fix": diagnosis.suggested_fix,
                "risk_level": diagnosis.risk_level,
                "confidence": diagnosis.confidence,
                "outcome": outcome,
            }
        },
    )