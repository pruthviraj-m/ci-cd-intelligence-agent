import subprocess
from pathlib import Path


def validate_change(change, project_root):
    file_path = Path(project_root) / change.file_path

    # 1. File must exist
    if not file_path.exists():
        return False, f"File does not exist: {change.file_path}"

    # 2. Must be a file, not a directory
    if not file_path.is_file():
        return False, f"Not a file: {change.file_path}"

    current_content = file_path.read_text(encoding="utf-8")

    # 3. The old code must actually exist
    if change.old_text not in current_content:
        return False, (
            f"Expected old text was not found in "
            f"{change.file_path}"
        )

    # 4. Prevent accidental multiple replacements
    occurrences = current_content.count(change.old_text)

    if occurrences != 1:
        return False, (
            f"Expected exactly one occurrence, "
            f"but found {occurrences} in {change.file_path}"
        )

    return True, "Change validated successfully."


def apply_change(change, project_root):
    is_valid, message = validate_change(
        change,
        project_root
    )

    if not is_valid:
        file_path = Path(project_root) / change.file_path

        if file_path.exists():
            current_content = file_path.read_text(
                encoding="utf-8"
            )

            # Patch was already applied.
            if change.new_text in current_content:
                return "Patch already applied."

        raise RuntimeError(message)

    file_path = Path(project_root) / change.file_path

    current_content = file_path.read_text(
        encoding="utf-8"
    )

    updated_content = current_content.replace(
        change.old_text,
        change.new_text,
        1
    )

    file_path.write_text(
        updated_content,
        encoding="utf-8"
    )

    return message

def run_tests(project_root):
    result = subprocess.run(
        ["python", "-m", "pytest"],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    return {
        "passed": result.returncode == 0,
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }