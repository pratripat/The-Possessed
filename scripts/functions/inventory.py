import pygame

class Inventory:
    def __init__(self, n, position):
        self.n = n
        self.position = position
        self.size = 48
        self.items = [None for _ in range(self.n)]
        self.paths = ['' for _ in range(self.n)]
        self.item_background_image = pygame.transform.scale(pygame.image.load('data/graphics/images/icon_background.png'), (self.size, self.size))

    def render(self, surface):
        position = self.position.copy()

        for item in self.items:
            surface.blit(self.item_background_image, position, special_flags=pygame.BLEND_RGBA_ADD)
            if item:
                surface.blit(item, position)

            position[0] += self.size

    def add_item(self, id):
        if None in self.items:
            image_path = f'data/graphics/icons/inventory/{id}.png'
            image = pygame.transform.scale(pygame.image.load(image_path), (self.size, self.size))

            i = 0

            while i != len(self.items):
                if self.items[i] == None:
                    self.paths[i] = image_path
                    self.items[i] = image
                    break

                i += 1
