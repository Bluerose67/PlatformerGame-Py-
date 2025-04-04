import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1280, 720
CAMERA_BORDER = 300 
TILE_SIZE = 32
PLAYER_SPEED = 5
GRAVITY = 0.8
JUMP_FORCE = -15

#Creating the artwork
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#We initialize the screen
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
        
        # Player's Horizontal movement
        if keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
        elif keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED
        else:
            self.velocity.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity.y = JUMP_FORCE
            self.on_ground = False

        # For handeling physics
        self.velocity += self.acceleration
        self.rect.x += self.velocity.x
        self.collide(self.velocity.x, 0, tiles)
        self.rect.y += self.velocity.y
        self.collide(0, self.velocity.y, tiles)

        # For Keep player within screen bounds
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(HEIGHT, self.rect.bottom)

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

class Camera:
    def __init__(self):
        self.offset = pygame.math.Vector2(0, 0)
        self.width = WIDTH
        self.height = HEIGHT

    def update(self, target):
        # We should be able to center camera on player when near edges
        target_x = -target.rect.centerx + WIDTH/2
        target_y = -target.rect.centery + HEIGHT/2
        
        # For Smooth camera movement
        self.offset.x += (target_x - self.offset.x) * 0.05
        self.offset.y += (target_y - self.offset.y) * 0.05

class ParallaxBackground:
    def __init__(self):
        self.layers = [
            {"image": pygame.Surface((WIDTH, HEIGHT)), "speed": 0.2},
            {"image": pygame.Surface((WIDTH, HEIGHT)), "speed": 0.5}
        ]
        # Created simple background layers for parallax effect
        self.layers[0]["image"].fill((50, 50, 100)) 
        self.layers[1]["image"].fill((100, 100, 150))  
        
    def draw(self, screen, offset):
        for layer in self.layers:
            x = -offset.x * layer["speed"]
            screen.blit(layer["image"], (x, 0))

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
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    " XX    XXX                     XXX                         XXX              XX  ",
    " XX P                         XX  XX                     XX  XX                 ",
    " XXXX        XX         XX  XXXXXXXX        E          XXXXXXXXXX         XX   ",
    " XXXX      XX  E       XX  XXXXXXXXXX               XXXXXXXXXXXXXX      XX    ",
    " XX    X  XXXX    XX  XXXXXXXXXXXXXXXX    XXX     XXXXXXXXXXXXXXXXXX  XXXXXXX",
    "      XX  XXXXXX  XX  XXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "    XXXX  XXXXXX  XX  XXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
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
    camera = Camera()
    background = ParallaxBackground()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Necessary Update
        player.update(tiles)
        enemies.update(tiles)
        camera.update(player)

        
        # We Check the collisions here
        if pygame.sprite.spritecollide(player, enemies, False):
            print("Game Over!")
            running = False
        
    
        screen.fill(BLACK)
        background.draw(screen, camera.offset)
        
        for tile in tiles:
            screen.blit(tile.image, tile.rect.topleft + camera.offset)
        
        screen.blit(player.image, player.rect.topleft + camera.offset)
        for enemy in enemies:
            screen.blit(enemy.image, enemy.rect.topleft + camera.offset)
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()