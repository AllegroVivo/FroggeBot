from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("CorruptedFileError",)

################################################################################
class CorruptedFileError(ErrorMessage):

    def __init__(self, input_file: str):

        super().__init__(
            title="Corrupted Input File",
            message=(
                f"The file provided could not be decoded by the JSON deserializer."
            ),
            solution=f"Please ensure you upload a valid `{input_file}`."
        )

################################################################################
