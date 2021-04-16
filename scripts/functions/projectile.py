import pygame
from .funcs import *

class Projectile:
    def __init__(self, targets, position, size, damage, timer):
        self.targets = targets
        self.rect = pygame.Rect(*position, *size)
        self.damage = damage
        self.timer = timer
        self.destroyed = False

    #Checks for collision with the targets
    def update(self, camera, particles):
        self.timer -= 1

        if self.timer <= 0:
            self.destroyed = True
            return

        for target in self.targets:
            if rect_rect_collision(self.rect, target.rect):
                target.damage(self.damage)
                camera.set_screen_shake(3, 7)
                particles.add_particle([self.rect.x+self.rect.w/2, self.rect.y+self.rect.h/2], [0, -1], size=3, decrementation=0.5, intensity=2, color=(41,43,48), number=10)
                self.destroyed = True
