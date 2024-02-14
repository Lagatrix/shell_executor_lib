"""Make commands in the shell."""

import asyncio
from asyncio.subprocess import Process
from shell_executor_lib import CommandError


class CommandManager:
    """Make commands in the shell."""

    def __init__(self, user: str, password: str) -> None:
        """Initialize the class.

        Args:
            user: The user of the shell who execute command.
            password: The password of the user.
        """
        self.user = user
        self.password = password

    async def execute_command(self, command: str, sudo: bool, *stdin: str) -> list[str]:
        """Execute a command into the shell.

        Args:
            command: The command to execute.
            sudo: If the command require sudo privileges.
            *stdin: Stdin params of the command.

        Returns:
            A list with the response from the command.

        Raises:
            CommandError: If the exit code is not 0.

        """
        process = await asyncio.create_subprocess_shell(
            f"su - {self.user} -c {'/bin/sudo -S ' if sudo else ''}{command}",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        await self.__set_stdin(process, sudo, *stdin)

        if process.stdout and process.stderr is not None:
            output, error = await asyncio.gather(process.stdout.read(), process.stderr.read())

            if isinstance(process.returncode, int):
                if process.returncode != 0:
                    raise CommandError(int(process.returncode), error.decode())
                return output.decode().split("\n")

            raise CommandError(-1, "Not valid exit status")
        else:
            raise CommandError(-2, "Stdout and stderr read error")

    async def __set_stdin(self, process: Process, sudo: bool, *stdin: str) -> None:
        """Put the stdin data into the command.

        Args:
            process: The process of the command to exec.
            sudo: If the command require sudo privileges.
            *stdin: Stdin params of the command.
        """
        if process.stdin is not None:
            process.stdin.write(self.password.encode() + b"\n")
            await process.stdin.drain()

            if sudo:
                process.stdin.write(self.password.encode() + b"\n")
                await process.stdin.drain()

            for param in stdin:
                process.stdin.write(param.encode() + b"\n")
                await process.stdin.drain()
