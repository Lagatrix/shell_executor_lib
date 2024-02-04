"""Mocks of the async process."""
from unittest.mock import AsyncMock

mock_subprocess_correct = AsyncMock()
mock_subprocess_correct.stdout.read.return_value = b"Output data\nOutput data\nOutput data"
mock_subprocess_correct.stderr.read.return_value = b""
mock_subprocess_correct.returncode = 0

mock_subprocess_error_exit_code = AsyncMock()
mock_subprocess_error_exit_code.stdout.read.return_value = b"Output data\nOutput data\nOutput data"
mock_subprocess_error_exit_code.stderr.read.return_value = b""
mock_subprocess_error_exit_code.returncode = 1

mock_subprocess_invalid_exit_code = AsyncMock()
mock_subprocess_invalid_exit_code.stdout.read.return_value = b"Output data\nOutput data\nOutput data"
mock_subprocess_invalid_exit_code.stderr.read.return_value = b""
mock_subprocess_invalid_exit_code.returncode = None

mock_subprocess_invalid_outs = AsyncMock()
mock_subprocess_invalid_outs.stdout = None
mock_subprocess_invalid_outs.stderr = None
mock_subprocess_invalid_outs.returncode = 0
