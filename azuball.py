import pygame
from resources.sprite.spritesheet import Spritesheet
from player import Player
from ball import Ball

class Azuball:
    def __init__(self):
        ############# LOAD UP BASIC WINDOW AND CLOCK #############
        pygame.init()
        DISPLAY_W, DISPLAY_H = 1066, 600
        self.canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
        self.window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
        self.running = True
        self.clock = pygame.time.Clock()
        self.TARGET_FPS = 60

        ############# LOAD PLAYER #############
        self.player_1 = Player("osaka_4.png", (pygame.K_a, pygame.K_d, pygame.K_w))
        self.player_1.position.x, self.player_1.position.y = 130, DISPLAY_H
        ## reducing the player size because
        self.player_1.image = pygame.transform.scale(self.player_1.image, (128, 274))
        self.player_1.rect = self.player_1.image.get_rect()
        self.player_1.collide_rect_offset = self.player_1.rect.width/2
        self.player_1.collide_rect.height = self.player_1.rect.height*.82
        self.player_1.boundaries = 130, DISPLAY_W/2
        
        self.player_2 = Player("chiyo_4.png", (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP))
        self.player_2.position.x, self.player_2.position.y = DISPLAY_W-258, DISPLAY_H
        self.player_2.image = pygame.transform.scale(self.player_2.image, (128, 274))
        self.player_2.rect = self.player_2.image.get_rect()
        self.player_2.collide_rect_offset = self.player_2.rect.width/2 + 7
        self.player_2.collide_rect.height = self.player_2.rect.height*.72
        self.player_2.boundaries = DISPLAY_W/2, DISPLAY_W-130
        
        ############# LOAD BACKGROUND #############
        background_img = pygame.image.load("resources/sprite/azuball_field-800x600.png").convert()
        self.background = pygame.Surface((800, 600))
        self.background.blit(background_img, (0, 0))

        ############# LOAD SPRITESHEET #############
        spritesheet = Spritesheet("resources/sprite/azuball_spritesheet.png")

        ############# LOAD VOLLEY ELEMENTS #############
        net_img = spritesheet.parse_sprite("net.png")  # 10x128
        net_img = pygame.transform.scale(net_img, (28, 358))
        net_x, net_y = ((((DISPLAY_W-260)/2) - net_img.get_width()/2) - 5, DISPLAY_H-net_img.get_height()+10)
        self.background.blit(net_img, (net_x, net_y))
        self.net_rect = pygame.Rect((net_x + 135, net_y + 3), (net_img.get_width() - 3, 100))
        
        self.ball = Ball()
        self.ball.position.x, self.ball.position.y = DISPLAY_W/4, 200
        self.ball.acceleration.y = 0

    def play(self):
        ############# MAIN GAME LOOP #############
        while self.running:
            dt = self.clock.tick(60) * 0.001 * self.TARGET_FPS
            ############# CHECK PLAYER INPUT #############
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.check_player_keys(self.player_1, event)
                self.check_player_keys(self.player_2, event)

                self.test_ball_physics(event)

            ############# UPDATE PLAYER AND BALL #############
            self.player_1.update(dt)
            self.player_2.update(dt)
            
            if self.ball.rect.left < self.net_rect.right or self.ball.rect.right > self.net_rect.left:
                self.ball.rect_collision(self.net_rect)
            
            if self.ball.rect.centerx < 530:
                self.ball.update(dt, self.player_1.collide_rect)
            else:
                self.ball.update(dt, self.player_2.collide_rect)

            ############# UPDATE WINDOW AND DISPLAY #############
            self.canvas.fill((58, 57, 57))
            self.canvas.blit(self.background, (133, 0))
            self.player_1.draw(self.canvas)
            self.player_2.draw(self.canvas)
            self.ball.draw(self.canvas)

            self.show_rects()
            self.show_kinetic_data(self.ball)

            self.window.blit(self.canvas, (0, 0))
            pygame.display.update()
    
    def check_player_keys(self, player: Player, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == player.LEFT_KEY:
                player.LEFT_KEY_PRESSED = True
            elif event.key == player.RIGHT_KEY:
                player.RIGHT_KEY_PRESSED = True
            elif event.key == player.UP_KEY:
                player.jump()
        
        if event.type == pygame.KEYUP:
            if event.key == player.LEFT_KEY:
                player.LEFT_KEY_PRESSED = False
            elif event.key == player.RIGHT_KEY:
                player.RIGHT_KEY_PRESSED = False
            elif event.key == player.UP_KEY:
                if player.is_jumping:
                    player.velocity.y *= 0.5 
                    player.is_jumping = False

    def test_ball_physics(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.ball.fell:
                    self.ball.position.x, self.ball.position.y = 266, 200
                    self.ball.acceleration.y = 0
                    self.ball.velocity.x, self.ball.velocity.y = 0, 0
                    self.ball.fell = False
                else:
                    self.ball.acceleration.y = self.ball.gravity
                    self.ball.velocity.x, self.ball.velocity.y = 10, -20

    def show_rects(self):
        pygame.draw.rect(self.canvas, (0, 0, 0), self.player_1.rect, 1)
        pygame.draw.rect(self.canvas, (0, 0, 0), self.player_2.rect, 1)
        pygame.draw.rect(self.canvas, (0, 0, 0), self.ball.rect, 1)
        pygame.draw.rect(self.canvas, (0, 0, 0), self.net_rect, 1)
        
        pygame.draw.rect(self.canvas, (250, 0, 0), self.player_1.collide_rect, 1)
        pygame.draw.rect(self.canvas, (250, 0, 0), self.player_2.collide_rect, 1)
    
    def show_kinetic_data(self, object: Player | Ball):
        font = pygame.font.Font(None, 36)
        pos = f"Position: {object.position}"
        pos_info = font.render(pos, 1, (0, 0, 0))
        self.canvas.blit(pos_info, (0, 0))
        
        vel = f"Velocity: {object.velocity}"
        vel_info = font.render(vel, 1, (0, 0, 0))
        self.canvas.blit(vel_info, (0, 30))

        acc = f"Acceleration: {object.acceleration}"
        acc_info = font.render(acc, 1, (0, 0, 0))
        self.canvas.blit(acc_info, (0, 60))

game = Azuball()
game.play()
