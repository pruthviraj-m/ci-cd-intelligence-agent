# from app.incident_collector import get_failed_incident
# from app.llm_client import diagnose_incident
# from app.llm_client import generate_patch
# from app.patch_applier import apply_change, run_tests
# from app.pr_creator import create_pull_request
# from app.ci_verifier import wait_for_ci


# import subprocess

# RUN_ID = 31593832847


# incident = get_failed_incident(RUN_ID)
# diagnosis = diagnose_incident(incident)
# patch = generate_patch(incident, diagnosis)

# print("\n========== CHANGED FILES ==========")

# for file in incident.changed_files:
#     print(
#         f"{file['filename']} | "
#         f"{file['status']} | "
#         f"+{file['additions']} "
#         f"-{file['deletions']}"
#     )

# print("\n========== DIFF ==========")
# print(incident.diff)

# print("========== CI INCIDENT ==========")
# print("Run ID:", incident.run_id)
# print("Job ID:", incident.job_id)
# print("Job:", incident.job_name)
# print("Conclusion:", incident.conclusion)
# print("Failed step:", incident.failed_step)

# print("Commit SHA:", incident.commit_sha)
# print("Commit message:", incident.commit_message)
# print("Author:", incident.author)

# print("\n========== LOGS ==========")
# print(incident.logs)

# print("\n========== AI DIAGNOSIS ==========")

# print("Root cause:")
# print(diagnosis.root_cause)

# print("\nEvidence:")

# for evidence in diagnosis.evidence:
#     print(f"- [{evidence.source}] {evidence.observation}")

# print("\nRisk level:")
# print(diagnosis.risk_level)


# print("\nAffected files:")

# for file in diagnosis.affected_files:
#     print("-", file)

# print("\nSuggested fix:")
# print(diagnosis.suggested_fix)

# print("\nConfidence:")
# print(diagnosis.confidence)

# print("\n========== PATCH PROPOSAL ==========")

# print(patch.explanation)

# for change in patch.changes:
#     print("\nFile:", change.file_path)
#     print("OLD:")
#     print(change.old_text)
#     print("NEW:")
#     print(change.new_text)

#     print("\n========== APPLYING PATCH ==========")

# for change in patch.changes:
#     message = apply_change(
#         change,
#         "."
#     )

#     print(message)

# print("\n========== RUNNING TESTS ==========")

# test_result = run_tests(".")

# print(test_result["stdout"])

# if test_result["passed"]:
#     print("✅ PATCH VALIDATED — ALL TESTS PASSED")
# else:
#     print("❌ PATCH FAILED VALIDATION")
#     print(test_result["stderr"])

# # if test_result["passed"]:
# #     print("\n========== COMMITTING FIX ==========")

# #     subprocess.run(
# #         ["git", "add", "app/calculator.py"],
# #         check=True
# #     )

# #     subprocess.run(
# #         [
# #             "git",
# #             "commit",
# #             "-m",
# #             f"Fix CI failure for run {RUN_ID}"
# #         ],
# #         check=True
# #     )

# #     subprocess.run(
# #         [
# #             "git",
# #             "push",
# #             "-u",
# #             "origin",
# #             "agent/fix-31593832847"
# #         ],
# #         check=True
# #     )

# #     print("✅ Fix committed and pushed.")
# # else:
# #     print("❌ Tests failed. Fix will NOT be committed.")


# print("\n========== CREATING PULL REQUEST ==========")

# pr = create_pull_request(
#     branch="agent/fix-31593832847",
#     run_id=RUN_ID,
#     diagnosis=diagnosis,
#     patch=patch,
# )

# print("✅ Pull request created.")
# print("PR:", pr["html_url"])
# print("\n========== VERIFYING GITHUB CI ==========")

# ci_run = wait_for_ci(
#     "agent/fix-31593832847"
# )

