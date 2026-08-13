import sys
from pathlib import Path
from datetime import datetime, timezone

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.state_store import list_incidents, save_incident


st.set_page_config(
    page_title="CI/CD Intelligence Agent",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 CI/CD Intelligence Agent")
st.caption("AI-powered CI failure diagnosis and remediation")


# ============================================================
# DEMO CONTROLS
# ============================================================

st.subheader("Demo & Testing")

col1, col2 = st.columns([2, 1])

with col1:
    if st.button(
        "🚨 Trigger Test Incident",
        use_container_width=True,
    ):
        demo_run_id = f"DEMO-{int(datetime.now().timestamp())}"

        demo_incident = {
            "run_id": demo_run_id,
            "job_id": "demo-job-001",
            "job_name": "test",
            "status": "CI_PASSED",
            "conclusion": "failure",
            "ci_status": "success",
            "failed_step": "Run tests",
            "commit_sha": "3684044cfb70ab1470e1a99c8bda5805c7ecec91",
            "branch": "remediation/demo",
            "pr_number": 3,
            "pr_url": "https://github.com/pruthviraj-m/ci-cd-intelligence-agent/pull/3",
            "failure_reason": (
                "Intentional syntax error prevented the test suite "
                "from importing the application module."
            ),
            "root_cause": (
                "An intentional syntax error was introduced into "
                "app/calculator.py."
            ),
            "suggested_fix": (
                "Remove the invalid syntax line from app/calculator.py."
            ),
            "risk_level": "low",
            "confidence": 100.0,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "demo": True,
        }

        save_incident(demo_run_id, demo_incident)

        st.success("Test incident created successfully.")
        st.rerun()

with col2:
    if st.button(
        "🔄 Refresh",
        use_container_width=True,
    ):
        st.rerun()


st.divider()


# ============================================================
# INCIDENT DATA
# ============================================================

incidents = list_incidents()

if not incidents:
    st.info("No CI incidents recorded yet.")
    st.stop()

latest = incidents[0]


# ============================================================
# LATEST INCIDENT SUMMARY
# ============================================================

st.subheader("Latest Incident")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Run ID",
        latest.get("run_id", "N/A"),
    )

with col2:
    st.metric(
        "Status",
        latest.get("status", "UNKNOWN"),
    )

with col3:
    st.metric(
        "CI",
        latest.get("ci_status", "N/A"),
    )

with col4:
    pr_number = latest.get("pr_number", "N/A")
    st.metric(
        "Pull Request",
        f"#{pr_number}" if pr_number != "N/A" else "N/A",
    )


# ============================================================
# PIPELINE
# ============================================================

st.divider()

st.subheader("Remediation Pipeline")

pipeline = [
    ("1", "Incident Detected"),
    ("2", "AI Diagnosis"),
    ("3", "Patch Generated"),
    ("4", "Tests Passed"),
    ("5", "Pull Request Created"),
    ("6", "CI Verified"),
]

cols = st.columns(len(pipeline))

for col, (number, label) in zip(cols, pipeline):
    with col:
        st.success(f"✓ {number}. {label}")


# ============================================================
# INCIDENT + AI REMEDIATION
# ============================================================

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Incident")

    st.write(
        "**Branch:**",
        latest.get("branch", "N/A"),
    )

    st.write(
        "**Job:**",
        latest.get("job_name", "N/A"),
    )

    st.write(
        "**Failed step:**",
        latest.get("failed_step", "N/A"),
    )

    st.write(
        "**Commit:**",
        latest.get("commit_sha", "N/A"),
    )

    st.write(
        "**Conclusion:**",
        latest.get("conclusion", "N/A"),
    )


with right:
    st.subheader("AI Remediation")

    if latest.get("root_cause"):
        st.write("**Root Cause**")
        st.info(latest["root_cause"])

    if latest.get("suggested_fix"):
        st.write("**Suggested Fix**")
        st.success(latest["suggested_fix"])

    col_a, col_b = st.columns(2)

    with col_a:
        st.metric(
            "Risk",
            latest.get("risk_level", "N/A"),
        )

    with col_b:
        confidence = latest.get("confidence")

        if confidence is not None:
            st.metric(
                "Confidence",
                f"{float(confidence):.1f}%",
            )


# ============================================================
# PULL REQUEST
# ============================================================

if latest.get("pr_url"):
    st.divider()

    st.subheader("Pull Request")

    st.write(
        f"AI-generated remediation PR #{latest.get('pr_number', 'N/A')}"
    )

    st.link_button(
        "Open Pull Request →",
        latest["pr_url"],
    )


# ============================================================
# INCIDENT HISTORY
# ============================================================

st.divider()

st.subheader("Incident History")

for incident in incidents:
    run_id = incident.get("run_id", "N/A")
    status = incident.get("status", "UNKNOWN")

    with st.expander(
        f"Run {run_id} — {status}"
    ):
        st.json(incident)