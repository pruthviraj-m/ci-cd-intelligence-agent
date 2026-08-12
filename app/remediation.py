from app.incident_collector import get_failed_incident
from app.llm_client import diagnose_incident
from app.llm_client import generate_patch
from app.patch_applier import apply_change, run_tests
from app.pr_creator import create_pull_request
from app.ci_verifier import wait_for_ci
from app.state_store import update_incident

import subprocess


def run_remediation(run_id, branch):
    """
    Run the complete CI remediation workflow for one failed run.
    """

    # ============================================================
    # 1. COLLECT INCIDENT
    # ============================================================

    update_incident(
        run_id,
        {
            "status": "COLLECTING",
            "branch": branch,
        },
    )

    incident = get_failed_incident(run_id)

    print("\n========== CI INCIDENT ==========")
    print("Run ID:", incident.run_id)
    print("Job ID:", incident.job_id)
    print("Job:", incident.job_name)
    print("Conclusion:", incident.conclusion)
    print("Failed step:", incident.failed_step)
    print("Commit SHA:", incident.commit_sha)

    # ============================================================
    # 2. AI DIAGNOSIS
    # ============================================================

    update_incident(
        run_id,
        {
            "status": "DIAGNOSING",
        },
    )

    diagnosis = diagnose_incident(incident)

    print("\n========== AI DIAGNOSIS ==========")
    print("Root cause:")
    print(diagnosis.root_cause)

    print("\nSuggested fix:")
    print(diagnosis.suggested_fix)

    print("\nRisk level:")
    print(diagnosis.risk_level)

    print("\nConfidence:")
    print(diagnosis.confidence)

    # ============================================================
    # 3. GENERATE PATCH
    # ============================================================

    update_incident(
        run_id,
        {
            "status": "GENERATING_PATCH",
        },
    )

    patch = generate_patch(
        incident,
        diagnosis,
    )

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

    update_incident(
        run_id,
        {
            "status": "APPLYING_PATCH",
        },
    )

    print("\n========== APPLYING PATCH ==========")

    for change in patch.changes:
        message = apply_change(
            change,
            ".",
        )

        print(message)

    # ============================================================
    # 5. LOCAL VALIDATION
    # ============================================================

    update_incident(
        run_id,
        {
            "status": "VALIDATING_PATCH",
        },
    )

    print("\n========== RUNNING TESTS ==========")

    test_result = run_tests(".")

    print(test_result["stdout"])

    if not test_result["passed"]:
        update_incident(
            run_id,
            {
                "status": "FAILED",
                "failure_reason": "Local tests failed",
            },
        )

        print("PATCH FAILED VALIDATION")
        print(test_result["stderr"])

        raise RuntimeError(
            "Patch failed local tests."
        )

    print("PATCH VALIDATED - ALL TESTS PASSED")

    # ============================================================
    # 6. COMMIT REMEDIATION
    # ============================================================

    print("\n========== COMMITTING REMEDIATION ==========")

    subprocess.run(
        ["git", "add", "-A"],
        check=True,
    )

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            f"AI remediation for CI run {run_id}",
        ],
        check=True,
    )

    print("Remediation patch committed.")

    # ============================================================
    # 7. PUSH REMEDIATION BRANCH
    # ============================================================

    print("\n========== PUSHING REMEDIATION BRANCH ==========")

    subprocess.run(
        [
            "git",
            "push",
            "-u",
            "origin",
            branch,
        ],
        check=True,
    )

    print("Remediation branch pushed:", branch)

    update_incident(
        run_id,
        {
            "status": "PATCH_VALIDATED",
        },
    )

    # ============================================================
    # 8. CREATE PULL REQUEST
    # ============================================================

    update_incident(
        run_id,
        {
            "status": "CREATING_PR",
        },
    )

    print("\n========== CREATING PULL REQUEST ==========")

    pr = create_pull_request(
        branch=branch,
        run_id=run_id,
        diagnosis=diagnosis,
        patch=patch,
    )

    print("Pull request ready.")
    print("PR:", pr["html_url"])

    update_incident(
        run_id,
        {
            "status": "PR_CREATED",
            "pr_number": pr["number"],
            "pr_url": pr["html_url"],
        },
    )

    # ============================================================
    # 9. VERIFY GITHUB CI
    # ============================================================

    update_incident(
        run_id,
        {
            "status": "CI_VERIFYING",
        },
    )

    print("\n========== VERIFYING GITHUB CI ==========")

    ci_run = wait_for_ci(branch)

    if ci_run["conclusion"] != "success":
        update_incident(
            run_id,
            {
                "status": "FAILED",
                "ci_status": ci_run["conclusion"],
            },
        )

        print("GITHUB CI FAILED")
        print("Run:", ci_run["html_url"])

        raise RuntimeError(
            "GitHub CI failed after patch."
        )

    print("GITHUB CI PASSED")
    print("Fix verified by GitHub Actions.")

    update_incident(
        run_id,
        {
            "status": "CI_PASSED",
            "ci_status": "success",
        },
    )

    return {
        "run_id": run_id,
        "branch": branch,
        "pr_number": pr["number"],
        "pr_url": pr["html_url"],
        "ci_status": "success",
        "status": "CI_PASSED",
    }