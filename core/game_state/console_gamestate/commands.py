from core.entity.file_system.Folder import Folder
from core.game_state.snake_gamestate.SnakeGameState import SnakeGameState


class AbstractCommand:
    def __init__(self):
        pass

    def execute(self, console):
        pass


class ChangeDirCommand(AbstractCommand):
    def __init__(self, dir_path):
        super().__init__()
        self.dir_path = dir_path
        self.dir_arr = dir_path.split("/")
        self.result_folder = None

    def execute(self, console):
        self.result_folder = console.current_folder
        for folder_name in self.dir_arr:
            check = self.get_next(console, folder_name)
            if check:
                return
        console.current_folder = self.result_folder

    def get_next(self, console, folder_name):
        if folder_name == "..":
            self.result_folder = console.current_folder.parent
            return 0
        for heir in self.result_folder.heirs:
            if (heir.name[:-1] == folder_name or heir.name == folder_name) and isinstance(heir, Folder):
                self.result_folder = heir
                return 0
            if folder_name != "":
                console.create_error(f"There's nothing on path {self.dir_path}")
                return 1


class ListCommand(AbstractCommand):
    def __init__(self):
        super().__init__()

    def execute(self, console):
        list_of_dirs = ""
        for heir in console.current_folder.heirs:
            list_of_dirs += heir.name
            list_of_dirs += " "
        console.create_message("", list_of_dirs, "system")


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
