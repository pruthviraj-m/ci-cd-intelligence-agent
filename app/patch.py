from pydantic import BaseModel, Field


class FileChange(BaseModel):
    file_path: str = Field(
        description="Path of the file to modify."
    )

    old_text: str = Field(
        description="Exact text currently present in the file that should be replaced."
    )

    new_text: str = Field(
        description="Replacement text."
    )


class PatchProposal(BaseModel):
    explanation: str = Field(
        description="Why this change should fix the CI failure."
    )

    changes: list[FileChange] = Field(
        description="Exact file changes required to fix the failure."
    )