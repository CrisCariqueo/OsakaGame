import pygame

class player:
    def __init__(self, sprite: str, initialPos: tuple, speed: list[int], deathSound: str):
        self.sprite = pygame.image.load(sprite)
        self.box    = self.sprite.get_rect()
        self.box.move_ip(initialPos[0], initialPos[1])
        self.speed = speed
        self.deathSound = pygame.mixer.Sound(deathSound)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.box.move_ip(-6,0)
        if keys[pygame.K_RIGHT]:
            self.box.move_ip(6,0)
        if keys[pygame.K_UP]:
            self.box.move_ip(0,-6)
        if keys[pygame.K_DOWN]:
            self.box.move_ip(0,6)

    def render(self, window: pygame.Surface):
        window.blit(self.sprite, self.box)
