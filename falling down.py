import pygame
import sys

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Falling objects')

# rect parameters
x_of_rect = 0
y_of_rect = 0
rect_width = 100
rect_height = 50
delta_x_rect = 2

FALL_OBJECT_WIDTH = rect_width
FALL_OBJECT_DELTA_Y = 1


class Block:  # class Block
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_y = 1

    def update_position(self):
        self.y += self.velocity_y

    def __str__(self):
        return f"{self.x}, {self.y}"


def draw_rect(stuff):
    pygame.draw.rect(screen, (255, 0, 0), (stuff.x, stuff.y, FALL_OBJECT_WIDTH, FALL_OBJECT_WIDTH), 0)


def generate_stuff():
    x = x_of_rect
    y = y_of_rect + rect_height
    return Block(x, y)


tick_time = 200
tick = 0

blocks = [0 for i in range(50)]

capacity = 50
pointer = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((255, 255, 255))
    # rect movement
    if x_of_rect + rect_width >= SCREEN_WIDTH:
        delta_x_rect *= -1
    if x_of_rect + 1 <= 0:
        delta_x_rect *= -1
    x_of_rect += delta_x_rect
    r = (x_of_rect, y_of_rect, rect_width, rect_height)
    pygame.draw.rect(screen, (0, 0, 0), r)

    # block = generate_stuff()

    if tick % tick_time == 0:
        tick = 0
        blocks[pointer] = generate_stuff()
        pointer += 1
        if pointer == capacity:
            pointer = 0
    for block in blocks:
        if isinstance(block, Block):
            block.update_position()  # Update the position of each block
            draw_rect(block)
    tick += 1
    pygame.display.flip()
