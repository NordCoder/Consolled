from core.game_state.abstract_game_state import GameState
from core.game_state.snake_gamestate.Snake import Snake


class SnakeGameState(GameState):
    def __init__(self, game_state_manager):
        super().__init__(game_state_manager)
        self.snake_game = Snake(self)

    def update(self):
        self.snake_game.update()

    def render(self, screen):
        self.snake_game.draw_rects(screen)

    def handle_key_input(self, events):
        for event in events:
            self.snake_game.handle_key_input(event)
