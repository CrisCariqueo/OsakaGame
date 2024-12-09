import pygame
from Player import player

sataCounter = 0
__sataArr = []

pygame.mixer.init()
sound  = pygame.mixer.Sound("./resources/sound/Sata andagi_x2.mp3")

def add_sata(sata):
    __sataArr.append(sata)

def count_sata():
    global sataCounter
    sataCounter += 1

def handle_sata_obtain(player: player):
        for sata in __sataArr:
            if player.box.colliderect(sata.box):
                count_sata()                # NO ACCECIBLE
                print("Sata Andagi++", sataCounter)
                __sataArr.remove(sata)
                sound.play() # Reproduce el sonido de colisión

def sata_render(window: pygame.Surface):
    # ventana.blit(sata, sataBox)
    for sata in __sataArr:
        window.blit(sata.sprite, sata.box)

def sataCounter_render(window: pygame.Surface):
    font = pygame.font.Font(None, 36)
    text = font.render("Sata Andagi: " + str(sataCounter), 1, (255, 255, 255))
    window.blit(text, (10, 10))

class sata:
    def __init__(self, sprite: str, initialPos: tuple):
        self.sprite = pygame.image.load(sprite)
        self.box    = self.sprite.get_rect()
        self.box.move_ip(initialPos[0], initialPos[1])
    