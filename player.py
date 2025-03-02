import pygame
from resources.sprite.anima import Anima
from resources.sprite.spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self, spriteName: str, keys: tuple[pygame.event.Event], scale: tuple[int] | None = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet("resources/sprite/azuball_spritesheet.png").parse_sprite(spriteName)
        if scale:   self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.collide_rect = pygame.Rect(self.rect.x, self.rect.y, 50, self.rect.height * .9)
        self.collide_rect_offset = self.rect.width/2 -25
        
        self.LEFT_KEY, self.RIGHT_KEY, self.UP_KEY = keys
        
        self.LEFT_KEY_PRESSED, self.RIGHT_KEY_PRESSED = False, False
        self.is_jumping, self.on_ground = False, False
        
        self.gravity, self.friction = 1.5, -0.07
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.l_wall, self.r_wall = 130, 936
        self.floor = 570
        
        self.animator = Anima()
        self.in_animation = False
        self.sel_animation = False # False = throw, True = prep
        self.animation_timer = 0
        self.near_prepped = False
        self.prepped = False

    def draw(self, display: pygame.Surface):
        display.blit(self.image, self.rect)

    def update(self, dt: float):
        if self.in_animation and not self.sel_animation:    return
        
        self.horizontal_movement(dt)
        self.vertical_movement(dt)

    def horizontal_movement(self, dt: float):
        self.acceleration.x = 0
        if self.LEFT_KEY_PRESSED:
            self.acceleration.x -= 1
        elif self.RIGHT_KEY_PRESSED:
            self.acceleration.x += 1
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(10)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 0.5) * (dt * dt)
        self.stay_inside()
        self.rect.x = self.position.x
        self.collide_rect.x = self.rect.x + self.collide_rect_offset

    def vertical_movement(self, dt: float):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 10:
            self.velocity.y = 10
        self.position.y += self.velocity.y * dt + (self.acceleration.y * 0.5) * (dt * dt)
        if self.position.y > self.floor:
            self.position.y = self.floor
            self.velocity.y = 0
            self.on_ground = True
        self.rect.bottom = self.position.y
        self.collide_rect.bottom = self.rect.bottom

    def limit_velocity(self, max_vel: float):
        self.velocity.x = min(max_vel, max(self.velocity.x, -max_vel))
        if abs(self.velocity.x) < 0.2:
            self.velocity.x = 0
    
    def stay_inside(self):
        left_boundary = self.l_wall - self.collide_rect_offset
        right_boundary = self.r_wall - self.collide_rect.width - self.collide_rect_offset
        self.position.x = max(left_boundary, min(right_boundary, self.position.x))

    def jump(self):
        if self.on_ground:
            self.velocity.y = -20
            self.on_ground = False
            self.is_jumping = True

    def stop_movement(self):
        self.velocity.x = 0
        self.velocity.y = 0
    
    def handle_animations(self, dt: float, spritesheet: Spritesheet, ball_box: pygame.Rect):
        self.animation_timer += dt/60
        if self.sel_animation and not self.prepped: # sel_animation = True: prep
            if self.animation_timer == dt/60: print("\nPrepping ball")
            
            if self.handle_ball_prep(ball_box, self.animation_timer, spritesheet):
                self.animation_timer = 0
                self.in_animation = False
                self.prepped = True
        
        elif not self.sel_animation: # sel_animation = False: throw
            if self.animation_timer == dt/60: print("\nThrowing ball")
            self.stop_movement()
            
            if self.play_animation("throw", self.animation_timer, spritesheet):
                self.animation_timer = 0
                self.in_animation = False
    
    def play_animation(self, name: str, time: float, spritesheet: Spritesheet, set_default_after: bool = True):
        if self.animator.animate_player(self, name, time):
            print("Animation ended")
            if set_default_after:
                image = spritesheet.parse_sprite("osaka_0.png")
                self.image = image if image.get_size() == self.image.get_size() else pygame.transform.scale(image, self.image.get_size())
            return True
        return False
    
    def handle_ball_prep(self, ball_box: pygame.Rect, time: float, spritesheet: Spritesheet):
        if self.near_prepped:
            if abs(ball_box.centerx - self.rect.centerx) <= 50:
                image = spritesheet.parse_sprite("osaka_4.png")
                self.image = image if image.get_size() == self.image.get_size() else pygame.transform.scale(image, self.image.get_size())
                print("Prepped")
                self.prepped = True
                return True
        else:
            if self.play_animation("prep", time, spritesheet, False):
                self.near_prepped = True
        return False
