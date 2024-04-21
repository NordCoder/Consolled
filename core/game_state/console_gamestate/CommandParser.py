from core.game_state.console_gamestate.commands import ChangeDirCommand, ListCommand, ExecuteCommand, ErrorCommand


class CommandParser:
    def __init__(self, console):
        self.console = console

    def parse_command(self, string):
        tokens = string.split()
        if len(tokens) > 0:
            if tokens[0] == 'ls':
                return ListCommand()
            if len(tokens) > 1:
                if tokens[0] == 'cd':
                    return ChangeDirCommand(tokens[1])

                if tokens[0] == 'execute':
                    return ExecuteCommand(tokens[1])

        return ErrorCommand(f"There's no command named {string}")
