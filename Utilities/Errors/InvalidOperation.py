from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("InvalidOperationError",)

################################################################################
class InvalidOperationError(ErrorMessage):

    def __init__(self, operation: str):

        super().__init__(
            title="Invalid Operation",
            message=f"You attempted to perform an invalid operation: `{operation}`.",
            solution=f"Please check the documentation for the correct operation."
        )

################################################################################
