"""Represents an error response of shell command."""

from dataclasses import dataclass


@dataclass
class CommandError(Exception):
    """Represents an error response of shell command.

    Attributes:
        status_code: The exit status of the command
        response: Error message.
    """
    status_code: int
    response: str
