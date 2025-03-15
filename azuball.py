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
        self.round_started = False
        self.show_throw_box = True

        ############# LOAD SPRITESHEET #############
        self.spritesheet = Spritesheet("resources/sprite/azuball_spritesheet.png")

        ############# LOAD PLAYER #############
        self.player_1 = Player("osaka_0.png", (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_e), (128, 274))
        self.player_1.position.x, self.player_1.position.y = 130, DISPLAY_H
        self.player_1.r_wall = DISPLAY_W/2
        self.player_1.throw_pos_offset.xy = 105, -5
        self.player_1.animator.create_animation(self.spritesheet, "osaka", "prep", .3, 4)
        self.player_1.animator.create_animation(self.spritesheet, "osaka_ball", "throw", .4)
        
        self.player_2 = Player("chiyo_0.png", (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_MINUS), (128, 274))
        self.player_2.ID = True
        self.player_2.position.x, self.player_2.position.y = DISPLAY_W-258, DISPLAY_H
        self.player_2.collide_rect_offset += 7
        self.player_2.collide_rect.height = self.player_2.rect.height * .8
        self.player_2.l_wall = DISPLAY_W/2
        self.player_2.throw_pos_offset.xy = 20, 50
        self.player_2.animator.create_animation(self.spritesheet, "chiyo", "prep", .3, 4)
        self.player_2.animator.create_animation(self.spritesheet, "chiyo_ball", "throw", .4)
        
        ############# LOAD BACKGROUND #############
        background_img = pygame.image.load("resources/sprite/azuball_field-800x600.png").convert()
        self.background = pygame.Surface((800, 600))
        self.background.blit(background_img, (0, 0))

        ############# LOAD VOLLEY ELEMENTS #############
        net_img = self.spritesheet.parse_sprite("net.png")  # 10x128
        net_img = pygame.transform.scale(net_img, (28, 358))
        net_x, net_y = ((((DISPLAY_W-260)/2) - net_img.get_width()/2) - 5, DISPLAY_H-net_img.get_height()+10)
        self.background.blit(net_img, (net_x, net_y))
        self.net_rect = pygame.Rect((net_x + 135, net_y + 3), (net_img.get_width() - 3, 100))
        
        self.ball = Ball()
        self.ball.position.x, self.ball.position.y = DISPLAY_W/2, 200
        self.ball.acceleration.y = 0

    def play(self):
        ############# MAIN GAME LOOP #############
        while self.running:
            dt = self.clock.tick(60) * 0.001 * self.TARGET_FPS
            ############# CHECK PLAYER INPUT #############
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    self.show_throw_box = not self.show_throw_box

                self.check_player_keys(self.player_1, event)
                self.check_player_keys(self.player_2, event)

                self.test_ball_physics(event)
            
            ############# UPDATE PLAYER AND BALL #############
            self.player_1.update(dt)
            self.player_2.update(dt)
            
            if self.ball.rect.left < self.net_rect.right or self.ball.rect.right > self.net_rect.left:
                self.ball.handle_collision(self.net_rect)
            
            if self.ball.rect.centerx < 530:
                if self.ball.update(dt, self.player_1):
                    print("P1 bonk") # Debug info
            else:
                if self.ball.update(dt, self.player_2):
                    print("P2 bonk") # Debug info

            ############# HANDLE ANIMATIONS #############
            self.handle_animations(self.player_1, dt, self.spritesheet)
            self.handle_animations(self.player_2, dt, self.spritesheet)

            ############# UPDATE WINDOW AND DISPLAY #############
            self.canvas.fill((58, 57, 57))
            self.canvas.blit(self.background, (133, 0))
            self.player_1.draw(self.canvas)
            self.player_2.draw(self.canvas)
            self.ball.draw(self.canvas)

            # Debug info, comment/uncomment as needed
            self.show_rects()
            # self.show_kinetic_data(self.ball)
            if self.show_throw_box:
                throw_pos_1, throw_vel_1 = self.player_1.get_ball_throw_info()
                throw_pos_2, throw_vel_2 = self.player_2.get_ball_throw_info()
                self.draw_throw_pos(throw_pos_1, throw_pos_2)

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
            elif event.key == player.THROW_KEY:
                player.in_animation = True
                player.sel_animation = False
        
        if event.type == pygame.KEYUP:
            if event.key == player.LEFT_KEY:
                player.LEFT_KEY_PRESSED = False
            elif event.key == player.RIGHT_KEY:
                player.RIGHT_KEY_PRESSED = False
            elif event.key == player.UP_KEY:
                if player.is_jumping:
                    player.velocity.y *= 0.5 
                    player.is_jumping = False

    def throw_ball(self, player: Player):
        throw_pos, throw_vel = player.get_ball_throw_info()
        if not self.round_started:
            self.round_started = True
            self.ball.throw(throw_pos, throw_vel)

    def handle_animations(self, player: Player, dt: float, spritesheet: Spritesheet):
        if abs(self.ball.rect.centerx - player.rect.centerx) < 150:
            player.in_animation = True
            player.sel_animation = True

        if player.in_animation:
            player.handle_animations(dt, spritesheet, self.ball.rect)
            
            if not player.in_animation and not player.sel_animation:
                self.throw_ball(player)

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
        # players' png box
        pygame.draw.rect(self.canvas, (255, 255, 255), self.player_1.rect, 1)
        pygame.draw.rect(self.canvas, (255, 255, 255), self.player_2.rect, 1)
        
        # ball's collision/png box
        pygame.draw.rect(self.canvas, (0, 0, 0), self.ball.rect, 1)

        # net's collision box
        x, y = self.net_rect.topleft
        width = self.net_rect.width
        pygame.draw.rect(self.canvas, (0, 0, 0), self.net_rect, 1) # Whole
        pygame.draw.rect(self.canvas, (250, 0, 0), pygame.Rect(x, y, width, width), 1) # Vertical bounce
        
        # players' collision box
        x, y = self.player_1.collide_rect.topleft
        width = self.player_1.collide_rect.width
        pygame.draw.rect(self.canvas, (0, 0, 0), self.player_1.collide_rect, 1) # Whole
        pygame.draw.rect(self.canvas, (250, 0, 0), pygame.Rect(x, y, width, width), 1) # Vertical bounce
        x, y = self.player_2.collide_rect.topleft
        width = self.player_2.collide_rect.width
        pygame.draw.rect(self.canvas, (0, 0, 0), self.player_2.collide_rect, 1) # Whole
        pygame.draw.rect(self.canvas, (250, 0, 0), pygame.Rect(x, y, width, width), 1) # Vertical bounce
    
    def draw_throw_pos(self, throw_pos_1: pygame.math.Vector2, throw_pos_2: pygame.math.Vector2):
        throw_box_1 = pygame.Rect(0, 0, 32, 32)
        throw_box_1.topleft = throw_pos_1.x, throw_pos_1.y
        pygame.draw.rect(self.canvas, (255, 255, 255), throw_box_1, 1)

        throw_box_2 = pygame.Rect(0, 0, 32, 32)
        throw_box_2.topleft = throw_pos_2.x, throw_pos_2.y
        pygame.draw.rect(self.canvas, (255, 255, 255), throw_box_2, 1)
    
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
