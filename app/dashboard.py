# import sys
# from pathlib import Path
# from datetime import datetime, timezone
# from time import sleep
# from html import escape

# import streamlit as st

# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# if str(PROJECT_ROOT) not in sys.path:
#     sys.path.insert(0, str(PROJECT_ROOT))

# from app.state_store import (
#     list_incidents,
#     save_incident,
#     recall_similar_incidents,
# )


# # ============================================================
# # PAGE CONFIG
# # ============================================================

# st.set_page_config(
#     page_title="CI/CD Intelligence Agent",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )


# # ============================================================
# # VISUAL SYSTEM
# # ============================================================

# st.markdown(
#     """
#     <style>
#     :root {
#         --bg: #05070a;
#         --panel: #0b0f14;
#         --panel2: #0e141b;
#         --border: #1b2631;
#         --text: #f4f7f9;
#         --muted: #778491;
#         --green: #39e27d;
#         --green-dim: #0a2417;
#         --red: #ff5c68;
#         --red-dim: #2a1015;
#         --blue: #4da3ff;
#         --blue-dim: #0b1c2d;
#         --purple: #c084fc;
#         --amber: #f6c453;
#     }

#     .stApp {
#         background: var(--bg);
#         color: var(--text);
#     }

#     [data-testid="stHeader"] {
#         background: rgba(5, 7, 10, .94);
#     }

#     [data-testid="stSidebar"] {
#         background: #070a0e;
#         border-right: 1px solid var(--border);
#     }

#     [data-testid="stSidebar"] > div:first-child {
#         padding-top: 1.1rem;
#     }

#     .block-container {
#         max-width: 1500px;
#         padding-top: 1.2rem;
#         padding-bottom: 2.8rem;
#     }

#     /* ---------- Typography ---------- */

#     .eyebrow {
#         color: #9aa7b3;
#         font-size: .68rem;
#         font-weight: 850;
#         letter-spacing: .14em;
#         text-transform: uppercase;
#         margin-bottom: .42rem;
#     }

#     .hero-title {
#         font-size: 2.25rem;
#         line-height: 1;
#         font-weight: 900;
#         letter-spacing: -.05em;
#         margin: 0;
#     }

#     .hero-sub {
#         color: var(--muted);
#         margin-top: .45rem;
#         font-size: .92rem;
#     }

#     .section-title {
#         color: #dce3e8;
#         font-size: .68rem;
#         font-weight: 850;
#         letter-spacing: .12em;
#         text-transform: uppercase;
#         margin: 0 0 .75rem;
#     }

#     /* ---------- Sidebar ---------- */

#     .brand {
#         padding: .4rem 0 1.25rem;
#         border-bottom: 1px solid var(--border);
#         margin-bottom: 1.15rem;
#     }

#     .brand-title {
#         font-size: 1.08rem;
#         font-weight: 850;
#         color: white;
#     }

#     .brand-sub {
#         color: var(--muted);
#         font-size: .76rem;
#         margin-top: .18rem;
#         line-height: 1.45;
#     }

#     .side-nav {
#         color: #e6ebef;
#         font-size: .88rem;
#         line-height: 2.9;
#     }

#     .side-nav .active {
#         color: white;
#         font-weight: 800;
#     }

#     .side-copy {
#         color: #8995a1;
#         font-size: .76rem;
#         line-height: 1.55;
#     }

#     .side-status {
#         color: #8995a1;
#         font-size: .74rem;
#         line-height: 1.9;
#     }

#     .side-status .ok {
#         color: var(--green);
#     }

#     .live {
#         display: inline-flex;
#         align-items: center;
#         gap: .45rem;
#         border: 1px solid #19482d;
#         background: #09150f;
#         color: var(--green);
#         padding: .38rem .65rem;
#         border-radius: 999px;
#         font-size: .68rem;
#         font-weight: 850;
#         letter-spacing: .06em;
#         text-transform: uppercase;
#     }

#     .dot {
#         width: 7px;
#         height: 7px;
#         border-radius: 50%;
#         display: inline-block;
#         background: var(--green);
#         box-shadow: 0 0 10px rgba(57,226,125,.7);
#     }

#     /* ---------- Panels ---------- */

#     .panel {
#         background: linear-gradient(180deg, #0b1016 0%, #090d12 100%);
#         border: 1px solid var(--border);
#         border-radius: 12px;
#         padding: 1rem 1.05rem;
#     }

#     .panel-tight {
#         padding: .82rem .9rem;
#     }

#     .spacer {
#         height: .9rem;
#     }

#     /* ---------- Pipeline ---------- */

#     .pipeline {
#         display: flex;
#         align-items: stretch;
#         gap: .32rem;
#     }

#     .stage {
#         flex: 1;
#         min-width: 0;
#         border: 1px solid #26323e;
#         background: #0a0f15;
#         border-radius: 10px;
#         padding: .72rem .5rem;
#         text-align: center;
#         transition: all .2s ease;
#     }

#     .stage.waiting {
#         opacity: .48;
#     }

#     .stage.active {
#         border-color: #4b8fd2;
#         background: #0c1927;
#         box-shadow: 0 0 0 1px rgba(77,163,255,.15), 0 0 24px rgba(77,163,255,.08);
#     }

#     .stage.failed {
#         border-color: #71303a;
#         background: #160b0f;
#     }

#     .stage.done {
#         border-color: #1d6740;
#         background: #091b12;
#     }

#     .stage-icon {
#         font-size: 1.12rem;
#         margin-bottom: .25rem;
#     }

#     .stage-name {
#         font-size: .69rem;
#         font-weight: 900;
#         color: #eef2f4;
#     }

#     .stage-desc {
#         color: #74808c;
#         font-size: .61rem;
#         line-height: 1.35;
#         margin-top: .25rem;
#         min-height: 2.05em;
#     }

#     .stage-state {
#         font-size: .59rem;
#         font-weight: 850;
#         margin-top: .45rem;
#         color: #687580;
#     }

#     .stage.done .stage-state {
#         color: var(--green);
#     }

#     .stage.active .stage-state {
#         color: #72baff;
#     }

#     .stage.failed .stage-state {
#         color: #ff7882;
#     }

#     .connector {
#         width: 14px;
#         align-self: center;
#         border-top: 1px dashed #33404c;
#         opacity: .8;
#     }

#     .connector.done {
#         border-color: #2c7650;
#     }

#     .status-banner {
#         border: 1px solid #1d6c40;
#         background: linear-gradient(90deg, #082017, #0b2518);
#         color: var(--green);
#         border-radius: 10px;
#         padding: .75rem 1rem;
#         text-align: center;
#         font-weight: 900;
#         font-size: .9rem;
#     }

#     .status-banner.active {
#         border-color: #315c86;
#         background: linear-gradient(90deg, #0a1622, #0b1b2a);
#         color: #71baff;
#     }

#     .status-banner.failed {
#         border-color: #6b2932;
#         background: linear-gradient(90deg, #210d12, #180b0e);
#         color: #ff7580;
#     }

#     .status-banner span {
#         display: block;
#         color: #74818c;
#         font-size: .69rem;
#         font-weight: 500;
#         margin-top: .2rem;
#     }

#     /* ---------- Incident ---------- */

#     .incident-id {
#         font-size: 1.38rem;
#         font-weight: 900;
#         letter-spacing: -.035em;
#         word-break: break-word;
#     }

#     .meta {
#         color: var(--muted);
#         font-size: .78rem;
#         margin-top: .25rem;
#     }

#     .kv {
#         display: grid;
#         grid-template-columns: 74px 1fr;
#         gap: .42rem .7rem;
#         font-size: .76rem;
#     }

#     .kv .k {
#         color: #66727e;
#     }

#     .kv .v {
#         color: #dfe4e8;
#         word-break: break-word;
#     }

#     .badge {
#         display: inline-block;
#         padding: .26rem .52rem;
#         border-radius: 999px;
#         font-size: .62rem;
#         font-weight: 900;
#         letter-spacing: .04em;
#     }

#     .badge-green {
#         background: #0c2a1b;
#         border: 1px solid #1b6840;
#         color: var(--green);
#     }

#     .badge-red {
#         background: var(--red-dim);
#         border: 1px solid #6d2830;
#         color: #ff7a7a;
#     }

#     .badge-amber {
#         background: #241b09;
#         border: 1px solid #5d4719;
#         color: var(--amber);
#     }

#     /* ---------- Investigation ---------- */

#     .root-cause {
#         border-left: 3px solid var(--blue);
#         background: var(--blue-dim);
#         color: #b9d9ff;
#         border-radius: 7px;
#         padding: .78rem .88rem;
#         line-height: 1.5;
#         font-size: .82rem;
#     }

