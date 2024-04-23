import pygame

from core.game_state.abstract_game_state import GameState
from core.game_state.dyno_gamestate.Dino import Dino


class DynoGameState(GameState):
    def __init__(self, game_state_manager):
        super().__init__(game_state_manager)
        self.dyno_game = Dino(self)

    def update(self):
        self.dyno_game.update()

    def render(self, screen):
        self.dyno_game.render(screen)

    def handle_key_input(self, events):
        for event in events:
            self.dyno_game.handle_key_input(event)
