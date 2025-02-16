import pygame
from resources.sprite.anima import Anima
from resources.sprite.spritesheet import Spritesheet

############# LOAD UP BASIC WINDOW #############
pygame.init()
DISPLAY_W, DISPLAY_H = 1066, 600
canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
running = True
clock = pygame.time.Clock()
TARGET_FPS = 60
################################################

my_spritesheet = Spritesheet("resources/sprite/azuball_spritesheet.png")
animator = Anima()
animator.create_animation(my_spritesheet, "osaka/osaka_waltah/osaka_waltah", "osaka_waltah", 5)
animator.create_animation(my_spritesheet, "osaka/hapi/hapi", "osaka_hapi", 3)

print(animator.animations)

print("\nOSAKA WALTAH:",
      animator.animations["osaka_waltah"],
      "\nn frames:", len(animator.animations["osaka_waltah"]["frames"]),
      "\nduration:", animator.animations["osaka_waltah"]["duration"]
)
anim_play_waltah = False
anim_timer_waltah = 0

print("\nOSAKA HAPI:",
      animator.animations["osaka_hapi"],
      "\nn frames:", len(animator.animations["osaka_hapi"]["frames"]),
      "\nduration:", animator.animations["osaka_hapi"]["duration"]
)
anim_play_hapi = False
anim_timer_hapi = 0

while running:
    dt = clock.tick(60) * 0.001 * TARGET_FPS
    ############# CHECK PLAYER INPUT #############
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ############# UPDATE SPRITE IF SPACE IS PRESSED #############
            if event.key == pygame.K_SPACE:
                print("reproducing animation")
                anim_play_waltah = not anim_play_waltah
                if not anim_play_waltah:    anim_timer_waltah = 0
                
                anim_play_hapi = not anim_play_hapi
                if not anim_play_hapi:      anim_timer_hapi = 0

    ############# UPDATE WINDOW AND DISPLAY #############
    canvas.fill((255, 255, 255))
    
    if anim_play_waltah:
        anim_timer_waltah += dt/60
        if animator.play_animation(canvas, "osaka_waltah", anim_timer_waltah, (DISPLAY_W/3, DISPLAY_H/2)):
            anim_play_waltah = False
            anim_timer_waltah = 0
    
    if anim_play_hapi:
        anim_timer_hapi += dt/60
        if animator.play_animation(canvas, "osaka_hapi", anim_timer_hapi, (DISPLAY_W*2/3, DISPLAY_H/2)):
            anim_play_hapi = False
            anim_timer_hapi = 0
    
    window.blit(canvas, (0, 0))
    pygame.display.update()