#     .fix {
#         border-left: 3px solid var(--green);
#         background: var(--green-dim);
#         color: #baf4cf;
#         border-radius: 7px;
#         padding: .78rem .88rem;
#         line-height: 1.5;
#         font-size: .82rem;
#     }

#     .evidence {
#         background: #080c11;
#         border: 1px solid #18212b;
#         border-radius: 8px;
#         padding: .66rem .76rem;
#         color: #aeb7c1;
#         font-size: .72rem;
#         line-height: 1.45;
#         margin-bottom: .42rem;
#     }

#     .evidence strong {
#         color: #dce3e8;
#     }

#     .mini-label {
#         color: #7b8792;
#         font-size: .67rem;
#         font-weight: 800;
#         text-transform: uppercase;
#         letter-spacing: .08em;
#         margin-bottom: .35rem;
#     }

#     /* ---------- Activity ---------- */

#     .activity {
#         position: relative;
#         padding-left: 1rem;
#     }

#     .activity:before {
#         content: "";
#         position: absolute;
#         left: .24rem;
#         top: .3rem;
#         bottom: .3rem;
#         width: 1px;
#         background: #26323d;
#     }

#     .event {
#         position: relative;
#         margin-bottom: .8rem;
#     }

#     .event:before {
#         content: "";
#         position: absolute;
#         left: -.95rem;
#         top: .24rem;
#         width: 7px;
#         height: 7px;
#         border-radius: 50%;
#         background: #53616e;
#         box-shadow: 0 0 0 3px #0b1016;
#     }

#     .event.done:before {
#         background: var(--green);
#         box-shadow: 0 0 8px rgba(57,226,125,.35), 0 0 0 3px #0b1510;
#     }

#     .event.active:before {
#         background: #55aaff;
#         box-shadow: 0 0 10px rgba(77,163,255,.5), 0 0 0 3px #0b1510;
#     }

#     .event-title {
#         font-size: .76rem;
#         font-weight: 850;
#         color: #e8edf0;
#     }

#     .event-desc {
#         font-size: .66rem;
#         color: #6f7b87;
#         margin-top: .12rem;
#         line-height: 1.4;
#     }

#     /* ---------- Metrics / history ---------- */

#     .metric-box {
#         border: 1px solid #1b2631;
#         background: #090e14;
#         border-radius: 9px;
#         padding: .7rem;
#     }

#     .metric-label {
#         color: #687582;
#         font-size: .62rem;
#         text-transform: uppercase;
#         letter-spacing: .08em;
#         font-weight: 850;
#     }

#     .metric-value {
#         color: white;
#         font-size: 1.15rem;
#         font-weight: 900;
#         margin-top: .2rem;
#     }

#     .metric-value.green {
#         color: var(--green);
#     }

#     .history-table {
#         width: 100%;
#     }

#     .history-row {
#         display: grid;
#         grid-template-columns: 1.15fr .7fr 1.8fr .75fr .65fr;
#         gap: .7rem;
#         align-items: center;
#         padding: .7rem .75rem;
#         border-top: 1px solid #17202a;
#         font-size: .7rem;
#     }

#     .history-head {
#         border-top: 0;
#         color: #626e7b;
#         font-size: .61rem;
#         font-weight: 850;
#         letter-spacing: .08em;
#         text-transform: uppercase;
#     }

#     .history-main {
#         color: #e2e7eb;
#         font-weight: 800;
#         word-break: break-word;
#     }

#     .history-muted {
#         color: #707c88;
#         line-height: 1.35;
#     }

#     .pr-title {
#         font-size: .95rem;
#         font-weight: 850;
#     }

#     /* ---------- Buttons ---------- */

#     div[data-testid="stButton"] > button,
#     div[data-testid="stLinkButton"] > a {
#         border-radius: 8px;
#         border: 1px solid #283440;
#         background: #0d131a;
#         color: #e8edf1;
#         font-weight: 750;
#     }

#     div[data-testid="stButton"] > button:hover,
#     div[data-testid="stLinkButton"] > a:hover {
#         border-color: #466075;
#         color: white;
#     }

#     div[data-testid="stButton"] button[kind="primary"] {
#         background: #10251a;
#         border-color: #246a40;
#         color: #72eea0;
#     }

#     div[data-testid="stButton"] button[kind="primary"]:hover {
#         background: #14321f;
#         border-color: #39e27d;
#         color: #9af5bb;
#     }

#     .footer {
#         text-align: center;
#         color: #4e5965;
#         font-size: .66rem;
#         padding-top: 1.3rem;
#     }

#     @media (max-width: 900px) {
#         .pipeline {
#             flex-direction: column;
#         }
#         .connector {
#             display: none;
#         }
#         .history-row {
#             grid-template-columns: 1fr 1fr;
#         }
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# # ============================================================
# # HELPERS
# # ============================================================

# def pct(value):
#     if value is None:
#         return "—"
#     try:
#         number = float(value)
#         if number <= 1:
#             number *= 100
#         return f"{number:.1f}%"
#     except (TypeError, ValueError):
#         return str(value)


# def badge(status):
#     value = str(status or "UNKNOWN").upper()
#     if any(x in value for x in ("PASS", "SUCCESS", "COMPLETE", "REMEDIAT")):
#         cls = "badge-green"
#     elif any(x in value for x in ("FAIL", "ERROR")):
#         cls = "badge-red"
#     else:
#         cls = "badge-amber"
#     return f'<span class="badge {cls}">{escape(value)}</span>'


# def risk_badge(risk):
#     value = str(risk or "unknown").lower()
#     cls = {
#         "low": "badge-green",
#         "medium": "badge-amber",
#         "high": "badge-red",
#     }.get(value, "badge-amber")
#     return f'<span class="badge {cls}">{escape(value.upper())} RISK</span>'

# def make_demo_incident():
#     now = datetime.now(timezone.utc)

#     run_id = f"DEMO-{int(now.timestamp() * 1000)}"

#     incident = {
#         "run_id": run_id,
#         "job_id": "demo-job-001",
#         "job_name": "test",
#         "status": "CI_PASSED",
#         "conclusion": "failure",
#         "ci_status": "success",
#         "failed_step": "Run tests",
#         "commit_sha": "3684044cfb70ab1470e1a99c8bda5805c7ecec91",
#         "branch": "remediation/demo",
#         "pr_number": 3,
#         "pr_url": "https://github.com/pruthviraj-m/ci-cd-intelligence-agent/pull/3",
#         "failure_reason": (
#             "Intentional syntax error prevented the test suite "
#             "from importing the application module."
#         ),
#         "root_cause": (
#             "An intentional syntax error was introduced into "
#             "app/calculator.py."
#         ),
#         "suggested_fix": (
#             "Remove the invalid syntax line from app/calculator.py."
#         ),
#         "risk_level": "low",
#         "confidence": 100.0,
#         "updated_at": now.isoformat(),
#         "demo": True,
#         "logs": (
#             "pytest failed during test collection with "
#             "SyntaxError in app/calculator.py"
#         ),
#         "diff": (
#             "app/calculator.py was modified and introduced "
#             "an intentional syntax error."
#         ),
#     }

#     return run_id, incident


# def choose_active(incidents):
#     # A fresh dashboard load should be a clean landing state.
#     # Only an incident explicitly triggered in this session becomes active.
#     active_id = st.session_state.get("active_run_id")

#     if active_id:
#         for item in incidents:
#             if str(item.get("run_id")) == str(active_id):
#                 return item

#     return None


# def render_pipeline(stage_index, total=6):
#     stages = [
#         ("🚨", "DETECT", "CI failure detected"),
#         ("🧠", "DIAGNOSE", "AI analyzes logs & code"),
#         ("🛠️", "PATCH", "Minimal fix generated"),
#         ("🧪", "VALIDATE", "Tests run successfully"),
#         ("⑂", "PULL REQUEST", "PR created for review"),
#         ("🛡️", "VERIFY CI", "CI verification passed"),
#     ]

#     html = '<div class="pipeline">'

#     for index, (icon, name, desc) in enumerate(stages):
#         # stage_index == -1 means the system is idle before a demo is triggered.
#         if stage_index < 0:
#             state_class = "waiting"
#             state = "○ WAITING"
#         elif stage_index >= total:
#             state_class = "done"
#             state = "✓ COMPLETE"
#         elif index < stage_index:
#             state_class = "done"
#             state = "✓ COMPLETE"
#         elif index == stage_index:
#             state_class = "active"
#             state = "● RUNNING"
#         elif index == 0 and stage_index == 0:
#             state_class = "failed"
#             state = "● FAILURE DETECTED"
#         else:
#             state_class = "waiting"
#             state = "○ WAITING"

