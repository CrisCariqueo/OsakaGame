import pygame
from resources.sprite.spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self, spriteName: str, keys: tuple[pygame.event.Event]):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet("resources/sprite/azuball_spritesheet.png").parse_sprite(spriteName)
        self.rect = self.image.get_rect()
        
        self.LEFT_KEY, self.RIGHT_KEY, self.UP_KEY = keys
        
        self.LEFT_KEY_PRESSED, self.RIGHT_KEY_PRESSED = False, False
        self.is_jumping, self.on_ground = False, False
        
        self.gravity, self.friction = 1.5, -0.07
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.floor = 570
        self.acceleration = pygame.math.Vector2(0, self.gravity)

    def draw(self, display):
        display.blit(self.image, self.rect)

    def update(self, dt):
        self.horizontal_movement(dt)
        self.vertical_movement(dt)

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY_PRESSED:
            self.acceleration.x -= 1
        elif self.RIGHT_KEY_PRESSED:
            self.acceleration.x += 1
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(10)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 0.5) * (dt * dt)
        self.rect.x = self.position.x

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 10:
            self.velocity.y = 10
        self.position.y += self.velocity.y * dt + (self.acceleration.y * 0.5) * (dt * dt)
        if self.position.y > self.floor:
            self.position.y = self.floor
            self.velocity.y = 0
            self.on_ground = True
        self.rect.bottom = self.position.y

    def limit_velocity(self, max_vel):
        self.velocity.x = min(max_vel, max(self.velocity.x, -max_vel))
        if abs(self.velocity.x) < 0.2:
            self.velocity.x = 0

    def jump(self):
        if self.on_ground:
            self.velocity.y = -20
            self.on_ground = False
            self.is_jumping = True
