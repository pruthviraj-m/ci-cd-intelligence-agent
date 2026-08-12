from pydantic import BaseModel, Field


class Evidence(BaseModel):
    source: str = Field(
        description="Where this evidence came from, such as CI logs, commit diff, or commit message."
    )

    observation: str = Field(
        description="The exact factual observation supported by the evidence."
    )


class Diagnosis(BaseModel):
    root_cause: str = Field(
        description="The most likely technical root cause."
    )

    evidence: list[Evidence] = Field(
        description="Evidence directly supporting the root cause."
    )

    affected_files: list[str] = Field(
        description="Files directly changed or implicated by the failure."
    )

    suggested_fix: str = Field(
        description="Concrete fix that should resolve the failure."
    )

    confidence: float = Field(
        description="Confidence between 0.0 and 1.0."
    )

    risk_level: str = Field(
        description="Risk of applying the suggested fix: low, medium, or high."
    )