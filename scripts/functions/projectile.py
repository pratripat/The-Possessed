import pygame
from .funcs import *

class Projectile:
    def __init__(self, owner, targets, position, size, damage, timer):
        self.owner = owner
        self.targets = targets
        self.rect = pygame.Rect(*position, *size)
        self.damage = damage
        self.timer = timer
        self.destroyed = False

    #Checks for collision with the targets
    def update(self, camera):
        self.timer -= 1

        if self.timer <= 0:
            self.destroyed = True
            return

        for target in self.targets:
            if rect_rect_collision(self.rect, target.rect):
                target.damage(self.damage)
                camera.set_screen_shake(3, 7)
                self.destroyed = True
