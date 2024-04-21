import pygame


class GameState:
    def __init__(self, game_state_manager):
        self.game_state_manager = game_state_manager

    def update(self):
        pass

    def render(self, screen):
        pass

    def handle_key_input(self, events):
        pass
