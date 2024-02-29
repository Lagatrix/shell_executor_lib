"""Test the command manager."""

import unittest
from unittest import mock

from mock_shell_executor_lib import mock_subprocess_correct, mock_subprocess_error_exit_code, \
    mock_subprocess_invalid_exit_code, mock_subprocess_invalid_outs, mock_asyncio_subprocess, mock_output_data
from shell_executor_lib import CommandError
from shell_executor_lib.manager.command_executor import executor


class TestCommandExecutor(unittest.IsolatedAsyncioTestCase):
    """Test the command executor."""

    async def test_execute_command(self) -> None:
        """Test correctly functioning of command executor."""
        with mock.patch(mock_asyncio_subprocess, return_value=mock_subprocess_correct):
            self.assertEquals(await executor("ls"), mock_output_data)

    async def test_execute_command_with_stdin(self) -> None:
        """Test correctly functioning of command executor with stdin."""
        with mock.patch(mock_asyncio_subprocess, return_value=mock_subprocess_correct):
            self.assertEquals(await executor("ls", "Input data", "Input data", "Input data"), mock_output_data)

    async def test_execute_command_exit_code_error(self) -> None:
        """Test error if the exit status code of the command is not 0."""
        with mock.patch(mock_asyncio_subprocess, return_value=mock_subprocess_error_exit_code):
            with self.assertRaises(CommandError):
                await executor("ls")

    async def test_execute_command_invalid_exit_code_error(self) -> None:
        """Test error if command returns an invalid exit status code."""
        with mock.patch(mock_asyncio_subprocess, return_value=mock_subprocess_invalid_exit_code):
            with self.assertRaises(CommandError):
                await executor("ls")

    async def test_execute_command_invalid_outs(self) -> None:
        """Test error if the command returns invalid stout and stderr."""
        with mock.patch(mock_asyncio_subprocess, return_value=mock_subprocess_invalid_outs):
            with self.assertRaises(CommandError):
                await executor("ls")
