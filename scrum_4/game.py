import pygame
import csv
import os
from config import *
from entities.player import Player
from entities.enemy import Enemy
from objects.tile import Tile
from objects.background import Background
from objects.ui import UI
from objects.menu import Menu
import pygame.mixer

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Platformer")
        self.clock = pygame.time.Clock()
        
        # Game state management
        self.state = "menu"  # menu, playing, game_over
        self.menu = Menu()
        
        # Initialize systems
        pygame.mixer.init()
        self.load_sounds()
        
        # Game objects
        self.background = Background()
        self.reset_game(load_level=False)  # Don't load level until playing

    def reset_game(self, load_level=True):
        """Reset game state"""
        self.player = Player(128, 128, self)
        self.tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.ui = UI()
        self.camera_offset = [0, 0]
        
        if load_level:
            self.level_width, self.level_height = self.load_level()
            self.camera_offset = [0, max(0, self.level_height - HEIGHT)]
            self.spawn_enemies()

    def load_level(self):
        with open(os.path.join(LEVELS_DIR, "level_02.csv")) as f:
            reader = csv.reader(f)
            rows = list(reader)
            level_height = len(rows) * TILE_SIZE
            level_width = len(rows[0]) * TILE_SIZE
            vertical_offset = HEIGHT - level_height
            
            # Clear existing enemies before spawning new ones
            self.enemies.empty()
            
            for y, row in enumerate(rows):
                for x, tile_id in enumerate(row):
                    tile_id = int(tile_id)
                    if tile_id >= 0:
                        tile_y = (y * TILE_SIZE) + vertical_offset
                        tile = Tile(x * TILE_SIZE, tile_y, tile_id)
                        self.tiles.add(tile)
                        
                        # Spawn only ONE enemy per marker
                        if tile_id == 15 and not any(e for e in self.enemies if e.enemy_type == "slime"):
                            enemy = Enemy(x * TILE_SIZE, tile_y - SCALED_TILE, "slime")
                            enemy.start_x = x * TILE_SIZE
                            self.enemies.add(enemy)
                        elif tile_id == 11 and not any(e for e in self.enemies if e.enemy_type == "worm"):
                            enemy = Enemy(x * TILE_SIZE, tile_y - SCALED_TILE, "worm")
                            enemy.start_x = x * TILE_SIZE
                            self.enemies.add(enemy)
        
            return (level_width, level_height)

    def load_sounds(self):
        """Initialize game sounds"""
        self.sounds = {
            "bg": pygame.mixer.Sound(os.path.join("assets", "sounds", "background.mp3")),
            "jump": pygame.mixer.Sound(os.path.join("assets", "sounds", "jump.mp3")),
            "hurt": pygame.mixer.Sound(os.path.join("assets", "sounds", "hurt.wav")),
            "game_over": pygame.mixer.Sound(os.path.join("assets", "sounds", "game_over.wav"))
        }
        # Set volumes
        self.sounds["bg"].set_volume(0.3)
    
        # Stop any currently playing music first
        pygame.mixer.stop()  
        # Start background music (loop forever)
        self.sounds["bg"].play(-1)  

    def spawn_enemies(self):
        """Spawn enemies on top of platform tiles"""
        for tile in self.tiles:
            if tile.tile_id == 15:  # Slime spawn marker
                self.enemies.add(Enemy(
                    tile.rect.x, 
                    tile.rect.y - SCALED_TILE,  # Spawn above the platform
                    "slime"
                ))
            elif tile.tile_id == 11:  # Worm spawn marker
                self.enemies.add(Enemy(
                    tile.rect.x,
                    tile.rect.y - SCALED_TILE,  # Spawn above the platform
                    "worm"
                ))

    def run(self):
        """Main game loop"""
        running = True
        while running:
            self.clock.tick(FPS)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # State management
            if self.state == "menu":
                self.handle_menu()
            elif self.state == "playing":
                self.handle_gameplay()
            elif self.state == "game_over":
                self.handle_game_over()
            
            # Drawing
            self.screen.fill((0, 0, 0))
            self.background.draw(self.screen, self.camera_offset)
            
            if self.state == "menu":
                self.menu.draw(self.screen)
            elif self.state == "playing":
                self.draw_game()
            elif self.state == "game_over":
                self.draw_game_over()
            
            pygame.display.update()

        pygame.quit()
        quit()

    def handle_menu(self):
        selection = self.menu.handle_input()
        if selection == "Play":
            self.state = "playing"
            self.reset_game()
            # Ensure music is playing (but not duplicated)
            if not pygame.mixer.get_busy():
                self.sounds["bg"].play(-1)
        elif selection == "Quit":
            pygame.quit()
            quit()

    def handle_gameplay(self):
        """Main game logic"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.state = "menu"
            return
            
        self.handle_movement()
        self.handle_collisions()
        self.update_camera()
        self.enemies.update()

    def handle_game_over(self):
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            self.state = "menu"
            # Restart music when returning to menu
            self.sounds["bg"].play(-1)

    def draw_game(self):
        """Draw all game objects"""
        # Draw tiles
        for tile in self.tiles:
            tile.draw(self.screen, self.camera_offset[0], self.camera_offset[1])
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_offset[0], self.camera_offset[1])
        
        # Draw player
        self.player.update_animation()
        self.screen.blit(self.player.image, 
                        (self.player.rect.x - self.camera_offset[0],
                         self.player.rect.y - self.camera_offset[1]))
        
        # Draw UI
        self.ui.draw(self.screen)

    def draw_game_over(self):
        """Draw game over screen"""
        game_over_text = pygame.font.SysFont("Arial", 72).render("GAME OVER", True, WHITE)
        instruction_text = pygame.font.SysFont("Arial", 36).render("Press ENTER to continue", True, (200, 200, 200))
        
        self.screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        self.screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT//2 + 50))

    def handle_movement(self):
        """Handle player movement input"""
        keys = pygame.key.get_pressed()
        self.player.x_vel = 0
        
        if keys[pygame.K_LEFT]:
            self.player.x_vel = -PLAYER_VEL
            self.player.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.player.x_vel = PLAYER_VEL
            self.player.direction = "right"
        if keys[pygame.K_SPACE] and self.player.jump_count < 2:
            self.player.jump()
            self.sounds["jump"].play()

    def apply_gravity(self):
        """Apply gravity to player"""
        self.player.y_vel += GRAVITY
        self.player.rect.y += self.player.y_vel

    def handle_collisions(self):
        """Handle all game collisions"""
        # Horizontal collisions
        self.player.rect.x += self.player.x_vel
        for tile in self.tiles:
            if tile.rect.colliderect(self.player.rect):
                if tile.name == "danger":
                    if self.ui.take_damage():
                        self.state = "game_over"
                elif tile.name == "solid":
                    if self.player.x_vel > 0:
                        self.player.rect.right = tile.rect.left
                    elif self.player.x_vel < 0:
                        self.player.rect.left = tile.rect.right

        # Vertical collisions
        self.apply_gravity()
        for tile in self.tiles:
            if tile.rect.colliderect(self.player.rect):
                if tile.name == "solid":
                    if self.player.y_vel > 0:
                        self.player.rect.bottom = tile.rect.top
                        self.player.jump_count = 0
                    elif self.player.y_vel < 0:
                        self.player.rect.top = tile.rect.bottom
                    self.player.y_vel = 0

        # Enemy collisions
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self.player, enemy):
                if self.ui.take_damage():
                    self.state = "game_over"
                    self.sounds["game_over"].play()
                else:
                    self.sounds["hurt"].play()
                    # Knockback effect
                    self.player.rect.x += -50 if enemy.x_vel > 0 else 50

    def update_camera(self):
        # Directly center camera on player
        self.camera_offset[0] = self.player.rect.centerx - WIDTH // 2
        self.camera_offset[1] = self.player.rect.centery - HEIGHT // 2
        
        # Clamp to level boundaries
        self.camera_offset[0] = max(0, min(self.camera_offset[0], self.level_width - WIDTH))
        self.camera_offset[1] = max(0, min(self.camera_offset[1], self.level_height - HEIGHT))

if __name__ == "__main__":
    game = Game()
    game.run()