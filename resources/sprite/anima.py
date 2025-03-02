import pygame
from resources.sprite.spritesheet import Spritesheet

class Anima:
    def __init__(self):
        self.animations: dict[str, dict[str, list[pygame.Surface] | int]] = {}

    def create_animation(self, spritesheet: Spritesheet, route: str, name: str, duration_s: float, take_until: int = 20):
        frames: list[pygame.Surface] = []
        try:
            try:
                for i in range(take_until):
                    frames.append(spritesheet.parse_sprite(f"{route}_{i}.png"))
            except:
                for i in range(take_until):
                    num = "0" + str(i) if i < 10 else i
                    frames.append(spritesheet.parse_sprite(f"{route}_{num}.png"))
        except:
            print("Out of animation load by error: ", route)
        animation = {"frames": frames, "duration": duration_s}
        self.animations[name] = animation

    def play_animation(self, display: pygame.Surface, name: str, time: float, dest: tuple[float, float]):
        frame_id = self.calculate_frame(name, time)
        if frame_id >= len(self.animations[name]["frames"]):
            return True
        self.draw_frame(display, name, frame_id, dest)
        return False
    
    def animate_player(self, player, name: str, time: float):
        frame_id = self.calculate_frame(name, time)
        if frame_id >= len(self.animations[name]["frames"]):
            return True
        image = self.animations[name]["frames"][frame_id]
        player.image = image if image.get_size() == player.image.get_size() else pygame.transform.scale(image, player.image.get_size())
        return False
    
    def calculate_frame(self, name: str, time: float):
        gap = self.animations[name]["duration"] / len(self.animations[name]["frames"])
        frame = int(time / gap)
        return frame
    
    def draw_frame(self, display: pygame.Surface, name: str, frame_id: int, dest: tuple[float, float] = (0, 0)):
        frame = self.animations[name]["frames"][frame_id]
        display.blit(frame, dest)
