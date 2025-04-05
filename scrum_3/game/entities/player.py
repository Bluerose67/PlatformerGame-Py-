import pygame
from config import Config
from game.systems.animation import Animation, Animator

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.health = 3
        self.animator = Animator()
        self._load_animations()
        self.image = self.animator.get_current_frame()
        self.rect = self.image.get_rect(topleft=pos)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.facing_right = True   

    def _load_animations(self):
        # Load available frames
        walk_frames = [
            Config.load_image("player/alienGreen_walk1.png"),
            Config.load_image("player/alienGreen_walk2.png")
        ]
        
        # Single frame animations
        idle_frame = [Config.load_image("player/alienGreen_stand.png")]
        jump_frame = [Config.load_image("player/alienGreen_jump.png")]

        # Setup animations
        self.animator.add_animation("idle", Animation(idle_frame, 1000))  # Long duration
        self.animator.add_animation("walk", Animation(walk_frames, 200))   # 200ms per frame
        self.animator.add_animation("jump", Animation(jump_frame, 100))
        
        self.animator.play("idle")

    def update(self, tiles):
        print(f"Pre-move position: {self.rect.topleft}")  # Debug position

        self._handle_input()
        self._apply_physics(tiles)  # Make sure this exists
        self._handle_collisions(tiles)
        self._update_animation()
        print(f"Post-move position: {self.rect.topleft}")  # Debug position


    def _handle_input(self):
        keys = pygame.key.get_pressed()
        print(f"Keys pressed: A={keys[pygame.K_a]}, D={keys[pygame.K_d]}, SPACE={keys[pygame.K_SPACE]}")
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
        # Determine animation state
        if not self.on_ground:
            self.animator.play("jump")
        elif abs(self.velocity.x) > 0:
            self.animator.play("walk")
        else:
            self.animator.play("idle")

        # Flip image if facing left
        self.image = self.animator.get_current_frame()
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def _handle_collisions(self, tiles):
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if tile.collision_type == "hazard":
                    self.take_damage()
                elif tile.is_solid():
                    return self.collision_type in ["solid", "platform"]
    
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill() 

    def _apply_physics(self, tiles):
        # Apply gravity
        self.velocity.y += Config.GRAVITY
        
        # Horizontal movement
        self.rect.x += self.velocity.x
        self._handle_collisions_x(tiles)
        
        # Vertical movement
        self.rect.y += self.velocity.y
        self._handle_collisions_y(tiles)

    def _handle_collisions_x(self, tiles):
        for tile in tiles:
            if tile.is_solid() and self.rect.colliderect(tile.rect):
                if self.velocity.x > 0:  # Moving right
                    self.rect.right = tile.rect.left
                elif self.velocity.x < 0:  # Moving left
                    self.rect.left = tile.rect.right

    def _handle_collisions_y(self, tiles):
        self.on_ground = False
        for tile in tiles:
            if tile.is_solid() and self.rect.colliderect(tile.rect):
                if self.velocity.y > 0:  # Falling down
                    self.rect.bottom = tile.rect.top
                    self.on_ground = True
                    self.velocity.y = 0
                elif self.velocity.y < 0:  # Jumping up
                    self.rect.top = tile.rect.bottom
                    self.velocity.y = 0