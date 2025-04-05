import pygame
from game.world.level import Level
from game.systems.camera import Camera
from game.systems.particles import ParticleSystem
from game.systems.background import ParallaxManager
from game.ui.hud import HUD
from config import Config


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        try:
            self.level = Level("level_02.csv")
        except Exception as e:
            print(f"Level loading failed: {e}")
            raise
        self.camera = Camera(
            self.level.width, 
            self.level.height
        )
        print(f"Level contains {len(self.level.tiles)} tiles")
        print(f"Level contains {len(self.level.entities)} entities")
        if not self.level.player:
            # Show exact CSV coordinates where player should be
            for y, row in enumerate(self.level.level_data):
                for x, tile_id in enumerate(row):
                    if tile_id == 99:
                        print(f"Player spawn marker found at ({x},{y}) but not processed!")
            raise ValueError("Player not found in level! Check CSV for ID 99")
        
        # Force initial camera position
        self.camera.offset.x = -self.level.player.rect.centerx + Config.WIDTH//2
        self.camera.offset.y = -self.level.player.rect.centery + Config.HEIGHT//2

        self.particles = ParticleSystem()
        self.hud = HUD(self.level.player)
        self.parallax = ParallaxManager()

        # Verify player exists
        # if not self.level.player:
        #     raise ValueError("No player spawn in level!")
        
    def _update(self, Enemy):
        # Update entities with proper arguments
        for entity in self.level.entities:
            if isinstance(entity, Enemy):
                entity.update(self.level.tiles, self.level.player)
            else:  # Player and other entities
                entity.update(self.level.tiles)
        # Update camera and background
        self.camera.update(self.level.player)
        self.parallax.update(self.camera.offset)
        
    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(Config.FPS)
            
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def _update(self):
        self.level.entities.update(self.level.tiles)
        self.camera.update(self.level.player)
        
    def _draw(self):
         # Clear screen with debug color
        self.screen.fill((30, 30, 30))  # Dark gray for contrast
        
        # 1. Draw parallax background (test without this first)
        # self.parallax.draw(self.screen)
        
        # 2. Draw tiles with debug borders
        for tile in self.level.tiles:
            screen_pos = tile.rect.topleft + self.camera.offset
            self.screen.blit(tile.image, screen_pos)
            pygame.draw.rect(self.screen, (255,0,0), (*screen_pos, *tile.rect.size), 1)  # Red borders
        
        # 3. Draw entities with debug markers
        for entity in self.level.entities:
            screen_pos = entity.rect.topleft + self.camera.offset
            self.screen.blit(entity.image, screen_pos)
            pygame.draw.circle(self.screen, (0,255,0), entity.rect.center + self.camera.offset, 5)  # Green center dot
        
        # 4. Draw player debug info
        if self.level.player:
            pygame.draw.rect(self.screen, (0,0,255), self.level.player.rect.move(self.camera.offset), 2)  # Blue border
            print(f"Player position: {self.level.player.rect.topleft}")  # Console debug

        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()