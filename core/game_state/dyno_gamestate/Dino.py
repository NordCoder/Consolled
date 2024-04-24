import pygame.draw
from enum import Enum
import random


class DinoState(Enum):
    WAITING = 0
    RUNNING = 1
    BRO_DEAD = 2


def split_sprites(path, num_of_sprites):
    sprite_sheet = pygame.image.load(path)
    length, height = sprite_sheet.get_size()
    width = length / num_of_sprites
    result = []
    for i in range(int(length / width)):
        rect = pygame.Rect(i * width, 0, width, height)
        result.append(sprite_sheet.subsurface(rect))
    return result


def rescale(sprite_array, size):
    rescaled = []
    for sprite in sprite_array:
        rescaled.append(pygame.transform.scale(sprite, size))
    return rescaled


BACKGROUND = (245, 245, 245)
OBSTACLE_COLOR = (10, 10, 10)
TICKS_OBSTACLE_COOLDOWN = 200
TICKS_TO_RAISE_SPEED = 200
TICKS_TO_CHANGE_DINO = 10
DINO_SIZE = (100, 100)
BIRDIE_SIZE = (100, 100)
INIT_SPEED = 20
DINO_X = 30
CACTUS_WIDTH = 70
CACTUS_HEIGHT = 200


class Obstacle:
    def __init__(self, x, y, width, height, type):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.type = type

    def move(self, speed):
        self.x -= speed

    def draw_width_sprite(self, screen, sprite):
        sprite_width, sprite_height = sprite.get_size()
        if sprite_width != self.width or sprite_height != self.height:
            sprite = pygame.transform.scale(sprite, (self.width, self.height))
        screen.blit(sprite, (self.x, self.y))

    def check_collision(self, rect):
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(rect)

    def draw_simple(self, screen):
        pygame.draw.rect(screen, OBSTACLE_COLOR, [self.x, self.y, self.width, self.height], 0)


class Dino:
    def __init__(self, gamestate):
        self.gamestate = gamestate
        self.screen_width = gamestate.game_state_manager.game.WINDOW_WIDTH
        self.screen_height = gamestate.game_state_manager.game.WINDOW_HEIGHT
        self.sprites = rescale(split_sprites("resources/sprites/dyno-sprites.png", 6), DINO_SIZE)
        self.cur_tick = 0
        self.speed = INIT_SPEED
        self.y_dyno_velocity = 0
        self.y_dyno_velocity_decay = 0
        self.obstacles_array = []
        self.animation_index = 3
        self.is_jumping = False
        self.dino = self.sprites[0]
        self.dino_y = self.screen_height - self.screen_height / 8 - 10
        self.dyno_state = DinoState.WAITING
        self.obstacle_array = []

    def get_dino_normal_pos(self):
        return self.screen_height - self.screen_height / 8 - 10

    def update(self):
        if self.dyno_state == DinoState.RUNNING:
            if self.cur_tick % TICKS_OBSTACLE_COOLDOWN == 0:
                cactus_or_birdie = random.randint(0, 1)
                if cactus_or_birdie:
                    self.create_birdie(random.randint(1, 3))
                else:
                    self.create_cactus(random.randint(1, 3))
                self.cur_tick = 0

            for obstacle in self.obstacle_array:
                obstacle.move(self.speed)
                if obstacle.x + obstacle.width < 0:
                    self.obstacle_array.remove(obstacle)

            for obstacle in self.obstacle_array:
                if obstacle.check_collision(pygame.Rect(DINO_X, self.dino_y, DINO_SIZE[0], DINO_SIZE[1])):
                    self.dyno_state = DinoState.BRO_DEAD

            if self.cur_tick % TICKS_TO_CHANGE_DINO == 0:
                self.animation_index = 2 if self.animation_index == 3 else 3

            if self.cur_tick % TICKS_TO_RAISE_SPEED == 0:
                self.speed += 1

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
        elif self.dyno_state == DinoState.BRO_DEAD:
            self.dino = self.sprites[4]
            self.dino_y += 3
            if self.dino_y > self.screen_height:
                self.gamestate.game_state_manager.get_back_to_console()

    def render(self, screen):
        screen.fill(BACKGROUND)
        pygame.draw.line(screen, OBSTACLE_COLOR, (0, self.screen_height - self.screen_height / 8),
                         (self.screen_width, self.screen_height - self.screen_height / 8), 3)
        for obstacle in self.obstacle_array:
            obstacle.draw_simple(screen)
        screen.blit(self.dino, (DINO_X, self.dino_y))

    def handle_key_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.is_jumping:
                if self.dyno_state == DinoState.WAITING:
                    self.dyno_state = DinoState.RUNNING
                self.y_dyno_velocity = -23
                self.is_jumping = True

    def create_birdie(self, level):
        self.obstacle_array.append(
            Obstacle(self.screen_width + 10, (self.get_dino_normal_pos() + DINO_SIZE[1]) - level * BIRDIE_SIZE[1],
                     BIRDIE_SIZE[0],
                     BIRDIE_SIZE[1], "birdie"))

    def create_cactus(self, num):
        for i in range(num):
            height = random.randint(CACTUS_HEIGHT // 2, CACTUS_HEIGHT)
            self.obstacle_array.append(
                Obstacle(self.screen_width + 10 + i * CACTUS_WIDTH, self.get_dino_normal_pos() + DINO_SIZE[1] - height,
                         CACTUS_WIDTH,
                         height, "cactus"))
