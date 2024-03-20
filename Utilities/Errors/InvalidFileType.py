from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("InvalidFileTypeError",)

################################################################################
class InvalidFileTypeError(ErrorMessage):

    def __init__(self, expected_type: str):

        super().__init__(
            title="Invalid File Type",
            message=f"The file provided is not of type `{expected_type}`.",
            solution=(
                f"Please ensure you upload a valid `{expected_type}` file at "
                "the prompt."
            )
        )

################################################################################
