import pygame
from resources.sprite.spritesheet import Spritesheet
from player import Player

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet("resources/sprite/azuball_spritesheet.png").parse_sprite("ballx32.png")
        self.rect = pygame.draw.circle(self.image, (0,0,0), (16, 16), 16, width=1)

        self.fell = False
        self.gravity, self.friction = 1, -0.04
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.boundaries = 130, 936
        self.floor = 570
    
    def draw(self, display: pygame.Surface):
        display.blit(self.image, self.rect)
    
    def update(self, dt: float, collide_object: Player | pygame.Rect):
        did_bonk = self.handle_collision(collide_object)
        self.horizontal_movement(dt)
        self.vertical_movement(dt)
        return did_bonk

    def horizontal_movement(self, dt: float):
        self.acceleration.x = 0
        if self.fell: 
            self.acceleration.x += self.velocity.x * self.friction
            self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(10)
        self.bounce_on_wall()
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 0.5) * (dt * dt)
        if self.position.x > -50:
            self.position.x = max(self.boundaries[0], min(self.boundaries[1] - self.rect.width, self.position.x))
        self.rect.x = self.position.x
    
    def vertical_movement(self, dt: float):
        self.velocity.y += self.acceleration.y * dt
        self.position.y += self.velocity.y * dt + (self.acceleration.y * 0.5) * (dt * dt)
        
        if self.position.y > self.floor:
            self.position.y = self.floor
            self.velocity.y = -self.velocity.y/2
            self.fell = True
        self.rect.bottom = self.position.y
        return self.fell
    
    def limit_velocity(self, max_vel: float):
        self.velocity.x = min(max_vel, max(self.velocity.x, -max_vel))
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0

    def bounce_on_wall(self):
        if self.position.x <= self.boundaries[0] or self.position.x >= self.boundaries[1] - self.rect.width:
            self.velocity.x = -self.velocity.x
    
    def handle_collision(self, object: Player | pygame.Rect):
        object_rect = object.collide_rect if isinstance(object, Player) else object
        object_velocity = object.velocity if isinstance(object, Player) else pygame.math.Vector2(0, 0)
        
        if self.rect.colliderect(object_rect):
            self.get_outa_my_box(object_rect)
            return self.bounce(object_rect, object_velocity)
        return False
    
    def get_outa_my_box(self, object_rect: pygame.Rect):
        if self.rect.bottom - 2 <= object_rect.top:
            self.rect.bottom = object_rect.top
            return
        
        if abs(self.rect.right - object_rect.left) < abs(object_rect.right - self.rect.left):
            self.rect.right = object_rect.left
        else:
            self.rect.left = object_rect.right
    
    def bounce(self, object_rect: pygame.Rect, object_velocity: pygame.math.Vector2):
        # bouncy y
        if self.rect.bottom < object_rect.top + object_rect.width:
            self.velocity.y = -abs(self.velocity.y)
            if abs(object_velocity.y) < -.2:
                self.velocity.y += object_velocity.y/2
            return True

        # bouncy x
        self.velocity.x = (self.rect.centerx - object_rect.centerx) / 5
        if abs(object_velocity.x) > .2:
            self.velocity.x += object_velocity.x/2
        
        return False

    def throw(self, throw_pos: pygame.math.Vector2, throw_vel: pygame.math.Vector2):
        if self.acceleration.y == 0:
            self.acceleration.y = self.gravity

        self.fell = False
        self.position = throw_pos
        self.velocity = throw_vel
