"""Test the CommandManager."""
import unittest
from unittest import mock

from mock_shell_executor_lib import mock_asyncio_subprocess, mock_subprocess_correct, mock_output_data, \
    mock_subprocess_error_exit_code
from shell_executor_lib import CommandManager, PrivilegesError, AuthenticationError


class TestCommandManager(unittest.IsolatedAsyncioTestCase):
    """Test the CommandManager."""

    async def test_execute_command(self) -> None:
        """Test correctly when execute a command."""
        with mock.patch(mock_asyncio_subprocess, side_effect=(mock_subprocess_correct, mock_subprocess_correct)):
            self.assertEqual(await (await CommandManager.init("augusto", "augusto"))
                             .execute_command("ls", False), mock_output_data)

    async def test_user_or_password_not_valid(self) -> None:
        """Test error if the user or password is not valid."""
        with mock.patch(mock_asyncio_subprocess, return_value=mock_subprocess_error_exit_code):
            with self.assertRaises(AuthenticationError):
                await CommandManager.init("augusto", "augusto")

    async def test_execute_command_with_privileges(self) -> None:
        """Test correctly when execute a command with privileges."""
        with mock.patch(mock_asyncio_subprocess, side_effect=(mock_subprocess_correct, mock_subprocess_correct)):
            self.assertEqual(await (await CommandManager.init("augusto", "augusto"))
                             .execute_command("ls", True), mock_output_data)

    async def test_execute_command_with_privileges_error(self) -> None:
        """Test error if the user does not have privileges."""
        with mock.patch(mock_asyncio_subprocess, side_effect=(mock_subprocess_correct,
                                                              mock_subprocess_error_exit_code)):
            with self.assertRaises(PrivilegesError):
                await (await CommandManager.init("augusto", "augusto")).execute_command("ls", True)
