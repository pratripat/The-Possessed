import pygame

class Health_Bar:
    def __init__(self, position, dimensions, max_health, image_path='health_bar'):
        self.position = position
        self.dimensions = dimensions
        self.max_health = max_health
        self.image = pygame.transform.scale(pygame.image.load(f'data/graphics/images/{image_path}.png'), dimensions)

    def render(self, surface, health, color, offset=[0,0]):
        surf = pygame.Surface(self.dimensions)
        surf.set_colorkey((0,0,0))
        pygame.draw.rect(surf, color, (*offset, (self.dimensions[0]-offset[0])/self.max_health*health, self.dimensions[1]-offset[1]))
        surf.blit(self.image, (0,0))
        surface.blit(surf, self.position)