# if ci_run["conclusion"] == "success":
#     print("✅ GITHUB CI PASSED")
#     print("Fix verified by GitHub Actions.")
# else:
#     print("❌ GITHUB CI FAILED")
#     print("Fix was not verified.")
#     print("Run:", ci_run["html_url"])


from app.incident_collector import (
    get_failed_incident,
    find_latest_failed_run,
)
from app.llm_client import diagnose_incident
from app.llm_client import generate_patch
from app.patch_applier import apply_change, run_tests
from app.pr_creator import create_pull_request
from app.ci_verifier import wait_for_ci


failed_run = find_latest_failed_run()

RUN_ID = failed_run["id"]
BRANCH = failed_run["head_branch"]

print("Latest failed run:", RUN_ID)

incident = get_failed_incident(RUN_ID)


# ============================================================
# 1. COLLECT INCIDENT
# ============================================================

incident = get_failed_incident(RUN_ID)

print("\n========== CI INCIDENT ==========")
print("Run ID:", incident.run_id)
print("Job ID:", incident.job_id)
print("Job:", incident.job_name)
print("Conclusion:", incident.conclusion)
print("Failed step:", incident.failed_step)
print("Commit SHA:", incident.commit_sha)
print("Commit message:", incident.commit_message)
print("Author:", incident.author)


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


print("\n========== LOGS ==========")
print(incident.logs)


# ============================================================
# 2. AI DIAGNOSIS
# ============================================================

diagnosis = diagnose_incident(incident)

print("\n========== AI DIAGNOSIS ==========")

print("Root cause:")
print(diagnosis.root_cause)

print("\nEvidence:")

for evidence in diagnosis.evidence:
    print(
        f"- [{evidence.source}] "
        f"{evidence.observation}"
    )

print("\nRisk level:")
print(diagnosis.risk_level)

print("\nAffected files:")

for file in diagnosis.affected_files:
    print("-", file)

print("\nSuggested fix:")
print(diagnosis.suggested_fix)

print("\nConfidence:")
print(diagnosis.confidence)


# ============================================================
# 3. GENERATE PATCH
# ============================================================

patch = generate_patch(incident, diagnosis)

print("\n========== PATCH PROPOSAL ==========")

print(patch.explanation)

for change in patch.changes:
    print("\nFile:", change.file_path)
    print("OLD:")
    print(change.old_text)
    print("NEW:")
    print(change.new_text)


# ============================================================
# 4. APPLY PATCH
# ============================================================

print("\n========== APPLYING PATCH ==========")

for change in patch.changes:
    message = apply_change(
        change,
        "."
    )

    print(message)


# ============================================================
# 5. RUN LOCAL TESTS
# ============================================================

print("\n========== RUNNING TESTS ==========")

test_result = run_tests(".")

print(test_result["stdout"])

if not test_result["passed"]:
    print("❌ PATCH FAILED VALIDATION")
    print(test_result["stderr"])
    raise RuntimeError("Patch failed local tests.")

print("✅ PATCH VALIDATED — ALL TESTS PASSED")


# ============================================================
# 6. CREATE PULL REQUEST
# ============================================================

print("\n========== CREATING PULL REQUEST ==========")

pr = create_pull_request(
    branch=BRANCH,
    run_id=RUN_ID,
    diagnosis=diagnosis,
    patch=patch,
)

print("✅ Pull request ready.")
print("PR:", pr["html_url"])


# ============================================================
# 7. VERIFY GITHUB CI
# ============================================================

print("\n========== VERIFYING GITHUB CI ==========")

ci_run = wait_for_ci(BRANCH)

if ci_run["conclusion"] == "success":
    print("✅ GITHUB CI PASSED")
    print("Fix verified by GitHub Actions.")
else:
    print("❌ GITHUB CI FAILED")
    print("Fix was not verified.")
    print("Run:", ci_run["html_url"])
    raise RuntimeError("GitHub CI failed after patch.")