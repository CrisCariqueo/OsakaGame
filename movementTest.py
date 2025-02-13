import pygame
from resources.sprite.spritesheet import Spritesheet
from player import Player

############# LOAD UP BASIC WINDOW AND CLOCK #############
pygame.init()
DISPLAY_W, DISPLAY_H = 1066, 600
canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
running = True
clock = pygame.time.Clock()
TARGET_FPS = 60

############# LOAD PLAYER AND SPRITESHEET #############
my_spritesheet = Spritesheet("resources/sprite/azuball_spritesheet.png")
player = Player("osaka_0.png")
player.position.x, player.position.y = 100, DISPLAY_H

############# LOAD BACKGROUND #############
background_img = pygame.image.load("resources/sprite/azuball_field-800x600.png").convert()
background = pygame.Surface((800, 600))
background.blit(background_img, (0, 0))

############# MAIN GAME LOOP #############
while running:
    dt = clock.tick(60) * 0.001 * TARGET_FPS
    ############# CHECK PLAYER INPUT #############
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.LEFT_KEY = True
            elif event.key == pygame.K_RIGHT:
                player.RIGHT_KEY = True
            elif event.key == pygame.K_UP:
                player.jump()
        
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.LEFT_KEY = False
            elif event.key == pygame.K_RIGHT:
                player.RIGHT_KEY = False
            elif event.key == pygame.K_UP:
                if player.is_jumping:
                    player.velocity.y *= 0.5 
                    player.is_jumping = False
    
    
    ############# UPDATE PLAYER #############
    player.update(dt)
    
    ############# UPDATE WINDOW AND DISPLAY #############
    canvas.fill((255, 255, 255))
    canvas.blit(background, (133, 0))
    player.draw(canvas)

    ############# DISPLAY PLAYER INFO #############
    font = pygame.font.Font(None, 36)
    pos = f"Position: {player.position}"
    pos_info = font.render(pos, 1, (0, 0, 0))
    canvas.blit(pos_info, (0, 0))
    
    vel = f"Velocity: {player.velocity}"
    vel_info = font.render(vel, 1, (0, 0, 0))
    canvas.blit(vel_info, (0, 30))

    acc = f"Acceleration: {player.acceleration}"
    acc_info = font.render(acc, 1, (0, 0, 0))
    canvas.blit(acc_info, (0, 60))
    
    window.blit(canvas, (0, 0))
    pygame.display.update()
