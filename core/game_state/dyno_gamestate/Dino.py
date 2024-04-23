import pygame.draw


def split_sprites(path, num_of_sprites):
    sprite_sheet = pygame.image.load(path)
    length, height = sprite_sheet.get_size()
    width = length / num_of_sprites
    result = []
    for i in range(int(length / width)):
        rect = pygame.Rect(i * width, 0, width, height)
        result.append(sprite_sheet.subsurface(rect))
    return result


BACKGROUND = (245, 245, 245)
TICKS_TO_RAISE_SPEED = 200
TICKS_TO_CHANGE_DINO = 10


class Dino:
    def __init__(self, gamestate):
        self.screen_width = gamestate.game_state_manager.game.WINDOW_WIDTH
        self.screen_height = gamestate.game_state_manager.game.WINDOW_HEIGHT
        self.sprites = split_sprites("resources/sprites/dyno-sprites.png", 6)
        self.cur_tick = 0
        self.speed = 20
        self.y_dyno_velocity = 0
        self.y_dyno_velocity_decay = 0
        self.obstacles_array = []
        self.animation_index = 3
        self.is_jumping = False
        self.dino = self.sprites[self.animation_index]
        self.dino_x = 20
        self.dino_y = self.screen_height - self.screen_height / 8 - 10

    def get_dino_normal_pos(self):
        return self.screen_height - self.screen_height / 8 - 10

    def update(self):
        if self.cur_tick % TICKS_TO_CHANGE_DINO == 0:
            self.animation_index = 2 if self.animation_index == 3 else 3
        print(self.cur_tick)

        if self.cur_tick % TICKS_TO_RAISE_SPEED == 0:
            self.speed += 10
            self.cur_tick = 0

        if self.is_jumping:
            self.dino_y += self.y_dyno_velocity
            self.y_dyno_velocity += self.y_dyno_velocity_decay
            if self.y_dyno_velocity < 0:
                self.y_dyno_velocity_decay += 0.1
            if self.dino_y >= self.get_dino_normal_pos():
                self.dino_y = self.get_dino_normal_pos()
                self.y_dyno_velocity_decay = 0
                self.y_dyno_velocity = 0
                self.is_jumping = False
        self.dino = self.sprites[self.animation_index]
        self.cur_tick += 1

    def render(self, screen):
        screen.fill(BACKGROUND)
        pygame.draw.line(screen, (0, 0, 0), (0, self.screen_height - self.screen_height / 8),
                         (self.screen_width, self.screen_height - self.screen_height / 8), 3)
        screen.blit(self.dino, (self.dino_x, self.dino_y))

    def handle_key_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.y_dyno_velocity = -20
                self.is_jumping = True
