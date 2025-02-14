import pygame
from resources.sprite.spritesheet import Spritesheet
from player import Player

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet("resources/sprite/azuball_spritesheet.png").parse_sprite("ballx32.png")
        self.rect = pygame.draw.circle(self.image, (0,0,0), (16, 16), 16, width=1)

        self.fell = False
        self.gravity, self.friction = 1.5, -0.04
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.boundaries = 130, 936
        self.floor = 570
    
    def draw(self, display):
        display.blit(self.image, self.rect)
    
    def update(self, dt, collide_rect: pygame.Rect):
        self.horizontal_movement(dt, collide_rect)
        self.vertical_movement(dt)

    def horizontal_movement(self, dt, collide_rect: pygame.Rect):
        self.acceleration.x = 0
        if self.fell: 
            self.acceleration.x += self.velocity.x * self.friction
            self.velocity.x += self.acceleration.x * dt
        self.rect_collision(collide_rect)
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
            self.velocity.y = -self.velocity.y/2
            self.fell = True
        self.rect.bottom = self.position.y
        return self.fell
    
    def limit_velocity(self, max_vel):
        self.velocity.x = min(max_vel, max(self.velocity.x, -max_vel))
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0

    def bounce_on_wall(self):
        if self.position.x <= self.boundaries[0] or self.position.x >= self.boundaries[1] - self.rect.width:
            self.velocity.x = -self.velocity.x
    
    def rect_collision(self, collide_rect: pygame.Rect):
        # return self.rect.colliderect(player.collide_rect)
        if self.rect.centery < collide_rect.top:
            cat_v = abs(collide_rect.top - self.rect.centery)
            cat_h = abs(collide_rect.centerx - self.rect.centerx)
            hyp = (cat_v**2 + cat_h**2)**0.5
            if hyp <= 36:
                self.velocity.y = -self.velocity.y
                self.velocity.x = (self.rect.centerx - collide_rect.centerx) / 10
        else:
            if abs(collide_rect.centerx - self.rect.centerx) <= 36:
                self.velocity.x = (self.rect.centerx - collide_rect.centerx) / 10
                # self.velocity.x = -self.velocity.x
