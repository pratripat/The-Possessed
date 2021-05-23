import random

class Camera:
    def __init__(self):
        self.target = None
        self.scroll = [0,0]
        self.movement = 1
        self.screen_shake = 0.001
        self.time = 0

    def update(self, surface, restrainments=None):
        if self.time == 0:
            self.screen_shake = 0

        if self.target:
            self.scroll[0] += int((self.target.center[0]-self.scroll[0]-surface.get_width()/2) * self.movement + random.uniform(-self.screen_shake, self.screen_shake+1))
            self.scroll[1] += int((self.target.center[1]-self.scroll[1]-surface.get_height()/2) * self.movement + random.uniform(-self.screen_shake, self.screen_shake+1))

        if self.time > 0:
            self.time -= 1

        if restrainments:
            if self.scroll[0] < restrainments[0][0]:
                self.scroll[0] = restrainments[0][0]
            if self.scroll[0] > restrainments[0][1]-surface.get_width():
                self.scroll[0] = restrainments[0][1]-surface.get_width()
            if self.scroll[1] < restrainments[1][0]:
                self.scroll[1] = restrainments[1][0]
            if self.scroll[1] > restrainments[1][1]-surface.get_height():
                self.scroll[1] = restrainments[1][1]-surface.get_height()

    def set_target(self, target):
        self.target = target

    def set_movement(self, movement):
        self.movement = movement

    def set_screen_shake(self, screen_shake, time):
        self.screen_shake = screen_shake
        self.time = time
