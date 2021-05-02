import math
from .boss import Boss
from .functions.health_bar import Health_Bar

class Eye(Boss):
    def __init__(self, animations, position):
        super().__init__(animations, 'eye', position, 'moving')
        self.max_health = 600
        self.health = self.max_health
        self.speed = 3
        self.phase = 0
        self.angle = 0
        self.x_counter = self.y_counter = 0

        self.health_bar = Health_Bar([300, 10], [800, 33], self.max_health, 'boss_health_bar')

    def run(self, dt, gravity, projectiles, player):
        super().run(dt, 0)

        dx = player.position[0]-self.center[0]
        dy = player.position[1]-self.center[1]

        self.angle = -math.degrees(math.atan2(dy, dx))

        self.x_counter += 0.05
        self.y_counter += 0.02

        self.velocity = [player.position[0]-self.position[0], player.position[1]-self.position[1]]
        magnitude = math.sqrt(self.velocity[0]*self.velocity[0]+self.velocity[1]*self.velocity[1])
        self.velocity[0] /= magnitude
        self.velocity[1] /= magnitude

        self.velocity[0] *= self.speed
        self.velocity[1] *= self.speed

        self.position[0] += math.cos(self.x_counter)*5
        self.position[1] += math.cos(self.y_counter)*2-3

    def move(self, collidables, dt):
        super().move([], dt)

    def render(self, surface, scroll):
        super().render(surface, scroll, angle=self.angle)
