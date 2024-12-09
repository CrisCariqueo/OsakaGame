import pygame
import SataCatcher

pygame.init()
window = pygame.display.set_mode((800,600))
pygame.display.set_caption("Osaka Game")

selectGame = 0
jugando = True


SataCatcher.play()

print("Game Over")

pygame.quit()
