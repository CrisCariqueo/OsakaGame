import pygame
import SataAndagi
import Player

# NO SOPORTA ==========================================
# Audio
#   .m4a
# =====================================================

def render():
    window.fill((55, 55, 55))
    osaka.render(window)
    SataAndagi.sata_render(window)
    SataAndagi.sataCounter_render(window)
    
    pygame.display.flip() # Todos los elementos del juego se vuelven a dibujar
    
def play():
    jugando = True
    while jugando:  # Bucle principal del juego
        for event in pygame.event.get():    # Comprobamos los eventos
            if event.type == pygame.QUIT:   # Comprobamos si se ha pulsado el botón de cierre de la ventana
                jugando = False
        
        osaka.handle_keys()
        render()
        # handle_collisions()
        SataAndagi.handle_sata_obtain(osaka)
        if SataAndagi.sound.get_num_channels() > 10:
            jugando = False
        
        pygame.time.Clock().tick(60)    # Controlamos la frecuencia de refresco (FPS)

# Main ========================================
pygame.init()
window = pygame.display.set_mode((800,600))
pygame.display.set_caption("sata andagi")


# osaka
osakaSprite = "./resources/sprite/kasuga-240x240.jpg"
osakaDeathSound = "./resources/sound/Flashbang sfx.mp3"

osaka = Player.player(osakaSprite, (100,100), [0,0], osakaDeathSound)

# sataAndagi
sataSprite = "./resources/sprite/sata_andagi-50x50.png"

sata01 = SataAndagi.sata(sataSprite, (400,400))
sata02 = SataAndagi.sata(sataSprite, (500,400))
sata03 = SataAndagi.sata(sataSprite, (600,400))

SataAndagi.add_sata(sata01)
SataAndagi.add_sata(sata02)
SataAndagi.add_sata(sata03)

play()
pygame.quit()
