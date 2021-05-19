import pygame

class Door:
    def __init__(self, position, tilemap):
        self.position = position
        self.load_image(tilemap)

    def load_image(self, tilemap):
        for tile in tilemap.entities:
            if tile['id'] == 'door':
                self.image = tile['image']
                break

        self.rect = pygame.Rect(*self.position, *self.image.get_size())

    def render(self, surface, scroll):
        surface.blit(self.image, [self.position[0]-scroll[0], self.position[1]-scroll[1]])
