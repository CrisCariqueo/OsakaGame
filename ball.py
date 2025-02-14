import pygame
from resources.sprite.spritesheet import Spritesheet

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet("resources/sprite/azuball_spritesheet.png").parse_sprite("ballx32.png")
        self.rect = pygame.draw.circle(self.image, (0,0,0), (16, 16), 16, width=1)

        self.fell = False
        self.gravity, self.friction = 1.5, -0.001
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.boundaries = 130, 936
        self.floor = 570
    
    def draw(self, display):
        display.blit(self.image, self.rect)
    
    def update(self, dt):
        self.horizontal_movement(dt)
        self.vertical_movement(dt)

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.fell: self.acceleration.x += self.velocity.x * self.friction
        else:         self.acceleration.x += self.velocity.x
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(10)
        self.bounce_on_wall()
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 0.5) * (dt * dt)
        self.position.x = max(self.boundaries[0], min(self.boundaries[1] - self.rect.width, self.position.x))
        self.rect.x = self.position.x
    
    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        # if self.velocity.y > 10:
        #     self.velocity.y = 10
        self.position.y += self.velocity.y * dt + (self.acceleration.y * 0.5) * (dt * dt)
        
        if self.position.y > self.floor:
            self.position.y = self.floor
            self.velocity.x *= 0.7
            self.velocity.y = -self.velocity.y/2
            self.fell = True
        self.rect.bottom = self.position.y
        return self.fell
    
    def limit_velocity(self, max_vel):
        self.velocity.x = min(max_vel, max(self.velocity.x, -max_vel))
        # if abs(self.velocity.x) < 0.2:
        #     self.velocity.x = 0

    def bounce_on_wall(self):
        if self.position.x <= self.boundaries[0] or self.position.x >= self.boundaries[1] - self.rect.width:
            self.velocity.x = -self.velocity.x
    
    def check_player_collision(self, player):
        # return self.rect.colliderect(player.collide_rect)
        pass
