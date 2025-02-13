import pygame
from resources.sprite.spritesheet import Spritesheet
from player import Player

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
        self.player_1 = Player("osaka_0.png")
        self.player_1.position.x, self.player_1.position.y = 130, DISPLAY_H
        ## reducing the player size because
        self.player_1.image = pygame.transform.scale(self.player_1.image, (128, 274))
        self.player_1.rect = self.player_1.image.get_rect()

        ############# LOAD BACKGROUND #############
        background_img = pygame.image.load("resources/sprite/azuball_field-800x600.png").convert()
        self.background = pygame.Surface((800, 600))
        self.background.blit(background_img, (0, 0))

    def play(self):
        ############# MAIN GAME LOOP #############
        while self.running:
            dt = self.clock.tick(60) * 0.001 * self.TARGET_FPS
            ############# CHECK PLAYER INPUT #############
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.player_1.LEFT_KEY = True
                    elif event.key == pygame.K_d:
                        self.player_1.RIGHT_KEY = True
                    elif event.key == pygame.K_w:
                        self.player_1.jump()
                
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.player_1.LEFT_KEY = False
                    elif event.key == pygame.K_d:
                        self.player_1.RIGHT_KEY = False
                    elif event.key == pygame.K_w:
                        if self.player_1.is_jumping:
                            self.player_1.velocity.y *= 0.5 
                            self.player_1.is_jumping = False
            
            
            ############# UPDATE PLAYER #############
            self.player_1.update(dt)
            
            ############# UPDATE WINDOW AND DISPLAY #############
            self.canvas.fill((58, 57, 57))
            self.canvas.blit(self.background, (133, 0))
            self.player_1.draw(self.canvas)
            
            self.window.blit(self.canvas, (0, 0))
            pygame.display.update()

game = Azuball()
game.play()
