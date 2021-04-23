import pygame

class Skill:
    def __init__(self, type, max_waiting_timer, max_using_timer):
        self.type = type
        self.icon = pygame.transform.scale(pygame.image.load(f'data/graphics/icons/skills/{self.type}.png').convert(), (48,48))
        self.icon.set_colorkey((0,0,0))
        self.max_waiting_timer = max_waiting_timer
        self.max_using_timer = max_using_timer
        self.using_timer = 0
        self.waiting_timer = 0

    def use(self):
        self.waiting_timer = self.max_waiting_timer
        self.using_timer = self.max_using_timer

    def render_icon(self, surface, position):
        surface.blit(self.icon, position)

    def update(self, dt):
        if self.waiting_timer > 0:
            self.waiting_timer -= dt

        if self.using_timer > 0:
            self.using_timer -= dt

        if round(self.waiting_timer) <= 0:
            self.waiting_timer = 0

        if round(self.using_timer) <= 0:
            self.using_timer = 0

    @property
    def used(self):
        return self.using_timer > 0
