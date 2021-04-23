import pygame, json, random
from .functions.dropped_item import Dropped_Item

class LootBox:
    def __init__(self, animations, position):
        self.animations = [animations.get_animation('closed_lootbox'), animations.get_animation('open_lootbox')]
        self.position = position
        self.current_animation = self.animations[0]
        self.opened = False

        self.load_weapons()

    def load_weapons(self):
        self.weapons = []
        for weapon_id in json.load(open('data/configs/weapons/weapons.json', 'r')).keys():
            for _ in range(json.load(open('data/configs/weapons/probability.json', 'r'))[weapon_id]):
                self.weapons.append(weapon_id)

    def render(self, surface, scroll):
        self.current_animation.render(surface, [self.position[0]-scroll[0], self.position[1]-scroll[1]])

    def run(self, dt):
        self.current_animation.run(dt)

    def open(self, dropped_entities):
        self.current_animation = self.animations[1]
        self.opened = True

        for i in range(2):
            dropped_entities.append(Dropped_Item(random.choice(self.weapons), self.center, [(i*2-1)*50, -10]))

    @property
    def rect(self):
        return pygame.Rect(*self.position, *self.current_animation.image.get_size())

    @property
    def center(self):
        return [self.position[0]+self.current_animation.image.get_width()/2, self.position[1]+self.current_animation.image.get_height()/2]
