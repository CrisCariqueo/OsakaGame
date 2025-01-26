import pygame
import json
import SataAndagi
import Player
from Killer import killer

# NO SOPORTA ==========================================
# Audio
#   .m4a
# =====================================================


def play():
    global playing
    while playing:  # Bucle principal del juego
        for event in pygame.event.get():    # Comprobamos los eventos
            if event.type == pygame.QUIT:   # Comprobamos si se ha pulsado el botón de cierre de la ventana
                playing = False
        
        osaka.handle_keys()
        render()
        handle_collisions()
        SataAndagi.handle_sata_obtain(osaka)
        
        killer01.move()
        
        if SataAndagi.sound.get_num_channels() > 10:
            playing = False
        
        pygame.time.Clock().tick(60)    # Controlamos la frecuencia de refresco (FPS)

def render():
    window.fill((55, 55, 55))
    osaka.render(window)
    SataAndagi.sata_render(window)
    SataAndagi.sataCounter_render(window)
    osaka.pos_render(window)

    killer01.render(window)
    
    pygame.display.flip() # Todos los elementos del juego se vuelven a dibujar

def handle_collisions():
    if killer01.check_kill(osaka):
        death()

def death():
    osaka.die()
    finish_game()

def finish_game():
    global playing
    playing = False
    print("Sata Catcher Over")
    

# Main ========================================
pygame.init()
window = pygame.display.set_mode((800,600))
pygame.display.set_caption("Sata Catcher")
sata_data = json.load(open("resources/data/sataCatcher_data.json"))

playing = True

# map


# osaka
osakaSprite = "./resources/sprite/kasuga-240x240.jpg"
osakaDeathSound = "./resources/sound/Flashbang sfx.mp3"

osakaInitialPos = sata_data['osaka_pos']
osaka = Player.player(osakaSprite, 
                      (osakaInitialPos[0], osakaInitialPos[1]), 
                      [0,0], 
                      osakaDeathSound)

# sataAndagi
sataSprite = "./resources/sprite/sata_andagi-50x50.png"

for i in sata_data['sata_andagi_pos']:
    x, y = sata_data['sata_andagi_pos'][i]
    sata = SataAndagi.sata(sataSprite, (x, y))
    SataAndagi.add_sata(sata)

# killer
killerSprite = "./resources/sprite/tiger-150x99.png"

killer01 = killer(killerSprite, (750,100), [-8,0])

play()
# pygame.quit()
