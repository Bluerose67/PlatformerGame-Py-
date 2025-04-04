import pygame
from config import Config
from game.systems.animation import Animation, Animator

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animator = Animator()
        self._load_animations()
        self.image = self.animator.get_current_frame()
        self.rect = self.image.get_rect(topleft=pos)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.facing_right = True

    def _load_animations(self):
        idle_frames = [Config.load_image(f"player/idle_{i}.png") for i in range(4)]
        run_frames = [Config.load_image(f"player/run_{i}.png") for i in range(6)]
        
        self.animator.add_animation("idle", Animation(idle_frames, 10))
        self.animator.add_animation("run", Animation(run_frames, 5))

    def update(self, tiles):
        self._handle_input()
        self._apply_physics(tiles)
        self._update_animation()
        self._check_bounds()

    def _handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        
        if keys[pygame.K_a]:
            self.velocity.x = -Config.PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_d]:
            self.velocity.x = Config.PLAYER_SPEED
            self.facing_right = True
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity.y = Config.JUMP_FORCE
            self.on_ground = False

    def _update_animation(self):
        if abs(self.velocity.x) > 0:
            self.animator.play("run")
        else:
            self.animator.play("idle")
        
        self.image = self.animator.get_current_frame()
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)