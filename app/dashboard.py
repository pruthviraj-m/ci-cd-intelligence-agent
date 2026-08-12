import streamlit as st

from state_store import list_incidents


st.set_page_config(
    page_title="CI/CD Intelligence Agent",
    page_icon="🤖",
    layout="wide",
)


st.title("🤖 CI/CD Intelligence Agent")
st.caption("AI-powered CI failure diagnosis and remediation")


incidents = list_incidents()

if not incidents:
    st.info("No CI incidents recorded yet.")
    st.stop()


incidents = sorted(
    incidents,
    key=lambda incident: incident.get("run_id", 0),
    reverse=True,
)


latest = incidents[0]


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
    st.metric(
        "PR",
        latest.get("pr_number", "N/A"),
    )


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


with right:
    st.subheader("Remediation")

    st.write(
        "**Status:**",
        latest.get("status", "N/A"),
    )

    if latest.get("pr_url"):
        st.link_button(
            "Open Pull Request",
            latest["pr_url"],
        )

    st.write(
        "**CI status:**",
        latest.get("ci_status", "N/A"),
    )


st.divider()

st.subheader("Incident History")

for incident in incidents:
    with st.expander(
        f"Run {incident.get('run_id')} — "
        f"{incident.get('status', 'UNKNOWN')}"
    ):
        st.json(incident)


if st.button("Refresh"):
    st.rerun()