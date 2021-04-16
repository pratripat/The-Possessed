import pygame

class Health_Bar:
    def __init__(self, position, dimensions, max_health):
        self.position = position
        self.dimensions = dimensions
        self.max_health = max_health
        self.image = pygame.transform.scale(pygame.image.load('data/graphics/images/health_bar.png'), dimensions)

    def render(self, surface, health, color):
        surf = pygame.Surface(self.dimensions)
        pygame.draw.rect(surf, color, (0, 0, self.dimensions[0]/self.max_health*health, self.dimensions[1]))
        surf.blit(self.image, (0,0))
        surf.set_colorkey((0,0,0))
        surface.blit(surf, self.position)
