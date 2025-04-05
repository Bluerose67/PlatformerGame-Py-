import pygame
from config import Config
from game.systems.animation import Animation, Animator

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, enemy_type: str):
        super().__init__()
        self.enemy_type = enemy_type.lower()  # 'slime' or 'worm'
        self.animator = Animator()
        self._load_animations()
        self.image = self.animator.get_current_frame()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.Vector2(-1, 0)
        self.speed = 3 if "worm" in self.enemy_type else 2
        self.health = 100

    def _load_animations(self):
        # Load only walk animations
        walk_frames = []
        
        if self.enemy_type == "slime":
            walk_frames = [
                Config.load_image("enemy/Slimeidle_1.png"),
                Config.load_image("enemy/Slimewalk_2.png")
            ]
        elif self.enemy_type == "worm":
            walk_frames = [
                Config.load_image("enemy/wormGreen_idle.png"),
                Config.load_image("enemy/wormGreen_walk.png")
            ]

        self.animator.add_animation("walk", Animation(walk_frames, 200))
        self.animator.play("walk")

    def update(self, tiles, player):
        self._handle_movement(tiles)
        self._update_ai(player)
        self.animator.update()
        self._update_direction()
        
    def _handle_movement(self, tiles):
        self.rect.x += self.direction.x * self.speed
        if self._check_collisions(tiles):
            self.direction.x *= -1
            
    def _check_collisions(self, tiles):
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                return True
        return False
    
    def _update_ai(self, player):
        if player is None:
         return
        # Simple AI: Chase player if within range
        distance = player.rect.x - self.rect.x
        if abs(distance) < 300:
            self.direction.x = 1 if distance > 0 else -1
            