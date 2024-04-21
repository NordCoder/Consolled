from core.game_state.snake_gamestate.SnakeGameState import SnakeGameState


class AbstractCommand:
    def __init__(self):
        pass

    def execute(self, console):
        pass


class ChangeDirCommand(AbstractCommand):
    def __init__(self, dir_name):
        super().__init__()
        self.dir_name = dir_name

    def execute(self, console):
        for heir in console.current_folder.heirs:
            if heir.name == self.dir_name:
                console.current_folder = heir
                return
        console.create_error(f"There's no folder named {self.dir_name}")


class ListCommand(AbstractCommand):
    def __init__(self):
        super().__init__()

    def execute(self, console):
        list_of_dirs = ""
        for heir in console.current_folder.heirs:
            list_of_dirs += heir.name
            list_of_dirs += " "
        console.create_message("", list_of_dirs)


class ExecuteCommand(AbstractCommand):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def execute(self, console):
        for heir in console.current_folder.heirs:
            if heir.name == self.filename and self.filename == "snake.exe":
                console.write_til_not_down = False
                heir.execute(SnakeGameState(console.game_state.game_state_manager))
                return
        console.create_error(f"{self.filename} is not runnable")


class ErrorCommand(AbstractCommand):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def execute(self, console):
        console.create_error(self.message)
