"""Represents an error response of shell command."""


class CommandError(Exception):
    """Represents an error when attempting to manage a nonexistent group."""

    def __init__(self, status_code: int, response: str) -> None:
        """Initialize the CommandError exception.

        Attributes:
            status_code: The exit status of the command
            response: Error message.
        """
        self.status_code = status_code
        self.response = response
        super().__init__(self.response)
