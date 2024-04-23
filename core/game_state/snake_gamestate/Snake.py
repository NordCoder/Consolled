import pygame, sys, random
from pygame.locals import *

BACKGROUND = (255, 255, 255)

BLOCK_WIDTH = 60
YAMMIE_WIDTH = 60


class Block:  # class Block
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"


class Snake:
    def __init__(self, game_state):
        self.window_width = game_state.game_state_manager.game.WINDOW_WIDTH
        self.window_height = game_state.game_state_manager.game.WINDOW_HEIGHT
        self.direction = [0, 1]
        self.block_stack = []
        self.init_block = Block(300, 300)
        self.block_stack.append(self.init_block)
        self.tick_time = 5
        self.tick = 0
        self.yammie = self.generate_yammie()
        self.key_cooldown = False
        self.check_collision_cooldown = False
        self.game_state = game_state

    def draw_rects(self, screen):
        screen.fill(BACKGROUND)
        rects = self.block_stack
        for mrect in rects:
            pygame.draw.rect(screen, (0, 0, 0), [mrect.x, mrect.y, BLOCK_WIDTH, BLOCK_WIDTH], 0)
        pygame.draw.rect(screen, (255, 255, 255), [rects[0].x + BLOCK_WIDTH / 2, rects[0].y + BLOCK_WIDTH / 2, 10, 10],
                         0)
        pygame.draw.rect(screen, (255, 0, 0), [self.yammie.x, self.yammie.y, YAMMIE_WIDTH, YAMMIE_WIDTH], 0)

    def generate_yammie(self, ):
        x = random.randint(10, self.window_width - YAMMIE_WIDTH)
        y = random.randint(10, self.window_height - YAMMIE_WIDTH)
        return Block(x, y)

    def move_snake(self, block_stack, direction):
        delta_x = block_stack[0].x + direction[0] * BLOCK_WIDTH
        delta_y = block_stack[0].y + direction[1] * BLOCK_WIDTH
        new_head = block_stack.pop()
        new_head.x = delta_x
        new_head.y = delta_y
        block_stack.insert(0, new_head)

    def check_yammie_collision(self, head, yammie):
        return pygame.Rect(head.x, head.y, BLOCK_WIDTH, BLOCK_WIDTH).colliderect(
            pygame.Rect(yammie.x, yammie.y, BLOCK_WIDTH, BLOCK_WIDTH))

    def check_two_block_collision(self, b1, b2):
        return b1.x == b2.x and b1.y == b2.y

    def check_collisions(self, block_stack):
        head = block_stack[0]
        for i in range(1, len(block_stack)):
            if self.check_two_block_collision(head, block_stack[i]):
                return True
        if head.x < 0 or head.x >= self.window_width or head.y < 0 or head.y >= self.window_height:
            return True
        return False

    def update(self):
        if self.tick % self.tick_time == 0:
            self.move_snake(self.block_stack, self.direction)
            self.key_cooldown = False
            self.check_collision_cooldown = False
        if self.check_yammie_collision(self.block_stack[0], self.yammie):
            self.yammie = self.generate_yammie()
            to_add = Block(self.block_stack[-1].x, self.block_stack[-1].y)
            self.block_stack.insert(-1, to_add)
            self.check_collision_cooldown = True
        if self.check_collisions(self.block_stack) and not self.check_collision_cooldown:
            self.game_state.game_state_manager.get_back_to_console()
        self.tick += 1

    def handle_key_input(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if self.direction != [1, 0] and not self.key_cooldown:
                    self.direction = [-1, 0]
            elif event.key == K_RIGHT:
                if self.direction != [-1, 0] and not self.key_cooldown:
                    self.direction = [1, 0]
            elif event.key == K_UP:
                if self.direction != [0, 1] and not self.key_cooldown:
                    self.direction = [0, -1]
            elif event.key == K_DOWN:
                if self.direction != [0, -1] and not self.key_cooldown:
                    self.direction = [0, 1]
            self.key_cooldown = True
