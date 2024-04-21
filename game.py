import pygame

import core.utils.constants as consts
from core.game_state.GameStateManager import GameStateManager
from core.game_state.console_gamestate import ConsoleGameState
from core.utils.json_reader_file_system_creation import dump_json


class Game:
    def __init__(self):
        pygame.init()
        display_info = pygame.display.Info()
        self.WINDOW_WIDTH = display_info.current_w - consts.WINDOW_OFFSET
        self.WINDOW_HEIGHT = display_info.current_h - consts.WINDOW_OFFSET
        self.WINDOW = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT),
            pygame.SCALED)
        self.game_state_manager = GameStateManager(self)
        self.game_state_manager.init()
        self.start_main_loop()

    def start_main_loop(self):
        self.run_main_loop()

    def run_main_loop(self):
        clock = pygame.time.Clock()
        while True:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    return
            self.game_state_manager.current_game_state.handle_key_input(events)
            self.game_state_manager.current_game_state.update()
            self.game_state_manager.current_game_state.render(self.WINDOW)

            pygame.display.update()

            clock.tick(consts.FPS_SET)
            pygame.display.set_caption(f"FPS: {clock.get_fps()}")


if __name__ == '__main__':
    game = Game()
