import pygame
from resources.sprite.spritesheet import spritesheet

############# LOAD UP BASIC WINDOW #############
pygame.init()
DISPLAY_W, DISPLAY_H = 1066, 600
canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
running = True
################################################

my_spritesheet = spritesheet("resources/sprite/azuball_spritesheet.png")
# osaka = my_spritesheet.parse_sprite("osaka_1.png")
osaka = [my_spritesheet.parse_sprite(f"osaka_{i}.png") for i in range(0, 6)]
chiyo = [my_spritesheet.parse_sprite(f"chiyo_{i}.png") for i in range(0, 6)]

index = 0

while running:
    ############# CHECK PLAYER INPUT #############
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ############# UPDATE SPRITE IF SPACE IS PRESSED #############
            if event.key == pygame.K_SPACE:
                index = (index + 1) % len(osaka)



    ############# UPDATE WINDOW AND DISPLAY #############
    canvas.fill((255, 255, 255))
    canvas.blit(osaka[index], (100, DISPLAY_H - 407))
    canvas.blit(chiyo[index], (DISPLAY_W - 290, DISPLAY_H - 407))
    window.blit(canvas, (0, 0))
    pygame.display.update()
