import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 32
PLAYER_SPEED = 5
GRAVITY = 0.8
JUMP_FORCE = -15

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, GRAVITY)
        self.on_ground = False

    def update(self, tiles):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
        elif keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED
        else:
            self.velocity.x = 0

        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity.y = JUMP_FORCE
            self.on_ground = False

        # Apply physics
        self.velocity += self.acceleration
        self.rect.x += self.velocity.x
        self.collide(self.velocity.x, 0, tiles)
        self.rect.y += self.velocity.y
        self.collide(0, self.velocity.y, tiles)

    def collide(self, x_vel, y_vel, tiles):
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if x_vel > 0:
                    self.rect.right = tile.rect.left
                if x_vel < 0:
                    self.rect.left = tile.rect.right
                if y_vel > 0:
                    self.rect.bottom = tile.rect.top
                    self.on_ground = True
                    self.velocity.y = 0
                if y_vel < 0:
                    self.rect.top = tile.rect.bottom
                    self.velocity.y = 0

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=pos)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = 1
        self.speed = 2

    def update(self, tiles):
        self.rect.x += self.speed * self.direction
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                self.direction *= -1
                self.rect.x += self.speed * self.direction

level = [
    "                            ",
    "                            ",
    "                            ",
    " XX    XXX              XX  ",
    " XX P                       ",
    " XXXX        XX         XX  ",
    " XXXX      XX  E       XX   ",
    " XX    X  XXXX    XX  XXXXXX",
    "      XX  XXXXXX  XX  XXXXXX",
    "    XXXX  XXXXXX  XX  XXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

def generate_level(layout):
    tiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player = None

    for row_index, row in enumerate(layout):
        for col_index, cell in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if cell == "X":
                tiles.add(Tile((x, y)))
            elif cell == "P":
                player = Player()
                player.rect.topleft = (x, y)
            elif cell == "E":
                enemies.add(Enemy((x, y)))
    
    return player, tiles, enemies


def main():
    player, tiles, enemies = generate_level(level)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update
        player.update(tiles)
        enemies.update(tiles)
        
        # Check collisions
        if pygame.sprite.spritecollide(player, enemies, False):
            print("Game Over!")
            running = False
        
        # Draw
        screen.fill(BLACK)
        tiles.draw(screen)
        enemies.draw(screen)
        screen.blit(player.image, player.rect)
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()