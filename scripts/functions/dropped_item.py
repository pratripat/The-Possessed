import pygame
from .funcs import *

class Dropped_Item:
    def __init__(self, id, position, velocity):
        self.id = id
        self.velocity = velocity
        self.image = pygame.image.load(f'data/graphics/icons/inventory/{self.id}.png').convert()
        self.image.set_colorkey((0,0,0))
        self.position = [position[0]-self.image.get_width()/2, position[1]]

    def render(self, surface, scroll):
        surface.blit(self.image, [self.position[0]-scroll[0], self.position[1]-scroll[1]])

    def update(self, dt, gravity, rects):
        self.velocity[1] += 1

        self.position[0] += round(self.velocity[0]*dt*80)
        hit_list = self.get_colliding_objects(rects)
        rect = self.rect

        for obj in hit_list:
            if self.velocity[0] > 0:
                rect.right = obj.left
                self.position[0] = rect.x
            if self.velocity[0] < 0:
                rect.left = obj.right
                self.position[0] = rect.x

        self.position[1] += round(self.velocity[1]*dt*80)
        hit_list = self.get_colliding_objects(rects)
        rect = self.rect

        for obj in hit_list:
            if self.velocity[1] > 0:
                rect.bottom = obj.top
                self.position[1] = rect.y
            if self.velocity[1] < 0:
                rect.top = obj.bottom
                self.position[1] = rect.y

        self.velocity[0] *= 0.1
        self.velocity[1] *= 0.9

    def get_colliding_objects(self, rects):
        hit_list = []
        for rect in rects:
            if rect_rect_collision(self.rect, rect):
                hit_list.append(rect)

        return hit_list

    @property
    def rect(self):
        return pygame.Rect(*self.position, *self.image.get_size())
