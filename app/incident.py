from dataclasses import dataclass


@dataclass
class CIIncident:
    run_id: int
    job_id: int
    job_name: str
    conclusion: str
    failed_step: str
    logs: str
    commit_sha: str
    commit_message: str
    author: str
    changed_files: list
    diff: str