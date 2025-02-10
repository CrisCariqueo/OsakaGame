import pygame
from resources.sprite.spritesheet import Spritesheet

############# LOAD UP BASIC WINDOW #############
pygame.init()
DISPLAY_W, DISPLAY_H = 1066, 600
canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
running = True
################################################

my_spritesheet = Spritesheet("resources/sprite/azuball_spritesheet.png")
# osaka = my_spritesheet.parse_sprite("osaka_1.png")
osaka = [my_spritesheet.parse_sprite(f"osaka_{i}.png") for i in range(0, 6)]
chiyo = [my_spritesheet.parse_sprite(f"chiyo_{i}.png") for i in range(0, 6)]
referee = [my_spritesheet.parse_sprite(f"haroeberinyanhauaruyufainsankyuehaiwishuaiwasuaberdmusumegaamerikaniyusunodesu_{i}.png") for i in range(0, 2)]
referee.append(pygame.transform.flip(referee[1], True, False))

index = 0
ref_index = 0

while running:
    ############# CHECK PLAYER INPUT #############
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ############# UPDATE SPRITE IF SPACE IS PRESSED #############
            if event.key == pygame.K_SPACE:
                index = (index + 1) % len(osaka)
                ref_index = (ref_index + 1) % len(referee)


    ############# UPDATE WINDOW AND DISPLAY #############
    canvas.fill((255, 255, 255))
    canvas.blit(osaka[index], (100, DISPLAY_H - 407))
    canvas.blit(chiyo[index], (DISPLAY_W - 290, DISPLAY_H - 407))
    if ref_index == 2: canvas.blit(referee[ref_index], (DISPLAY_W/2-90, 100))
    else:              canvas.blit(referee[ref_index], (DISPLAY_W/2-150, 100))
    window.blit(canvas, (0, 0))
    pygame.display.update()
