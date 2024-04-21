import pygame

from core.game_state.abstract_game_state import GameState
from core.game_state.console_gamestate.Console import Console

BACKGROUND = (8, 8, 8)


class ConsoleGameState(GameState):
    def __init__(self, c_folder, game_state_manager):
        super().__init__(game_state_manager)
        self.console = Console(c_folder, self)

    def update(self):
        self.console.update()

    def render(self, screen):
        screen.fill(BACKGROUND)
        self.console.draw_text(screen)

    def handle_key_input(self, events):
        for event in events:
            self.console.type(event)