#         html += f"""
#         <div class="stage {state_class}">
#             <div class="stage-icon">{icon}</div>
#             <div class="stage-name">{escape(name)}</div>
#             <div class="stage-desc">{escape(desc)}</div>
#             <div class="stage-state">{escape(state)}</div>
#         </div>
#         """

#         if index < len(stages) - 1:
#             connector_class = "done" if stage_index > index else ""
#             html += f'<div class="connector {connector_class}"></div>'

#     html += "</div>"
#     return html


# def render_activity(latest, stage_index, total=6):
#     run_id = escape(str(latest.get("run_id", "N/A")))
#     job = escape(str(latest.get("job_name", "test")))
#     pr_number = latest.get("pr_number")

#     events = [
#         ("CI failure detected", f"Run #{run_id} failed in {job}."),
#         ("Evidence collected", "Logs, failed step and changed-file context inspected."),
#         ("AI diagnosis", "Root cause and affected files identified from supplied evidence."),
#         ("Remediation generated", "Smallest supported fix proposed."),
#         ("Validation", "Fix validated before CI verification."),
#         ("Pull request", f"PR #{escape(str(pr_number))} created for CI verification." if pr_number else "No pull request recorded."),
#         ("CI verification", f"Status: {escape(str(latest.get('ci_status', 'N/A')))}."),
#     ]

#     html = '<div class="activity">'

#     visible = min(stage_index + 1, len(events))

#     for i, (title, desc) in enumerate(events):
#         if i < visible - 1 or stage_index >= total:
#             cls = "done"
#         elif i == visible - 1:
#             cls = "active"
#         else:
#             cls = ""

#         html += f"""
#         <div class="event {cls}">
#             <div class="event-title">{escape(title)}</div>
#             <div class="event-desc">{desc}</div>
#         </div>
#         """

#     html += "</div>"
#     return html


# def render_incident_card(latest, active=True, running=False):
#     run_id = escape(str(latest.get("run_id", "N/A")))
#     job = escape(str(latest.get("job_name", "N/A")))
#     failed_step = escape(str(latest.get("failed_step", "N/A")))

#     if running:
#         current_status = '<span class="badge badge-amber">REMEDIATING</span>'
#     else:
#         current_status = badge(latest.get("status"))

#     return f"""
#     <div class="panel">
#         <div class="section-title">Active Incident</div>
#         <div class="incident-id">Run #{run_id}</div>
#         <div class="meta">{job} &nbsp;/&nbsp; {failed_step}</div>
#         <div style="height:.75rem"></div>
#         {current_status}
#         <div style="height:.8rem"></div>
#         <div class="kv">
#             <div class="k">CI status</div>
#             <div class="v">{escape(str(latest.get("ci_status", "N/A")))}</div>
#             <div class="k">Branch</div>
#             <div class="v">{escape(str(latest.get("branch", "N/A")))}</div>
#             <div class="k">Commit</div>
#             <div class="v">{escape(str(latest.get("commit_sha", "N/A")))}</div>
#             <div class="k">Updated</div>
#             <div class="v">{escape(str(latest.get("updated_at", "N/A")))}</div>
#         </div>
#     </div>
#     """


# def render_activity_panel(latest, stage_index):
#     return f"""
#     <div class="panel">
#         <div class="section-title">⚡ Agent Activity</div>
#         {render_activity(latest, stage_index)}
#     </div>
#     """


# # ============================================================
# # SESSION STATE
# # ============================================================

# if "active_run_id" not in st.session_state:
#     st.session_state.active_run_id = None

# if "demo_playing" not in st.session_state:
#     st.session_state.demo_playing = False


# # ============================================================
# # SIDEBAR
# # ============================================================

# with st.sidebar:
#     st.markdown(
#         """
#         <div class="brand">
#             <div class="brand-title">🤖 CI/CD Intelligence Agent</div>
#             <div class="brand-sub">Autonomous failure diagnosis & remediation</div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.markdown('<div class="eyebrow">Navigation</div>', unsafe_allow_html=True)
#     st.markdown(
#         """
#         <div class="side-nav">
#             <div class="active">▣ Dashboard</div>
#             <div>◇ Incidents</div>
#             <div>⌁ Activity</div>
#             <div>⑂ Pull Requests</div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.markdown("---")

#     st.markdown('<div class="eyebrow">Demo Controls</div>', unsafe_allow_html=True)
#     st.markdown(
#         '<div class="side-copy">Simulate a safe CI failure and watch the agent move through detection, diagnosis, remediation and verification.</div>',
#         unsafe_allow_html=True,
#     )

#     trigger = st.button(
#         "🚨  Trigger Test Incident",
#         use_container_width=True,
#         type="primary",
#         disabled=st.session_state.demo_playing,
#     )

#     if trigger:
#         run_id, incident = make_demo_incident()
#         save_incident(run_id, incident)

#         st.session_state.active_run_id = run_id
#         st.session_state.demo_playing = True
#         st.rerun()

#     st.markdown("---")

#     st.markdown('<div class="eyebrow">System Status</div>', unsafe_allow_html=True)
#     st.markdown(
#         """
#         <div style="margin-bottom:.65rem;">
#             <span class="live"><span class="dot"></span> System Live</span>
#         </div>
#         <div class="side-status">
#             <div>● &nbsp;Redis state store &nbsp;<span class="ok">Available</span></div>
#             <div>● &nbsp;Dashboard &nbsp;<span class="ok">Running</span></div>
#             <div>● &nbsp;Incident data &nbsp;<span class="ok">Loaded</span></div>
#             <div>● &nbsp;Remediation engine &nbsp;<span class="ok">Ready</span></div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.markdown(
#         '<div class="footer">CI/CD Intelligence Agent<br>v1.0.0</div>',
#         unsafe_allow_html=True,
#     )


# # ============================================================
# # DATA
# # ============================================================

# incidents = list_incidents()
# latest = choose_active(incidents)


# # ============================================================
# # EMPTY STATE
# # ============================================================

# if not latest:
#     st.markdown('<div class="eyebrow">Engineering Command Center</div>', unsafe_allow_html=True)
#     st.markdown('<div class="hero-title">CI/CD Intelligence Agent</div>', unsafe_allow_html=True)
#     st.markdown(
#         '<div class="hero-sub">Autonomous CI failure diagnosis & remediation</div>',
#         unsafe_allow_html=True,
#     )

#     st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

#     # Landing state: show the full remediation story, but nothing is complete
#     # until the user explicitly triggers the test incident.
#     st.markdown(
#         f"""
#         <div class="panel">
#             <div class="section-title">Autonomous Remediation Pipeline</div>
#             {render_pipeline(-1)}
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.markdown("<div style='height:.65rem'></div>", unsafe_allow_html=True)

#     st.markdown(
#         """
#         <div class="status-banner active">
#             ◉ SYSTEM READY
#             <span>Waiting for a CI failure. Trigger a test incident to start the autonomous remediation loop.</span>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.markdown("<div style='height:.65rem'></div>", unsafe_allow_html=True)

#     st.markdown(
#         """
#         <div class="panel" style="text-align:center;padding:1.15rem;">
#             <div style="font-size:1rem;font-weight:850;">No active incident</div>
#             <div class="meta">The pipeline will populate with the incident ID, diagnosis, patch, validation, pull request and CI verification after you trigger the demo.</div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
#     st.stop()


# # ============================================================
# # HEADER
# # ============================================================

# header_left, header_right = st.columns([5, 1])

# with header_left:
#     st.markdown('<div class="eyebrow">Engineering Command Center</div>', unsafe_allow_html=True)
#     st.markdown('<div class="hero-title">CI/CD Intelligence Agent</div>', unsafe_allow_html=True)
#     st.markdown(
#         '<div class="hero-sub">Autonomous CI failure diagnosis & remediation</div>',
#         unsafe_allow_html=True,
#     )

# with header_right:
#     st.markdown(
#         '<div style="text-align:right;margin-top:.25rem;"><span class="live"><span class="dot"></span> System Live</span></div>',
#         unsafe_allow_html=True,
#     )
#     if st.button("↻ Refresh", use_container_width=True):
#         st.rerun()


# st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)


# # ============================================================
# # LIVE DEMO AREA
# # Only runs after Trigger Test Incident.
# # Normal refreshes never replay it.
# # ============================================================

# running = bool(st.session_state.demo_playing)

