import pygame
from config import Config
from game.systems.animation import Animation, Animator

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animator = Animator()
        self._load_animations()
        self.image = self.animator.get_current_frame()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.Vector2(-1, 0)
        self.speed = 2
        self.health = 100

    def _load_animations(self):
        anim_frames = {
            "walk": [Config.load_image(f"enemy/walk_{i}.png") for i in range(4)],
            "attack": [Config.load_image(f"enemy/attack_{i}.png") for i in range(6)]
        }
        self.animator.add_animation("walk", Animation(anim_frames["walk"], 8))
        self.animator.add_animation("attack", Animation(anim_frames["attack"], 5))
        self.animator.play("walk")

    def update(self, tiles, player):
        self._handle_movement(tiles)
        self._update_ai(player)
        self._update_animation()
        
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
        # Simple AI: Chase player if within range
        distance = player.rect.x - self.rect.x
        if abs(distance) < 300:
            self.direction.x = 1 if distance > 0 else -1
            
    def _update_animation(self):
        self.animator.update()
        self.image = self.animator.get_current_frame()
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)