import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, color, velocity, lifespan):
        super().__init__()
        self.image = pygame.Surface((6, 6))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.velocity = pygame.Vector2(velocity)
        self.lifespan = lifespan
        self.age = 0

    def update(self):
        self.rect.center += self.velocity
        self.velocity.y += 0.5  # Gravity
        self.age += 1
        if self.age >= self.lifespan:
            self.kill()

class ParticleSystem:
    def __init__(self):
        self.particles = pygame.sprite.Group()
        
    def create_dust(self, pos):
        for _ in range(10):
            velocity = (
                random.uniform(-2, 2),
                random.uniform(-5, -2)
            )
            self.particles.add(Particle(
                pos, 
                (200, 200, 200), 
                velocity,
                random.randint(10, 20)
            ))
            
    def update(self):
        self.particles.update()
        
    def draw(self, screen):
        self.particles.draw(screen)