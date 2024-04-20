import pygame, sys, random
from pygame.locals import *

pygame.init()

BACKGROUND = (255, 255, 255)

FPS = 60
fpsClock = pygame.time.Clock()  # need for main loop

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

BLOCK_WIDTH = 30
YAMMIE_WIDTH = 30

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # create window
pygame.display.set_caption('Carl = Plumber!')


class Block:  # class Block
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"


def draw_rects(rects, yammie):
    for mrect in rects:
        pygame.draw.rect(WINDOW, (0, 0, 0), [mrect.x, mrect.y, BLOCK_WIDTH, BLOCK_WIDTH], 0)
    pygame.draw.rect(WINDOW, (255, 255, 255), [rects[0].x + BLOCK_WIDTH / 2, rects[0].y + BLOCK_WIDTH / 2, 10, 10], 0)
    pygame.draw.rect(WINDOW, (255, 0, 0), [yammie.x, yammie.y, YAMMIE_WIDTH, YAMMIE_WIDTH], 0)


def generate_yammie():
    x = random.randint(10, WINDOW_WIDTH - YAMMIE_WIDTH)
    y = random.randint(10, WINDOW_HEIGHT - YAMMIE_WIDTH)
    return Block(x, y)


def move_snake(block_stack, direction):
    delta_x = block_stack[0].x + direction[0] * BLOCK_WIDTH
    delta_y = block_stack[0].y + direction[1] * BLOCK_WIDTH
    new_head = block_stack.pop()
    new_head.x = delta_x
    new_head.y = delta_y
    block_stack.insert(0, new_head)


def check_yammie_collision(head, yammie):
    return pygame.Rect(head.x, head.y, BLOCK_WIDTH, BLOCK_WIDTH).colliderect(
        pygame.Rect(yammie.x, yammie.y, BLOCK_WIDTH, BLOCK_WIDTH))


def check_two_block_collision(b1, b2):
    return b1.x == b2.x and b1.y == b2.y


def check_collisions(block_stack):
    head = block_stack[0]
    for i in range(1, len(block_stack)):
        if check_two_block_collision(head, block_stack[i]):
            return True
    if head.x < 0 or head.x >= WINDOW_WIDTH or head.y < 0 or head.y >= WINDOW_HEIGHT:
        return True
    return False


def main():
    direction = [0, 1]
    block_stack = []
    init_block = Block(300, 300)
    block_stack.append(init_block)
    tick_time = 10
    tick = 0
    yammie = generate_yammie()
    key_cooldown = False
    check_collision_cooldown = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    if direction != [1, 0] and not key_cooldown:
                        direction = [-1, 0]
                elif event.key == K_RIGHT:
                    if direction != [-1, 0] and not key_cooldown:
                        direction = [1, 0]
                elif event.key == K_UP:
                    if direction != [0, 1] and not key_cooldown:
                        direction = [0, -1]
                elif event.key == K_DOWN:
                    if direction != [0, -1] and not key_cooldown:
                        direction = [0, 1]
                key_cooldown = True
        if tick % tick_time == 0:
            move_snake(block_stack, direction)
            key_cooldown = False
            check_collision_cooldown = False
        if check_yammie_collision(block_stack[0], yammie):
            yammie = generate_yammie()
            to_add = Block(block_stack[-1].x, block_stack[-1].y)
            block_stack.insert(-1, to_add)
            check_collision_cooldown = True
        if check_collisions(block_stack) and not check_collision_cooldown:
            pygame.quit()
            sys.exit()
        tick += 1
        WINDOW.fill(BACKGROUND)
        draw_rects(block_stack, yammie)
        pygame.display.update()
        fpsClock.tick(FPS)


main()
