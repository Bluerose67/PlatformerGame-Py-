import pygame
import csv
from config import *
from entities.player import Player
from objects.tile import Tile
from objects.background import Background
from objects.ui import UI
from objects.menu import Menu
from objects.game_over import GameOver
from objects.game_complete import GameComplete
from entities.enemy import Enemy
import pygame.mixer

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = "menu"  # menu, playing, game_over
        self.game_complete_screen = GameComplete(self.screen)
        self.menu = Menu(self.screen)
        self.game_over_screen = GameOver(self.screen)
        self.load_level()
        self.offset_x = 0
        self.offset_y = 0
        self.camera_borders = {"left": 200, "right": 100, "top": 100, "bottom": 100}
        self.background = Background()
        self.camera_offset = [0, 0]
        pygame.mixer.init()
        self.load_sounds()
        self.ui = UI()
        self.enemies = pygame.sprite.Group()
        self.spawn_enemies()

        self.debug_mode = True  # Set to False to disable prints

    def load_sounds(self):
        self.sounds = {
            "bg": pygame.mixer.Sound(os.path.join("assets", "sounds", "background.mp3")),
            "jump": pygame.mixer.Sound(os.path.join("assets", "sounds", "jump.mp3")),
            "hurt": pygame.mixer.Sound(os.path.join("assets", "sounds", "hurt.wav")),
            "game_over": pygame.mixer.Sound(os.path.join("assets", "sounds", "game_over.wav"))
        }
        self.sounds["bg"].set_volume(0.3)
        self.sounds["bg"].play(-1)  # Loop background music

    def update(self, tiles):
        self.patrol(tiles)
        self.apply_gravity()
        
        # Store previous position for stability check
        prev_y = self.rect.y
        
        # Vertical movement first
        self.rect.y += self.y_vel
        self.handle_collisions(tiles, 0, self.y_vel)
        
        # Horizontal movement after vertical resolution
        self.rect.x += self.x_vel
        self.handle_collisions(tiles, self.x_vel, 0)
        
        # Snap to ground if barely moving vertically
        if abs(self.rect.y - prev_y) < 1 and self.grounded:
            self.rect.bottom = self.last_grounded_y
        
        self.update_sprite()

    def handle_enemy_collision(self, enemy):
        # Check if player is stomping from above
        if (self.player.rect.bottom < enemy.rect.centery and 
            self.player.y_vel > 0):  # Falling onto enemy
            enemy.kill()
            self.player.y_vel = -15  # Bounce effect
            self.sounds["jump"].play()  # Play bounce sound
        else:
            self.handle_player_damage()
        
    def spawn_enemies(self):
        # Ground-level slime
        # self.enemies.add(Enemy(200, HEIGHT - 1000, "slime"))  # 150px above bottom
        
        # # Elevated worm on a platform
        # self.enemies.add(Enemy(607, 328, "worm"))  # Absolute Y-position
        
        # # Far-left slime with shorter patrol
        # slime_left = Enemy(50, HEIGHT - 500, "slime")
        # slime_left.patrol_distance = 100  # Custom patrol range
        # self.enemies.add(slime_left)
        enemy = Enemy(3528, 480, "worm")
        self.enemies.add(enemy)
        enemy = Enemy(704, 512, "slime")
        self.enemies.add(enemy)
        enemy = Enemy(2744, 896, "slime")
        self.enemies.add(enemy)
        


    def load_level(self):
        self.tiles = pygame.sprite.Group()
        self.player = Player(704, 512)
        
        with open(os.path.join(LEVELS_DIR, "level_02.csv")) as f:
            reader = csv.reader(f)
            for y, row in enumerate(reader):
                for x, tile_id in enumerate(row):
                    if int(tile_id) >= 0:
                        tile = Tile(x*TILE_SIZE, y*TILE_SIZE, int(tile_id))
                        self.tiles.add(tile)

    def update_camera(self):
        # Update camera offset to follow player
        target_x = self.player.rect.centerx - WIDTH // 2
        target_y = self.player.rect.centery - HEIGHT // 2
        
        # Smooth camera movement (LERP)
        self.camera_offset[0] += (target_x - self.camera_offset[0]) * 0.1
        self.camera_offset[1] += (target_y - self.camera_offset[1]) * 0.1
        
        # Clamp to level boundaries
        self.camera_offset[0] = max(0, min(self.camera_offset[0], LEVEL_WIDTH - WIDTH))
        self.camera_offset[1] = max(0, min(self.camera_offset[1], LEVEL_HEIGHT - HEIGHT))

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        self.player.x_vel = 0
        
        if keys[pygame.K_LEFT]:
            self.player.x_vel = -PLAYER_VEL
            self.player.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.player.x_vel = PLAYER_VEL
            self.player.direction = "right"
        if keys[pygame.K_SPACE] and self.player.jump_count < 2:
            self.player.y_vel = -GRAVITY * 15
            self.player.jump_count += 1

    def apply_gravity(self):
        self.player.y_vel += GRAVITY
        self.player.rect.y += self.player.y_vel

    def handle_collisions(self):
        # Horizontal collisions
        self.player.rect.x += self.player.x_vel
        for tile in self.tiles:
            if tile.rect.colliderect(self.player.rect):
                if tile.name == "danger":
                    self.handle_player_damage()
                if tile.name == "goal":
                    self.state ="complete"
                if tile.name == "solid":
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
            if pygame.sprite.collide_mask(self.player, enemy):
                self.handle_enemy_collision(enemy)

    def handle_player_damage(self):
        if self.player.take_damage():  # Only proceed if player wasn't invincible
            if self.ui.take_damage():  # Only proceed if player had hearts remaining
                self.sounds["hurt"].play()
                # Apply knockback
                knockback_dir = -1 if self.player.direction == "right" else 1
                self.player.x_vel = knockback_dir * 15
                self.player.y_vel = -10
            else:
                # No hearts left - game over
                self.game_over()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press 'P' to print
                    print(f"Snapshot: X={self.player.rect.x}, Y={self.player.rect.y}")

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.background.draw(self.screen, self.camera_offset)
        
        # Draw all tiles
        for tile in self.tiles:
            tile.draw(self.screen, self.camera_offset[0], self.camera_offset[1])
        
        # Draw player (will handle its own visibility)
        self.player.draw(self.screen, self.camera_offset[0], self.camera_offset[1])
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_offset[0], self.camera_offset[1])
        
        # Draw UI
        self.ui.draw(self.screen)
        
        pygame.display.update()
        
        if self.debug_mode:
            # Player world coordinates (without camera offset)
            print(f"Player World Position: X={self.player.rect.x}, Y={self.player.rect.y}")
        
        # Enemy world coordinates
        for i, enemy in enumerate(self.enemies):
            print(f"Enemy {i} World Position: X={enemy.rect.x}, Y={enemy.rect.y}")

        # Debug draw (temporary)
        # for enemy in self.enemies:
        #     pygame.draw.rect(self.screen, (255,0,0), 
        #         pygame.Rect(
        #             enemy.rect.x - self.camera_offset[0],
        #             enemy.rect.y - self.camera_offset[1],
        #             enemy.rect.width,
        #             enemy.rect.height
        #         ), 1)
    
    def reset_game(self):
        """Properly reset the game state"""
        self.tiles.empty()
        self.enemies.empty()
        self.load_level()
        self.ui = UI()
        self.spawn_enemies()
        self.camera_offset = [0, 0]
        self.player = Player(704, 512, self)
        self.state = "playing"  # Ensure we're in playing state
            

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.state == "menu":
                result = self.menu.handle_input()
                if result == "Play":
                    self.reset_game()
                    self.state = "playing"
                elif result == "Quit":
                    running = False
                self.menu.draw()
                
            elif self.state == "playing":
                self.handle_movement()
                self.handle_collisions()
                self.player.update()
                self.enemies.update(self.tiles)
                self.player.update_animation()
                self.update_camera()
                self.draw()
                
                if self.ui.hearts <= 0:
                    self.state = "game_over"
                    
            elif self.state == "game_over":
                if self.game_over_screen.handle_input():
                    self.state = "menu"
                    self.reset_game()
                self.game_over_screen.draw()
            elif self.state == "complete":
                if self.game_complete_screen.handle_input():
                    self.state = "menu"
                self.game_complete_screen.draw()

            pygame.display.update()
            if self.debug_mode:
                for enemy in self.enemies:
                    print(f"Enemy Position - World: ({enemy.rect.x}, {enemy.rect.y}) | Screen: ({enemy.rect.x - self.camera_offset[0]}, {enemy.rect.y - self.camera_offset[1]})")



        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
