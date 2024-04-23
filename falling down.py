import pygame, sys
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Falling objects')

background_image = pygame.image.load(r'C:\Users\mikhe\Desktop\space2.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
myimage = pygame.image.load(r"C:\Users\mikhe\Desktop\ufo.png")
# rect parameters
x_of_rect = 0
y_of_rect = 0
rect_width = 50
rect_height = 50
delta_x_rect = 2

FALL_OBJECT_WIDTH = rect_width
FALL_OBJECT_DELTA_Y = 1

tick_time = 170
tick = 0



capacity = 50
pointer = 0
score = 0

font = pygame.font.Font(None, 50)




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


def check_collisions(stuff):
    return pygame.Rect(player.x, player.y, rect_width, rect_width).colliderect(
        pygame.Rect(stuff.x, stuff.y, rect_width, rect_width))

player = Block(460,740)
key_right_pressed = False
key_left_pressed = False

blocks = [0 for i in range(0,50)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                key_right_pressed = True
            if event.key == K_LEFT:
                key_left_pressed = True
        elif event.type == KEYUP:
            if event.key == K_RIGHT:
                key_right_pressed = False
            if event.key == K_LEFT:
                key_left_pressed = False
    if key_right_pressed == True:
        player.x += 1
    if key_left_pressed == True:
        player.x -= 1
    if player.x + rect_width >= SCREEN_WIDTH:
        player.x = SCREEN_WIDTH - rect_width
    if player.x <= 0:
        player.x = 0
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen,(0,255,0),(player.x,player.y,rect_width,rect_width))
    # rect movement
    if x_of_rect + rect_width >= SCREEN_WIDTH:
        delta_x_rect *= -1
    if x_of_rect + 1 <= 0:
        delta_x_rect *= -1
    x_of_rect += delta_x_rect
    r = (x_of_rect, y_of_rect, rect_width, rect_height)
    pygame.draw.rect(screen, (0, 0, 0), r)


    if tick % tick_time == 0:
        tick = 0
        blocks[pointer] = generate_stuff()
        pointer += 1
        score += 1
    if pointer == capacity:
        pointer = 0
    for block in blocks:
        if isinstance(block, Block):
            block.update_position()  # Update the position of each block
            draw_rect(block)
            if check_collisions(block):
                pygame.quit()
                sys.exit()
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    tick += 1
    pygame.display.flip()