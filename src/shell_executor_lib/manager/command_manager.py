"""Make commands in the shell."""

from shell_executor_lib import CommandError
from shell_executor_lib.errors import AuthenticationError, PrivilegesError
from shell_executor_lib.manager.command_executor import executor


class CommandManager:
    """Make commands in the shell."""

    @classmethod
    async def init(cls, user: str, password: str) -> 'CommandManager':
        """Initialize the class.

        Args:
            user: The user of the shell who execute command.
            password: The password of the user.

        Returns:
            A CommandManager instance.

        Raises:
            AuthenticationError: If the user authentication fails.
        """
        try:
            await executor(f"/bin/su - {user}", password)

            return cls(user, password)
        except CommandError:
            raise AuthenticationError(user)

    def __init__(self, user: str, password: str) -> None:
        """Initialize the class.

        Args:
            user: The user of the shell who execute command.
            password: The password of the user.
        """
        self.user = user
        self.__password = password

    async def execute_command(self, command: str, sudo: bool = False, *stdin: str) -> list[str]:
        """Execute a command into the shell.

        Args:
            command: The command to execute.
            sudo: If the command require sudo privileges.
            *stdin: Stdin params of the command.

        Returns:
            A list with the response from the command.

        Raises:
            CommandError: If the exit code is not 0.
            PrivilegesError: If the user doesn't have sudo privileges.
        """
        if sudo:
            try:
                return await executor(f"su - {self.user} -c \"sudo -S {command}\"", self.__password,
                                      self.__password, *stdin)
            except CommandError:
                raise PrivilegesError(self.user)

        return await executor(f"su - {self.user} -c \"{command}\"", self.__password, *stdin)