# pipeline_placeholder = st.empty()
# status_placeholder = st.empty()
# incident_placeholder = st.empty()

# # During the demo, the page visibly progresses through the actual story.
# if running:
#     for stage in range(6):
#         pipeline_placeholder.markdown(
#             f"""
#             <div class="panel">
#                 <div class="section-title">Autonomous Remediation Pipeline</div>
#                 {render_pipeline(stage)}
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#         status_text = [
#             ("failed", "● CI FAILURE DETECTED", "The agent has received a failed test run and is collecting evidence."),
#             ("active", "◉ ANALYZING INCIDENT", "Logs, failed step and changed files are being inspected."),
#             ("active", "◉ GENERATING REMEDIATION", "The agent is producing the smallest supported fix."),
#             ("active", "◉ VALIDATING PATCH", "The proposed change is being checked before CI verification."),
#             ("active", "◉ SUBMITTING PULL REQUEST", "The remediation change is ready for CI verification."),
#             ("active", "◉ VERIFYING CI", "The repaired pipeline is being checked."),
#         ][stage]

#         status_placeholder.markdown(
#             f"""
#             <div class="status-banner {status_text[0]}">
#                 {status_text[1]}
#                 <span>{status_text[2]}</span>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#         incident_placeholder.markdown(
#             render_incident_card(latest, running=True),
#             unsafe_allow_html=True,
#         )

#         sleep(.58)

#     # Final state remains visible for the normal dashboard render below.
#     st.session_state.demo_playing = False
#     st.rerun()

# # Static final dashboard.
# pipeline_placeholder.markdown(
#     f"""
#     <div class="panel">
#         <div class="section-title">Autonomous Remediation Pipeline</div>
#         {render_pipeline(6)}
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# status_placeholder.markdown(
#     """
#     <div class="status-banner">
#         ✓ REMEDIATION COMPLETE
#         <span>The pipeline is healthy again.</span>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# incident_placeholder.markdown(
#     render_incident_card(latest),
#     unsafe_allow_html=True,
# )


# # ============================================================
# # INVESTIGATION / REMEDIATION / ACTIVITY
# # ============================================================

# st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# investigation_col, remediation_col, activity_col = st.columns(
#     [1.25, 1.25, .95],
#     gap="large",
# )

# with investigation_col:
#     st.markdown('<div class="panel">', unsafe_allow_html=True)
#     st.markdown('<div class="section-title">🧠 Agent Investigation</div>', unsafe_allow_html=True)

#     st.markdown("<b>Root Cause</b>", unsafe_allow_html=True)
#     root = escape(str(
#         latest.get("root_cause")
#         or latest.get("failure_reason")
#         or "Diagnosis not available."
#     ))
#     st.markdown(f'<div class="root-cause">{root}</div>', unsafe_allow_html=True)

#     st.markdown("<div style='height:.75rem'></div>", unsafe_allow_html=True)
#     st.markdown("<b>Failure Evidence</b>", unsafe_allow_html=True)

#     failure_reason = latest.get("failure_reason")
#     if failure_reason:
#         st.markdown(
#             f'<div class="evidence"><strong>CI failure</strong><br>{escape(str(failure_reason))}</div>',
#             unsafe_allow_html=True,
#         )

#     evidence = latest.get("evidence", [])
#     if isinstance(evidence, list):
#         for item in evidence[:4]:
#             if isinstance(item, dict):
#                 source = escape(str(item.get("source", "Evidence")))
#                 observation = escape(str(item.get("observation", "")))
#                 st.markdown(
#                     f'<div class="evidence"><strong>{source}</strong><br>{observation}</div>',
#                     unsafe_allow_html=True,
#                 )
#             elif item:
#                 st.markdown(
#                     f'<div class="evidence">{escape(str(item))}</div>',
#                     unsafe_allow_html=True,
#                 )

#     affected = latest.get("affected_files", [])
#     if affected:
#         st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
#         st.markdown('<div class="mini-label">Affected Files</div>', unsafe_allow_html=True)
#         for file_name in affected[:6]:
#             st.code(str(file_name), language=None)

#     st.markdown(
#         f"""
#         <div style="display:flex;justify-content:space-between;align-items:center;margin-top:.7rem;">
#             <span style="color:#7b8792;font-size:.68rem;">Confidence <b style="color:#fff;">{pct(latest.get("confidence"))}</b></span>
#             {risk_badge(latest.get("risk_level"))}
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.markdown('</div>', unsafe_allow_html=True)


# with remediation_col:
#     st.markdown('<div class="panel">', unsafe_allow_html=True)
#     st.markdown('<div class="section-title">🛠 Agent Remediation</div>', unsafe_allow_html=True)

#     st.markdown("<b>Proposed Fix</b>", unsafe_allow_html=True)
#     fix = escape(str(latest.get("suggested_fix", "No proposed fix available.")))
#     st.markdown(f'<div class="fix">{fix}</div>', unsafe_allow_html=True)

#     st.markdown("<div style='height:.75rem'></div>", unsafe_allow_html=True)

#     patch = latest.get("patch") or latest.get("patch_proposal")

#     if patch:
#         st.markdown("<b>Patch / Change</b>", unsafe_allow_html=True)

#         if isinstance(patch, dict):
#             explanation = patch.get("explanation")
#             if explanation:
#                 st.caption(str(explanation))

#             for change in patch.get("changes", []):
#                 if isinstance(change, dict):
#                     file_path = str(change.get("file_path", "file"))
#                     old_text = str(change.get("old_text", ""))
#                     new_text = str(change.get("new_text", ""))

#                     st.markdown(f"**{escape(file_path)}**")
#                     st.code(
#                         f"- {old_text}\n+ {new_text}",
#                         language="diff",
#                     )
#         else:
#             st.code(str(patch), language="diff")
#     else:
#         st.markdown(
#             """
#             <div class="evidence">
#                 <strong>Minimal-change principle</strong><br>
#                 The agent proposes the smallest supported change, then validates it before CI verification.
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#     metric_a, metric_b = st.columns(2)

#     with metric_a:
#         st.markdown(
#             f"""
#             <div class="metric-box">
#                 <div class="metric-label">Risk</div>
#                 <div class="metric-value green">{escape(str(latest.get("risk_level", "—")).upper())}</div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#     with metric_b:
#         st.markdown(
#             f"""
#             <div class="metric-box">
#                 <div class="metric-label">Confidence</div>
#                 <div class="metric-value">{pct(latest.get("confidence"))}</div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#     st.markdown('</div>', unsafe_allow_html=True)


# with activity_col:
#     st.markdown(
#         render_activity_panel(latest, 6),
#         unsafe_allow_html=True,
#     )


# # ============================================================
# # PR + PERFORMANCE
# # ============================================================

# st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# pr_col, perf_col = st.columns([2.25, 1], gap="large")

# with pr_col:
#     st.markdown('<div class="panel">', unsafe_allow_html=True)
#     st.markdown('<div class="section-title">⑂ Pull Request</div>', unsafe_allow_html=True)

#     if latest.get("pr_url"):
#         st.markdown(
#             f"""
#             <div class="pr-title">AI-generated remediation PR #{escape(str(latest.get("pr_number", "N/A")))}</div>
#             <div class="meta">The proposed fix was committed and submitted for CI verification.</div>
#             """,
#             unsafe_allow_html=True,
#         )
#         st.markdown("<div style='height:.65rem'></div>", unsafe_allow_html=True)
#         st.link_button("Open Pull Request →", str(latest["pr_url"]))
#     else:
#         st.markdown(
#             '<div class="meta">No pull request is recorded for this incident.</div>',
#             unsafe_allow_html=True,
#         )

#     st.markdown('</div>', unsafe_allow_html=True)


# with perf_col:
#     total = len(incidents)

#     passed = sum(
#         1
#         for item in incidents
#         if "PASS" in str(item.get("status", "")).upper()
#         or str(item.get("ci_status", "")).lower() in {"success", "passed"}
#     )

#     avg_conf_values = []

#     for item in incidents:
#         value = item.get("confidence")
#         try:
#             value = float(value)
#             if value <= 1:
#                 value *= 100
#             avg_conf_values.append(value)
#         except (TypeError, ValueError):
#             pass

#     avg_conf = (
#         sum(avg_conf_values) / len(avg_conf_values)
#         if avg_conf_values
#         else None
#     )

#     st.markdown('<div class="panel">', unsafe_allow_html=True)
#     st.markdown('<div class="section-title">Agent Performance</div>', unsafe_allow_html=True)

#     a, b = st.columns(2)

