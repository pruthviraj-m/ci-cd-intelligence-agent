from app.incident_collector import get_failed_incident
from app.llm_client import diagnose_incident
from app.llm_client import generate_patch
from app.patch_applier import apply_change, run_tests


RUN_ID = 31593832847


incident = get_failed_incident(RUN_ID)
diagnosis = diagnose_incident(incident)
patch = generate_patch(incident, diagnosis)

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

print("========== CI INCIDENT ==========")
print("Run ID:", incident.run_id)
print("Job ID:", incident.job_id)
print("Job:", incident.job_name)
print("Conclusion:", incident.conclusion)
print("Failed step:", incident.failed_step)

print("Commit SHA:", incident.commit_sha)
print("Commit message:", incident.commit_message)
print("Author:", incident.author)

print("\n========== LOGS ==========")
print(incident.logs)

print("\n========== AI DIAGNOSIS ==========")

print("Root cause:")
print(diagnosis.root_cause)

print("\nEvidence:")

for evidence in diagnosis.evidence:
    print(f"- [{evidence.source}] {evidence.observation}")

print("\nRisk level:")
print(diagnosis.risk_level)


print("\nAffected files:")

for file in diagnosis.affected_files:
    print("-", file)

print("\nSuggested fix:")
print(diagnosis.suggested_fix)

print("\nConfidence:")
print(diagnosis.confidence)

print("\n========== PATCH PROPOSAL ==========")

print(patch.explanation)

for change in patch.changes:
    print("\nFile:", change.file_path)
    print("OLD:")
    print(change.old_text)
    print("NEW:")
    print(change.new_text)

    print("\n========== APPLYING PATCH ==========")

for change in patch.changes:
    message = apply_change(
        change,
        "."
    )

    print(message)

print("\n========== RUNNING TESTS ==========")

test_result = run_tests(".")

print(test_result["stdout"])

if test_result["passed"]:
    print("✅ PATCH VALIDATED — ALL TESTS PASSED")
else:
    print("❌ PATCH FAILED VALIDATION")
    print(test_result["stderr"])