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
        self.player_1 = Player("osaka_0.png", (pygame.K_a, pygame.K_d, pygame.K_w))
        self.player_1.position.x, self.player_1.position.y = 130, DISPLAY_H
        ## reducing the player size because
        self.player_1.image = pygame.transform.scale(self.player_1.image, (128, 274))
        self.player_1.rect = self.player_1.image.get_rect()
        
        self.player_2 = Player("chiyo_0.png", (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP))
        self.player_2.position.x, self.player_2.position.y = DISPLAY_W-258, DISPLAY_H
        self.player_2.image = pygame.transform.scale(self.player_2.image, (128, 274))
        self.player_2.rect = self.player_2.image.get_rect()

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

                self.check_player_keys(self.player_1, event)
                self.check_player_keys(self.player_2, event)
            
            ############# UPDATE PLAYER #############
            self.player_1.update(dt)
            self.player_2.update(dt)
            
            ############# UPDATE WINDOW AND DISPLAY #############
            self.canvas.fill((58, 57, 57))
            self.canvas.blit(self.background, (133, 0))
            self.player_1.draw(self.canvas)
            self.player_2.draw(self.canvas)
            
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

game = Azuball()
game.play()
