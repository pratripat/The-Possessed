import pygame
from .dropped_item import Dropped_Item

class Inventory:
    def __init__(self, owner, position, data):
        self.size = 48
        self.owner = owner
        self.position = position
        self.ids = data['inventory_ids']
        self.items = data['inventory_items']
        self.item_background_image = pygame.transform.scale(pygame.image.load('data/graphics/images/icon_background.png').convert(), (self.size, self.size))
        self.item_background_image.set_colorkey((0,0,0))
        self.current_item_index = data['inventory_current_item_index']

    def render(self, surface):
        position = self.position.copy()

        for i, item in enumerate(self.items):
            if i == self.current_item_index:
                surf = pygame.Surface((48,48))
                surf.fill((255,232,225))
                surface.blit(surf, position, special_flags=pygame.BLEND_RGBA_ADD)
            else:
                surface.blit(self.item_background_image, position, special_flags=pygame.BLEND_RGBA_ADD)

            if item:
                surface.blit(item, position)

            position[0] += self.size

    def add_item(self, id):
        if None in self.items:
            image_path = f'data/graphics/icons/inventory/{id}.png'
            image = pygame.transform.scale(pygame.image.load(image_path).convert(), (self.size, self.size))
            image.set_colorkey((0,0,0))

            i = 0

            while i != len(self.items):
                if self.items[i] == None:
                    self.ids[i] = id
                    self.items[i] = image
                    break

                i += 1

    def select_next_item(self):
        self.current_item_index += 1
        self.current_item_index %= 2

    def get_current_item_id(self):
        return self.ids[self.current_item_index]

    def pick_item(self, id, dropped_entities):
        image_path = f'data/graphics/icons/inventory/{id}.png'
        image = pygame.transform.scale(pygame.image.load(image_path).convert(), (self.size, self.size))
        image.set_colorkey((0,0,0))

        self.drop_item(dropped_entities)

        self.ids[self.current_item_index] = id
        self.items[self.current_item_index] = image

    def drop_item(self, dropped_entities):
        if self.ids[self.current_item_index] != '':
            entity = Dropped_Item(self.ids[self.current_item_index], self.owner.position, [0,-10])
            dropped_entities.append(entity)

            self.ids[self.current_item_index] = ''
            self.items[self.current_item_index] = None
