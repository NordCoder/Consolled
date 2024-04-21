from core.game_state.console_gamestate.ConsoleGameState import ConsoleGameState
from core.utils.json_reader_file_system_creation import dump_json


class GameStateManager:
    def __init__(self, game):
        self.game = game
        self.current_game_state = None
        self.console_game_state = None

    def init(self):
        self.console_game_state = ConsoleGameState(dump_json(self), self)
        self.current_game_state = self.console_game_state

    def get_back_to_console(self):
        self.current_game_state = self.console_game_state

    def set_game_state(self, game_state):
        self.current_game_state = game_state
