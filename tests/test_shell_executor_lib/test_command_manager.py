"""Test the command manager."""

import unittest
from unittest import mock

from mock_shell_executor_lib import mock_subprocess_correct, mock_subprocess_error_exit_code, \
    mock_subprocess_invalid_exit_code, mock_subprocess_invalid_outs
from shell_executor_lib import CommandManager, CommandError


class MockCommandManager(unittest.IsolatedAsyncioTestCase):
    """Test the command manager."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.command_manager = CommandManager("augusto", "augusto")

    async def test_execute_command(self) -> None:
        """Test correctly functioning of command manager."""
        with mock.patch('asyncio.create_subprocess_shell', return_value=mock_subprocess_correct):
            self.assertEquals(await self.command_manager.execute_command("ls", True),
                              ["Output data", "Output data", "Output data"])

    async def test_execute_command_with_stdin(self) -> None:
        """Test correctly functioning of command manager with stdin."""
        with mock.patch('asyncio.create_subprocess_shell', return_value=mock_subprocess_correct):
            self.assertEquals(await self.command_manager.execute_command("ls", True, "Input data",
                                                                         "Input data", "Input data"),
                              ["Output data", "Output data", "Output data"])

    async def test_execute_command_exit_code_error(self) -> None:
        """Test error on exit status code of command manager."""
        with mock.patch('asyncio.create_subprocess_shell', return_value=mock_subprocess_error_exit_code):
            with self.assertRaises(CommandError):
                await self.command_manager.execute_command("ls", False)

    async def test_execute_command_invalid_exit_code_error(self) -> None:
        """Test error an invalid exit status code of command manager."""
        with mock.patch('asyncio.create_subprocess_shell', return_value=mock_subprocess_invalid_exit_code):
            with self.assertRaises(CommandError):
                await self.command_manager.execute_command("ls", True)

    async def test_execute_command_invalid_outs(self) -> None:
        """Test error invalid stout and stderr of command manager."""
        with mock.patch('asyncio.create_subprocess_shell', return_value=mock_subprocess_invalid_outs):
            with self.assertRaises(CommandError):
                await self.command_manager.execute_command("ls", True)