#     with a:
#         st.markdown(
#             f'<div class="metric-box"><div class="metric-label">Incidents</div><div class="metric-value">{total}</div></div>',
#             unsafe_allow_html=True,
#         )

#     with b:
#         success_pct = (passed / total * 100) if total else 0
#         st.markdown(
#             f'<div class="metric-box"><div class="metric-label">CI Success</div><div class="metric-value green">{success_pct:.0f}%</div></div>',
#             unsafe_allow_html=True,
#         )

#     st.markdown("<div style='height:.45rem'></div>", unsafe_allow_html=True)

#     st.markdown(
#         f'<div class="metric-box"><div class="metric-label">Average Confidence</div><div class="metric-value">{f"{avg_conf:.1f}%" if avg_conf is not None else "—"}</div></div>',
#         unsafe_allow_html=True,
#     )

#     st.markdown('</div>', unsafe_allow_html=True)


# # ============================================================
# # INCIDENT HISTORY
# # ============================================================

# st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# st.markdown('<div class="panel">', unsafe_allow_html=True)
# st.markdown('<div class="section-title">▣ Incident History</div>', unsafe_allow_html=True)

# st.markdown(
#     """
#     <div class="history-row history-head">
#         <div>Run ID</div>
#         <div>Job</div>
#         <div>Failure / Root Cause</div>
#         <div>Status</div>
#         <div>CI</div>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# for incident in incidents[:10]:
#     run_id = escape(str(incident.get("run_id", "N/A")))
#     job = escape(str(incident.get("job_name", "N/A")))
#     root = incident.get("root_cause") or incident.get("failure_reason") or "Unknown"

#     root_short = str(root).replace("\n", " ")
#     if len(root_short) > 92:
#         root_short = root_short[:89] + "..."

#     root_short = escape(root_short)

#     st.markdown(
#         f"""
#         <div class="history-row">
#             <div class="history-main">#{run_id}</div>
#             <div class="history-muted">{job}</div>
#             <div class="history-muted">{root_short}</div>
#             <div>{badge(incident.get("status"))}</div>
#             <div>{badge(incident.get("ci_status"))}</div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# st.markdown('</div>', unsafe_allow_html=True)


# # ============================================================
# # FOOTER
# # ============================================================

# st.markdown(
#     '<div class="footer">Built with Streamlit · Redis · Kafka · NVIDIA AI · GitHub Actions</div>',
#     unsafe_allow_html=True,
# )


