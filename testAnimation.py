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

def move_ball_emuler(ball_emuler_box: pygame.Rect, event: pygame.event.Event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            ball_emuler_box.x -= 10
        elif event.key == pygame.K_d:
            ball_emuler_box.x += 10
        elif event.key == pygame.K_w:
            ball_emuler_box.y -= 10
        elif event.key == pygame.K_s:
            ball_emuler_box.y += 10 

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

print("\nOSAKA WALTAH:",
      "\nn frames:", len(animator.animations["osaka_waltah"]["frames"]),
      "\nduration:", animator.animations["osaka_waltah"]["duration"]
)
anim_play_waltah = False
anim_timer_waltah = 0

print("\nOSAKA HAPI:",
      "\nn frames:", len(animator.animations["osaka_hapi"]["frames"]),
      "\nduration:", animator.animations["osaka_hapi"]["duration"]
)
anim_play_hapi = False
anim_timer_hapi = 0

player = Player("osaka_0.png", (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP), (128, 274))
player.position.x, player.position.y = 130, DISPLAY_H
player.animator.create_animation(my_spritesheet, "osaka", "prep", .3, 4)
player.animator.create_animation(my_spritesheet, "osaka_ball", "throw", .4)
player_animation = False
player_animation_timer = 0

print("\nanimations loaded:")
for i in player.animator.animations:
    print(i)

ball_emuler = my_spritesheet.parse_sprite("ballx32.png")
ball_emuler_box = ball_emuler.get_rect()
ball_emuler_box.x, ball_emuler_box.y = DISPLAY_W-130, 100

while running:
    dt = clock.tick(60) * 0.001 * TARGET_FPS
    ############# CHECK PLAYER INPUT #############
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        check_player_keys(player, event)
        move_ball_emuler(ball_emuler_box, event)
        
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
                player.in_animation = True
                player.sel_animation = False
                
    ############# UPDATE PLAYER #############
    player.update(dt)
    
    if abs(ball_emuler_box.centerx - player.rect.centerx) < 150:
        player.in_animation = True
        player.sel_animation = True

    ############# UPDATE WINDOW AND DISPLAY #############
    canvas.fill((60, 60, 60))
    
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
    
    if player.in_animation:
        player.handle_animations(dt, my_spritesheet, ball_emuler_box)
    
    player.draw(canvas)
    canvas.blit(ball_emuler, ball_emuler_box)
    
    window.blit(canvas, (0, 0))
    pygame.display.update()
