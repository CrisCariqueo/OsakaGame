import pygame
from resources.sprite.anima import Anima
from resources.sprite.spritesheet import Spritesheet
from player import Player

def check_player_keys(player: Player, event: pygame.event.Event):
    if event.type == pygame.KEYDOWN:
        if event.key == player.LEFT_KEY:
            player.LEFT_KEY_PRESSED = True
        elif event.key == player.RIGHT_KEY:
            player.RIGHT_KEY_PRESSED = True
        elif event.key == player.UP_KEY:
            player.jump()
    
    if event.type == pygame.KEYUP:
        if event.key == player.LEFT_KEY:
            player.LEFT_KEY_PRESSED = False
        elif event.key == player.RIGHT_KEY:
            player.RIGHT_KEY_PRESSED = False
        elif event.key == player.UP_KEY:
            if player.is_jumping:
                player.velocity.y *= 0.5 
                player.is_jumping = False

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

player = Player("osaka_0.png", (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP), (128, 274))
player.position.x, player.position.y = 130, DISPLAY_H
player.animator.create_animation(my_spritesheet, "osaka_ball", "throw", .4)
player_animation = False
player_animation_timer = 0

while running:
    dt = clock.tick(60) * 0.001 * TARGET_FPS
    ############# CHECK PLAYER INPUT #############
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        check_player_keys(player, event)
        
        if event.type == pygame.KEYDOWN:
            ############# UPDATE SPRITE IF SPACE IS PRESSED #############
            if event.key == pygame.K_SPACE:
                print("\nReproducing animation")
                anim_play_waltah = not anim_play_waltah
                if not anim_play_waltah:    anim_timer_waltah = 0
                
                anim_play_hapi = not anim_play_hapi
                if not anim_play_hapi:      anim_timer_hapi = 0
            
            if event.key == pygame.K_DOWN:
                print("\nReproducing player animation")
                player_animation = not player_animation
                if not player_animation:    player_animation_timer = 0
    
    ############# UPDATE PLAYER #############
    player.update(dt)

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
    
    if player_animation:
        player_animation_timer += dt/60
        if player.play_animation("throw", player_animation_timer, my_spritesheet):
            player_animation = False
            player_animation_timer = 0
    
    player.draw(canvas)
    
    window.blit(canvas, (0, 0))
    pygame.display.update()
