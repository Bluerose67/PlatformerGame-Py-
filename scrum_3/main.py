import pygame
from game.world.level import Level
from game.systems.camera import Camera
from game.systems.particles import ParticleSystem
from game.ui.hud import HUD
from config import Config


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.level = Level("level_02.csv")
        self.camera = Camera(
            self.level.width, 
            self.level.height
        )
        self.particles = ParticleSystem()
        self.hud = HUD(self.level.player)

    def _update(self):
        self.particles.update()
        
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
        self.screen.fill(Config.BACKGROUND)
        self.particles.draw(self.screen)
        self.hud.draw(self.screen)
        
        # Draw tiles
        for tile in self.level.tiles:
            self.screen.blit(tile.image, tile.rect.topleft + self.camera.offset)
            
        # Draw entities
        for entity in self.level.entities:
            self.screen.blit(entity.image, entity.rect.topleft + self.camera.offset)
            
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()