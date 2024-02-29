"""This module contains functions to execute a command into the shell."""
import asyncio
from asyncio.subprocess import Process

from shell_executor_lib import CommandError


async def executor(command: str, *stdin: str) -> list[str]:
    """Execute a command into the shell.

    Args:
        command: The command to execute.
        *stdin: Stdin params of the command.

    Returns:
        A list with the response from the command.

    Raises:
        CommandError: If the exit code is not 0.
    """
    process = await asyncio.create_subprocess_shell(
        command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    await set_stdin(process, *stdin)

    if process.stdout and process.stderr is not None:
        output, error = await asyncio.gather(process.stdout.read(), process.stderr.read())
        await process.wait()

        if isinstance(process.returncode, int):
            if process.returncode != 0:
                raise CommandError(int(process.returncode), error.decode())
            return output.decode().rstrip().split("\n")

        raise CommandError(-1, "Not valid exit status")
    else:
        raise CommandError(-2, "Stdout and stderr read error")


async def set_stdin(process: Process, *stdin: str) -> None:
    """Put the stdin data into the command.

    Args:
        process: The process of the command to exec.
        *stdin: Stdin params of the command.
    """
    if process.stdin is not None:
        for param in stdin:
            process.stdin.write(param.encode() + b"\n")
            await process.stdin.drain()
        process.stdin.write_eof()
