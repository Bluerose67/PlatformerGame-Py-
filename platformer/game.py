import pygame
import csv
from config import *
from entities.player import Player
from objects.tile import Tile
from objects.background import Background

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.load_level()
        self.offset_x = 0
        self.offset_y = 0
        self.camera_borders = {"left": 200, "right": 200, "top": 100, "bottom": 100}
        self.background = Background()
        self.camera_offset = [0, 0]
        

    def load_level(self):
        self.tiles = pygame.sprite.Group()
        self.player = Player(128, 128)
        
        with open(os.path.join(LEVELS_DIR, "level_02.csv")) as f:
            reader = csv.reader(f)
            for y, row in enumerate(reader):
                for x, tile_id in enumerate(row):
                    if int(tile_id) >= 0:
                        tile = Tile(x*TILE_SIZE, y*TILE_SIZE, int(tile_id))
                        self.tiles.add(tile)

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
                    print("Player damaged!")
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
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.background.draw(self.screen, self.camera_offset)

        for tile in self.tiles:
            tile.draw(self.screen, self.offset_x, self.offset_y)
        # Update player drawing
        self.screen.blit(self.player.image, 
                        (self.player.rect.x - self.offset_x, 
                         self.player.rect.y - self.offset_y))
        pygame.display.update()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_movement()
            self.handle_collisions()
            self.player.update_animation()
            self.update_camera()
            self.draw()

            # Camera follow
            if self.player.rect.right - self.offset_x > WIDTH - 300:
                self.offset_x = self.player.rect.right - (WIDTH - 300)
            if self.player.rect.left - self.offset_x < 300:
                self.offset_x = self.player.rect.left - 300

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()