import sys
from pathlib import Path
from datetime import datetime, timezone
from time import sleep
from html import escape
from types import SimpleNamespace

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.state_store import (
    list_incidents,
    save_incident,
    recall_similar_incidents,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CI/CD Intelligence Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# VISUAL SYSTEM
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --bg: #05070a;
        --panel: #0b0f14;
        --panel2: #0e141b;
        --border: #1b2631;
        --text: #f4f7f9;
        --muted: #778491;
        --green: #39e27d;
        --green-dim: #0a2417;
        --red: #ff5c68;
        --red-dim: #2a1015;
        --blue: #4da3ff;
        --blue-dim: #0b1c2d;
        --purple: #c084fc;
        --amber: #f6c453;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(5, 7, 10, .94);
    }

    [data-testid="stSidebar"] {
        background: #070a0e;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.1rem;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.2rem;
        padding-bottom: 2.8rem;
    }

    /* ---------- Typography ---------- */

    .eyebrow {
        color: #9aa7b3;
        font-size: .68rem;
        font-weight: 850;
        letter-spacing: .14em;
        text-transform: uppercase;
        margin-bottom: .42rem;
    }

    .hero-title {
        font-size: 2.25rem;
        line-height: 1;
        font-weight: 900;
        letter-spacing: -.05em;
        margin: 0;
    }

    .hero-sub {
        color: var(--muted);
        margin-top: .45rem;
        font-size: .92rem;
    }

    .section-title {
        color: #dce3e8;
        font-size: .68rem;
        font-weight: 850;
        letter-spacing: .12em;
        text-transform: uppercase;
        margin: 0 0 .75rem;
    }

    /* ---------- Sidebar ---------- */

    .brand {
        padding: .4rem 0 1.25rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.15rem;
    }

    .brand-title {
        font-size: 1.08rem;
        font-weight: 850;
        color: white;
    }

    .brand-sub {
        color: var(--muted);
        font-size: .76rem;
        margin-top: .18rem;
        line-height: 1.45;
    }

    .side-nav {
        color: #e6ebef;
        font-size: .88rem;
        line-height: 2.9;
    }

    .side-nav .active {
        color: white;
        font-weight: 800;
    }

    .side-copy {
        color: #8995a1;
        font-size: .76rem;
        line-height: 1.55;
    }

    .side-status {
        color: #8995a1;
        font-size: .74rem;
        line-height: 1.9;
    }

    .side-status .ok {
        color: var(--green);
    }

    .live {
        display: inline-flex;
        align-items: center;
        gap: .45rem;
        border: 1px solid #19482d;
        background: #09150f;
        color: var(--green);
        padding: .38rem .65rem;
        border-radius: 999px;
        font-size: .68rem;
        font-weight: 850;
        letter-spacing: .06em;
        text-transform: uppercase;
    }

    .dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        display: inline-block;
        background: var(--green);
        box-shadow: 0 0 10px rgba(57,226,125,.7);
    }

    /* ---------- Panels ---------- */

    .panel {
        background: linear-gradient(180deg, #0b1016 0%, #090d12 100%);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem 1.05rem;
    }

    .panel-tight {
        padding: .82rem .9rem;
    }

    .spacer {
        height: .9rem;
    }

    /* ---------- Pipeline ---------- */

    .pipeline {
        display: flex;
        align-items: stretch;
        gap: .32rem;
    }

    .stage {
        flex: 1;
        min-width: 0;
        border: 1px solid #26323e;
        background: #0a0f15;
        border-radius: 10px;
        padding: .72rem .5rem;
        text-align: center;
        transition: all .2s ease;
    }

    .stage.waiting {
        opacity: .48;
    }

    .stage.active {
        border-color: #4b8fd2;
        background: #0c1927;
        box-shadow: 0 0 0 1px rgba(77,163,255,.15), 0 0 24px rgba(77,163,255,.08);
    }

    .stage.failed {
        border-color: #71303a;
        background: #160b0f;
    }

    .stage.done {
        border-color: #1d6740;
        background: #091b12;
    }

    .stage-icon {
        font-size: 1.12rem;
        margin-bottom: .25rem;
    }

    .stage-name {
        font-size: .69rem;
        font-weight: 900;
        color: #eef2f4;
    }

    .stage-desc {
        color: #74808c;
        font-size: .61rem;
        line-height: 1.35;
        margin-top: .25rem;
        min-height: 2.05em;
    }

    .stage-state {
        font-size: .59rem;
        font-weight: 850;
        margin-top: .45rem;
        color: #687580;
    }

    .stage.done .stage-state {
        color: var(--green);
    }

    .stage.active .stage-state {
        color: #72baff;
    }

    .stage.failed .stage-state {
        color: #ff7882;
    }

    .connector {
        width: 14px;
        align-self: center;
        border-top: 1px dashed #33404c;
        opacity: .8;
    }

    .connector.done {
        border-color: #2c7650;
    }

    .status-banner {
        border: 1px solid #1d6c40;
        background: linear-gradient(90deg, #082017, #0b2518);
        color: var(--green);
        border-radius: 10px;
        padding: .75rem 1rem;
        text-align: center;
        font-weight: 900;
        font-size: .9rem;
    }

    .status-banner.active {
        border-color: #315c86;
        background: linear-gradient(90deg, #0a1622, #0b1b2a);
        color: #71baff;
    }

    .status-banner.failed {
        border-color: #6b2932;
        background: linear-gradient(90deg, #210d12, #180b0e);
        color: #ff7580;
    }

    .status-banner span {
        display: block;
        color: #74818c;
        font-size: .69rem;
        font-weight: 500;
        margin-top: .2rem;
    }

    /* ---------- Incident ---------- */

    .incident-id {
        font-size: 1.38rem;
        font-weight: 900;
        letter-spacing: -.035em;
        word-break: break-word;
    }

    .meta {
        color: var(--muted);
        font-size: .78rem;
        margin-top: .25rem;
    }

    .kv {
        display: grid;
        grid-template-columns: 74px 1fr;
        gap: .42rem .7rem;
        font-size: .76rem;
    }

    .kv .k {
        color: #66727e;
    }

    .kv .v {
        color: #dfe4e8;
        word-break: break-word;
    }

    .badge {
        display: inline-block;
        padding: .26rem .52rem;
        border-radius: 999px;
        font-size: .62rem;
        font-weight: 900;
        letter-spacing: .04em;
    }

    .badge-green {
        background: #0c2a1b;
        border: 1px solid #1b6840;
        color: var(--green);
    }

    .badge-red {
        background: var(--red-dim);
        border: 1px solid #6d2830;
        color: #ff7a7a;
    }

    .badge-amber {
        background: #241b09;
        border: 1px solid #5d4719;
        color: var(--amber);
    }

    /* ---------- Investigation ---------- */

    .root-cause {
        border-left: 3px solid var(--blue);
        background: var(--blue-dim);
        color: #b9d9ff;
        border-radius: 7px;
        padding: .78rem .88rem;
        line-height: 1.5;
        font-size: .82rem;
    }

    .fix {
        border-left: 3px solid var(--green);
        background: var(--green-dim);
        color: #baf4cf;
        border-radius: 7px;
        padding: .78rem .88rem;
        line-height: 1.5;
        font-size: .82rem;
    }

    .evidence {
        background: #080c11;
        border: 1px solid #18212b;
        border-radius: 8px;
        padding: .66rem .76rem;
        color: #aeb7c1;
        font-size: .72rem;
        line-height: 1.45;
        margin-bottom: .42rem;
    }

    .evidence strong {
        color: #dce3e8;
    }

    .mini-label {
        color: #7b8792;
        font-size: .67rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .08em;
        margin-bottom: .35rem;
    }

    /* ---------- Activity ---------- */

    .activity {
        position: relative;
        padding-left: 1rem;
    }

    .activity:before {
        content: "";
        position: absolute;
        left: .24rem;
        top: .3rem;
        bottom: .3rem;
        width: 1px;
        background: #26323d;
    }

    .event {
        position: relative;
        margin-bottom: .8rem;
    }

    .event:before {
        content: "";
        position: absolute;
        left: -.95rem;
        top: .24rem;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #53616e;
        box-shadow: 0 0 0 3px #0b1016;
    }

    .event.done:before {
        background: var(--green);
        box-shadow: 0 0 8px rgba(57,226,125,.35), 0 0 0 3px #0b1510;
    }

    .event.active:before {
        background: #55aaff;
        box-shadow: 0 0 10px rgba(77,163,255,.5), 0 0 0 3px #0b1510;
    }

    .event-title {
        font-size: .76rem;
        font-weight: 850;
        color: #e8edf0;
    }

    .event-desc {
        font-size: .66rem;
        color: #6f7b87;
        margin-top: .12rem;
        line-height: 1.4;
    }

    /* ---------- Metrics / history ---------- */

    .metric-box {
        border: 1px solid #1b2631;
        background: #090e14;
        border-radius: 9px;
        padding: .7rem;
    }

    .metric-label {
        color: #687582;
        font-size: .62rem;
        text-transform: uppercase;
        letter-spacing: .08em;
        font-weight: 850;
    }

    .metric-value {
        color: white;
        font-size: 1.15rem;
        font-weight: 900;
        margin-top: .2rem;
    }

    .metric-value.green {
        color: var(--green);
    }

    .history-table {
        width: 100%;
    }

    .history-row {
        display: grid;
        grid-template-columns: 1.15fr .7fr 1.8fr .75fr .65fr;
        gap: .7rem;
        align-items: center;
        padding: .7rem .75rem;
        border-top: 1px solid #17202a;
        font-size: .7rem;
    }

    .history-head {
        border-top: 0;
        color: #626e7b;
        font-size: .61rem;
        font-weight: 850;
        letter-spacing: .08em;
        text-transform: uppercase;
    }

    .history-main {
        color: #e2e7eb;
        font-weight: 800;
        word-break: break-word;
    }

    .history-muted {
        color: #707c88;
        line-height: 1.35;
    }

    .pr-title {
        font-size: .95rem;
        font-weight: 850;
    }

    /* ---------- Buttons ---------- */

    div[data-testid="stButton"] > button,
    div[data-testid="stLinkButton"] > a {
        border-radius: 8px;
        border: 1px solid #283440;
        background: #0d131a;
        color: #e8edf1;
        font-weight: 750;
    }

    div[data-testid="stButton"] > button:hover,
    div[data-testid="stLinkButton"] > a:hover {
        border-color: #466075;
        color: white;
    }

    div[data-testid="stButton"] button[kind="primary"] {
        background: #10251a;
        border-color: #246a40;
        color: #72eea0;
    }

    div[data-testid="stButton"] button[kind="primary"]:hover {
        background: #14321f;
        border-color: #39e27d;
        color: #9af5bb;
    }

    .footer {
        text-align: center;
        color: #4e5965;
        font-size: .66rem;
        padding-top: 1.3rem;
    }

    @media (max-width: 900px) {
        .pipeline {
            flex-direction: column;
        }
        .connector {
            display: none;
        }
        .history-row {
            grid-template-columns: 1fr 1fr;
        }
    }

    /* ---------- Hindsight Memory ---------- */

    .hindsight-card {
        border: 1px solid #3b2b57;
        background: linear-gradient(180deg, #110d18 0%, #0b0d12 100%);
        border-radius: 12px;
        padding: 1rem 1.05rem;
    }

    .hindsight-title {
        color: #d8b4fe;
        font-size: .68rem;
        font-weight: 850;
        letter-spacing: .12em;
        text-transform: uppercase;
        margin-bottom: .75rem;
    }

    .hindsight-stat {
        color: #e8ddf7;
        font-size: .85rem;
        font-weight: 800;
    }

    .hindsight-muted {
        color: #81778d;
        font-size: .7rem;
        line-height: 1.45;
    }

    .hindsight-memory {
        border: 1px solid #2a2038;
        background: #0b0910;
        border-radius: 8px;
        padding: .65rem .75rem;
        margin-top: .55rem;
    }

    .hindsight-memory strong {
        color: #d8b4fe;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def pct(value):
    if value is None:
        return "—"
    try:
        number = float(value)
        if number <= 1:
            number *= 100
        return f"{number:.1f}%"
    except (TypeError, ValueError):
        return str(value)


def badge(status):
    value = str(status or "UNKNOWN").upper()
    if any(x in value for x in ("PASS", "SUCCESS", "COMPLETE", "REMEDIAT")):
        cls = "badge-green"
    elif any(x in value for x in ("FAIL", "ERROR")):
        cls = "badge-red"
    else:
        cls = "badge-amber"
    return f'<span class="badge {cls}">{escape(value)}</span>'


def risk_badge(risk):
    value = str(risk or "unknown").lower()
    cls = {
        "low": "badge-green",
        "medium": "badge-amber",
        "high": "badge-red",
    }.get(value, "badge-amber")
    return f'<span class="badge {cls}">{escape(value.upper())} RISK</span>'

def make_demo_incident():
    now = datetime.now(timezone.utc)

    run_id = f"DEMO-{int(now.timestamp() * 1000)}"

    incident = {
        "run_id": run_id,
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
        "updated_at": now.isoformat(),
        "demo": True,
        "logs": (
            "pytest failed during test collection with "
            "SyntaxError in app/calculator.py"
        ),
        "diff": (
            "app/calculator.py was modified and introduced "
            "an intentional syntax error."
        ),
    }

    return run_id, incident


def choose_active(incidents):
    # A fresh dashboard load should be a clean landing state.
    # Only an incident explicitly triggered in this session becomes active.
    active_id = st.session_state.get("active_run_id")

    if active_id:
        for item in incidents:
            if str(item.get("run_id")) == str(active_id):
                return item

    return None


def render_pipeline(stage_index, total=6):
    stages = [
        ("🚨", "DETECT", "CI failure detected"),
        ("🧠", "DIAGNOSE", "AI analyzes logs & code"),
        ("🛠️", "PATCH", "Minimal fix generated"),
        ("🧪", "VALIDATE", "Tests run successfully"),
        ("⑂", "PULL REQUEST", "PR created for review"),
        ("🛡️", "VERIFY CI", "CI verification passed"),
    ]

    html = '<div class="pipeline">'

    for index, (icon, name, desc) in enumerate(stages):
        # stage_index == -1 means the system is idle before a demo is triggered.
        if stage_index < 0:
            state_class = "waiting"
            state = "○ WAITING"
        elif stage_index >= total:
            state_class = "done"
            state = "✓ COMPLETE"
        elif index < stage_index:
            state_class = "done"
            state = "✓ COMPLETE"
        elif index == stage_index:
            state_class = "active"
            state = "● RUNNING"
        elif index == 0 and stage_index == 0:
            state_class = "failed"
            state = "● FAILURE DETECTED"
        else:
            state_class = "waiting"
            state = "○ WAITING"

        html += f"""
        <div class="stage {state_class}">
            <div class="stage-icon">{icon}</div>
            <div class="stage-name">{escape(name)}</div>
            <div class="stage-desc">{escape(desc)}</div>
            <div class="stage-state">{escape(state)}</div>
        </div>
        """

        if index < len(stages) - 1:
            connector_class = "done" if stage_index > index else ""
            html += f'<div class="connector {connector_class}"></div>'

    html += "</div>"
    return html


def render_activity(latest, stage_index, total=6):
    run_id = escape(str(latest.get("run_id", "N/A")))
    job = escape(str(latest.get("job_name", "test")))
    pr_number = latest.get("pr_number")

    events = [
        ("CI failure detected", f"Run #{run_id} failed in {job}."),
        ("Evidence collected", "Logs, failed step and changed-file context inspected."),
        ("AI diagnosis", "Root cause and affected files identified from supplied evidence."),
        ("Remediation generated", "Smallest supported fix proposed."),
        ("Validation", "Fix validated before CI verification."),
        ("Pull request", f"PR #{escape(str(pr_number))} created for CI verification." if pr_number else "No pull request recorded."),
        ("CI verification", f"Status: {escape(str(latest.get('ci_status', 'N/A')))}."),
    ]

    html = '<div class="activity">'

    visible = min(stage_index + 1, len(events))

    for i, (title, desc) in enumerate(events):
        if i < visible - 1 or stage_index >= total:
            cls = "done"
        elif i == visible - 1:
            cls = "active"
        else:
            cls = ""

        html += f"""
        <div class="event {cls}">
            <div class="event-title">{escape(title)}</div>
            <div class="event-desc">{desc}</div>
        </div>
        """

    html += "</div>"
    return html


def render_incident_card(latest, active=True, running=False):
    run_id = escape(str(latest.get("run_id", "N/A")))
    job = escape(str(latest.get("job_name", "N/A")))
    failed_step = escape(str(latest.get("failed_step", "N/A")))

    if running:
        current_status = '<span class="badge badge-amber">REMEDIATING</span>'
    else:
        current_status = badge(latest.get("status"))

    return f"""
    <div class="panel">
        <div class="section-title">Active Incident</div>
        <div class="incident-id">Run #{run_id}</div>
        <div class="meta">{job} &nbsp;/&nbsp; {failed_step}</div>
        <div style="height:.75rem"></div>
        {current_status}
        <div style="height:.8rem"></div>
        <div class="kv">
            <div class="k">CI status</div>
            <div class="v">{escape(str(latest.get("ci_status", "N/A")))}</div>
            <div class="k">Branch</div>
            <div class="v">{escape(str(latest.get("branch", "N/A")))}</div>
            <div class="k">Commit</div>
            <div class="v">{escape(str(latest.get("commit_sha", "N/A")))}</div>
            <div class="k">Updated</div>
            <div class="v">{escape(str(latest.get("updated_at", "N/A")))}</div>
        </div>
    </div>
    """


def render_activity_panel(latest, stage_index):
    return f"""
    <div class="panel">
        <div class="section-title">⚡ Agent Activity</div>
        {render_activity(latest, stage_index)}
    </div>
    """


# ============================================================
# SESSION STATE
# ============================================================

if "active_run_id" not in st.session_state:
    st.session_state.active_run_id = None

if "demo_playing" not in st.session_state:
    st.session_state.demo_playing = False


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-title">🤖 CI/CD Intelligence Agent</div>
            <div class="brand-sub">Autonomous failure diagnosis & remediation</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="eyebrow">Navigation</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="side-nav">
            <div class="active">▣ Dashboard</div>
            <div>◇ Incidents</div>
            <div>⌁ Activity</div>
            <div>⑂ Pull Requests</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown('<div class="eyebrow">Demo Controls</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="side-copy">Simulate a safe CI failure and watch the agent move through detection, diagnosis, remediation and verification.</div>',
        unsafe_allow_html=True,
    )

    trigger = st.button(
        "🚨  Trigger Test Incident",
        use_container_width=True,
        type="primary",
        disabled=st.session_state.demo_playing,
    )

    if trigger:
        run_id, incident = make_demo_incident()

        # Recall previous verified incidents before this demo starts.
        hindsight = recall_similar_incidents(
            SimpleNamespace(**incident),
            limit=3,
        )

        incident["hindsight_recalled"] = hindsight

        save_incident(run_id, incident)

        st.session_state.active_run_id = run_id
        st.session_state.demo_playing = True
        st.rerun()

    st.markdown("---")

    st.markdown('<div class="eyebrow">System Status</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="margin-bottom:.65rem;">
            <span class="live"><span class="dot"></span> System Live</span>
        </div>
        <div class="side-status">
            <div>● &nbsp;Redis state store &nbsp;<span class="ok">Available</span></div>
            <div>● &nbsp;Dashboard &nbsp;<span class="ok">Running</span></div>
            <div>● &nbsp;Incident data &nbsp;<span class="ok">Loaded</span></div>
            <div>● &nbsp;Remediation engine &nbsp;<span class="ok">Ready</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="footer">CI/CD Intelligence Agent<br>v1.0.0</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# DATA
# ============================================================

incidents = list_incidents()
latest = choose_active(incidents)


# ============================================================
# EMPTY STATE
# ============================================================

if not latest:
    st.markdown('<div class="eyebrow">Engineering Command Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">CI/CD Intelligence Agent</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Autonomous CI failure diagnosis & remediation</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # Landing state: show the full remediation story, but nothing is complete
    # until the user explicitly triggers the test incident.
    st.markdown(
        f"""
        <div class="panel">
            <div class="section-title">Autonomous Remediation Pipeline</div>
            {render_pipeline(-1)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:.65rem'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="status-banner active">
            ◉ SYSTEM READY
            <span>Waiting for a CI failure. Trigger a test incident to start the autonomous remediation loop.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:.65rem'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="panel" style="text-align:center;padding:1.15rem;">
            <div style="font-size:1rem;font-weight:850;">No active incident</div>
            <div class="meta">The pipeline will populate with the incident ID, diagnosis, patch, validation, pull request and CI verification after you trigger the demo.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns([5, 1])

with header_left:
    st.markdown('<div class="eyebrow">Engineering Command Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">CI/CD Intelligence Agent</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Autonomous CI failure diagnosis & remediation</div>',
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown(
        '<div style="text-align:right;margin-top:.25rem;"><span class="live"><span class="dot"></span> System Live</span></div>',
        unsafe_allow_html=True,
    )
    if st.button("↻ Refresh", use_container_width=True):
        st.rerun()


st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)


# ============================================================
# LIVE DEMO AREA
# Only runs after Trigger Test Incident.
# Normal refreshes never replay it.
# ============================================================

running = bool(st.session_state.demo_playing)

pipeline_placeholder = st.empty()
status_placeholder = st.empty()
incident_placeholder = st.empty()

# During the demo, the page visibly progresses through the actual story.
if running:
    for stage in range(6):
        pipeline_placeholder.markdown(
            f"""
            <div class="panel">
                <div class="section-title">Autonomous Remediation Pipeline</div>
                {render_pipeline(stage)}
            </div>
            """,
            unsafe_allow_html=True,
        )

        status_text = [
            ("failed", "● CI FAILURE DETECTED", "The agent has received a failed test run and is collecting evidence."),
            ("active", "◉ ANALYZING INCIDENT", "Logs, failed step and changed files are being inspected."),
            ("active", "◉ GENERATING REMEDIATION", "The agent is producing the smallest supported fix."),
            ("active", "◉ VALIDATING PATCH", "The proposed change is being checked before CI verification."),
            ("active", "◉ SUBMITTING PULL REQUEST", "The remediation change is ready for CI verification."),
            ("active", "◉ VERIFYING CI", "The repaired pipeline is being checked."),
        ][stage]

        status_placeholder.markdown(
            f"""
            <div class="status-banner {status_text[0]}">
                {status_text[1]}
                <span>{status_text[2]}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        incident_placeholder.markdown(
            render_incident_card(latest, running=True),
            unsafe_allow_html=True,
        )

        sleep(.58)

    # Final state remains visible for the normal dashboard render below.
    st.session_state.demo_playing = False
    st.rerun()

# Static final dashboard.
pipeline_placeholder.markdown(
    f"""
    <div class="panel">
        <div class="section-title">Autonomous Remediation Pipeline</div>
        {render_pipeline(6)}
    </div>
    """,
    unsafe_allow_html=True,
)

status_placeholder.markdown(
    """
    <div class="status-banner">
        ✓ REMEDIATION COMPLETE
        <span>The pipeline is healthy again.</span>
    </div>
    """,
    unsafe_allow_html=True,
)

incident_placeholder.markdown(
    render_incident_card(latest),
    unsafe_allow_html=True,
)


# ============================================================
# INVESTIGATION / REMEDIATION / ACTIVITY
# ============================================================

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

investigation_col, remediation_col, activity_col = st.columns(
    [1.25, 1.25, .95],
    gap="large",
)

with investigation_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧠 Agent Investigation</div>', unsafe_allow_html=True)

    st.markdown("<b>Root Cause</b>", unsafe_allow_html=True)
    root = escape(str(
        latest.get("root_cause")
        or latest.get("failure_reason")
        or "Diagnosis not available."
    ))
    st.markdown(f'<div class="root-cause">{root}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:.75rem'></div>", unsafe_allow_html=True)
    st.markdown("<b>Failure Evidence</b>", unsafe_allow_html=True)

    failure_reason = latest.get("failure_reason")
    if failure_reason:
        st.markdown(
            f'<div class="evidence"><strong>CI failure</strong><br>{escape(str(failure_reason))}</div>',
            unsafe_allow_html=True,
        )

    evidence = latest.get("evidence", [])
    if isinstance(evidence, list):
        for item in evidence[:4]:
            if isinstance(item, dict):
                source = escape(str(item.get("source", "Evidence")))
                observation = escape(str(item.get("observation", "")))
                st.markdown(
                    f'<div class="evidence"><strong>{source}</strong><br>{observation}</div>',
                    unsafe_allow_html=True,
                )
            elif item:
                st.markdown(
                    f'<div class="evidence">{escape(str(item))}</div>',
                    unsafe_allow_html=True,
                )

    affected = latest.get("affected_files", [])
    if affected:
        st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="mini-label">Affected Files</div>', unsafe_allow_html=True)
        for file_name in affected[:6]:
            st.code(str(file_name), language=None)

    st.markdown(
        f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:.7rem;">
            <span style="color:#7b8792;font-size:.68rem;">Confidence <b style="color:#fff;">{pct(latest.get("confidence"))}</b></span>
            {risk_badge(latest.get("risk_level"))}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)


with remediation_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🛠 Agent Remediation</div>', unsafe_allow_html=True)

    st.markdown("<b>Proposed Fix</b>", unsafe_allow_html=True)
    fix = escape(str(latest.get("suggested_fix", "No proposed fix available.")))
    st.markdown(f'<div class="fix">{fix}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:.75rem'></div>", unsafe_allow_html=True)

    patch = latest.get("patch") or latest.get("patch_proposal")

    if patch:
        st.markdown("<b>Patch / Change</b>", unsafe_allow_html=True)

        if isinstance(patch, dict):
            explanation = patch.get("explanation")
            if explanation:
                st.caption(str(explanation))

            for change in patch.get("changes", []):
                if isinstance(change, dict):
                    file_path = str(change.get("file_path", "file"))
                    old_text = str(change.get("old_text", ""))
                    new_text = str(change.get("new_text", ""))

                    st.markdown(f"**{escape(file_path)}**")
                    st.code(
                        f"- {old_text}\n+ {new_text}",
                        language="diff",
                    )
        else:
            st.code(str(patch), language="diff")
    else:
        st.markdown(
            """
            <div class="evidence">
                <strong>Minimal-change principle</strong><br>
                The agent proposes the smallest supported change, then validates it before CI verification.
            </div>
            """,
            unsafe_allow_html=True,
        )

    metric_a, metric_b = st.columns(2)

    with metric_a:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Risk</div>
                <div class="metric-value green">{escape(str(latest.get("risk_level", "—")).upper())}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with metric_b:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Confidence</div>
                <div class="metric-value">{pct(latest.get("confidence"))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)


with activity_col:
    st.markdown(
        render_activity_panel(latest, 6),
        unsafe_allow_html=True,
    )


# ============================================================
# HINDSIGHT MEMORY
# ============================================================

hindsight = latest.get("hindsight_recalled", [])

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

st.markdown(
    '<div class="hindsight-card">',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hindsight-title">🧠 Hindsight Memory</div>',
    unsafe_allow_html=True,
)

if hindsight:
    st.markdown(
        f'<div class="hindsight-stat">'
        f'Recalled {len(hindsight)} similar previous incident(s)'
        f'</div>',
        unsafe_allow_html=True,
    )

    for memory in hindsight[:3]:
        run_id = escape(str(memory.get("run_id", "N/A")))
        root_cause = escape(str(memory.get("root_cause", "Unknown")))
        matched = escape(", ".join(memory.get("matched_terms", [])))
        score = memory.get("similarity_score", 0)

        st.markdown(
            f"""
            <div class="hindsight-memory">
                <strong>Previous Run #{run_id}</strong>
                <div class="hindsight-muted">
                    {root_cause}
                </div>
                <div class="hindsight-muted" style="margin-top:.35rem;">
                    Matched: {matched}
                    &nbsp;·&nbsp;
                    Similarity: {score}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="hindsight-muted" style="margin-top:.7rem;">
            Previous incident experience was recalled and supplied
            as historical context for AI diagnosis.
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    st.markdown(
        '<div class="hindsight-stat">No previous memory recalled</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hindsight-muted">
            The agent will retain verified remediation outcomes
            for future incidents.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# PR + PERFORMANCE
# ============================================================

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

pr_col, perf_col = st.columns([2.25, 1], gap="large")

with pr_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⑂ Pull Request</div>', unsafe_allow_html=True)

    if latest.get("pr_url"):
        st.markdown(
            f"""
            <div class="pr-title">AI-generated remediation PR #{escape(str(latest.get("pr_number", "N/A")))}</div>
            <div class="meta">The proposed fix was committed and submitted for CI verification.</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:.65rem'></div>", unsafe_allow_html=True)
        st.link_button("Open Pull Request →", str(latest["pr_url"]))
    else:
        st.markdown(
            '<div class="meta">No pull request is recorded for this incident.</div>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)


with perf_col:
    total = len(incidents)

    passed = sum(
        1
        for item in incidents
        if "PASS" in str(item.get("status", "")).upper()
        or str(item.get("ci_status", "")).lower() in {"success", "passed"}
    )

    avg_conf_values = []

    for item in incidents:
        value = item.get("confidence")
        try:
            value = float(value)
            if value <= 1:
                value *= 100
            avg_conf_values.append(value)
        except (TypeError, ValueError):
            pass

    avg_conf = (
        sum(avg_conf_values) / len(avg_conf_values)
        if avg_conf_values
        else None
    )

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Agent Performance</div>', unsafe_allow_html=True)

    a, b = st.columns(2)

    with a:
        st.markdown(
            f'<div class="metric-box"><div class="metric-label">Incidents</div><div class="metric-value">{total}</div></div>',
            unsafe_allow_html=True,
        )

    with b:
        success_pct = (passed / total * 100) if total else 0
        st.markdown(
            f'<div class="metric-box"><div class="metric-label">CI Success</div><div class="metric-value green">{success_pct:.0f}%</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:.45rem'></div>", unsafe_allow_html=True)

    st.markdown(
        f'<div class="metric-box"><div class="metric-label">Average Confidence</div><div class="metric-value">{f"{avg_conf:.1f}%" if avg_conf is not None else "—"}</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# INCIDENT HISTORY
# ============================================================

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">▣ Incident History</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="history-row history-head">
        <div>Run ID</div>
        <div>Job</div>
        <div>Failure / Root Cause</div>
        <div>Status</div>
        <div>CI</div>
    </div>
    """,
    unsafe_allow_html=True,
)

for incident in incidents[:10]:
    run_id = escape(str(incident.get("run_id", "N/A")))
    job = escape(str(incident.get("job_name", "N/A")))
    root = incident.get("root_cause") or incident.get("failure_reason") or "Unknown"

    root_short = str(root).replace("\n", " ")
    if len(root_short) > 92:
        root_short = root_short[:89] + "..."

    root_short = escape(root_short)

    st.markdown(
        f"""
        <div class="history-row">
            <div class="history-main">#{run_id}</div>
            <div class="history-muted">{job}</div>
            <div class="history-muted">{root_short}</div>
            <div>{badge(incident.get("status"))}</div>
            <div>{badge(incident.get("ci_status"))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">Built with Streamlit · Redis · Kafka · NVIDIA AI · GitHub Actions</div>',
    unsafe_allow_html=True,
)