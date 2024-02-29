"""Represents an error when the authentication of user fail."""
from shell_executor_lib.errors.command_error import CommandError


class PrivilegesError(CommandError):
    """Represents an error when the user hasn't sudo privileges."""

    def __init__(self, username: str) -> None:
        """Initialize the PrivilegesError exception.

        Attributes:
            username: The username of the user who didn't have sudo privileges.
        """
        super().__init__(1, f"The user {username} doesn't have sudo privileges.")
