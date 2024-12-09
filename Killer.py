import pygame

class killer:
    def __init__(self, sprite: str, initialPos: tuple, speed: list[int]):
        self.sprite = pygame.image.load(sprite)
        self.box = self.sprite.get_rect()
        self.speed = speed
        self.box.move_ip(initialPos[0], initialPos[1])
    
    def check_kill(self, player):
        if self.box.colliderect(player.box):
            return True
        return False
    
    def move(self):
        self.box = self.box.move(self.speed)
    
    def render(self, window: pygame.Surface):
        window.blit(self.sprite, self.box)
