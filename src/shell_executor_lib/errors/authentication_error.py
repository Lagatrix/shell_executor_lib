"""Represents an error when the authentication of user fail."""
from shell_executor_lib.errors.command_error import CommandError


class AuthenticationError(CommandError):
    """Represents an error when the authentication of user fail."""

    def __init__(self, username: str) -> None:
        """Initialize the AuthenticationError exception.

        Attributes:
            username: The username of the user who auth fails.
        """
        super().__init__(1, f"Authentication failed with user {username}")
