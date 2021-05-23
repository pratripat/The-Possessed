import math, random
from .boss import Boss
from .functions.health_bar import Health_Bar
from .functions.projectile import Projectile

class Eye(Boss):
    def __init__(self, game, animations, position):
        super().__init__(animations, 'eye', position, 'moving')
        self.game = game
        self.max_health = 600
        self.health = self.max_health
        self.damage_amount = 10
        self.speed = 3
        self.phase = 0
        self.angle = 0
        self.warp_timer = 0
        self.x_counter = self.y_counter = 0
        self.health_bar = Health_Bar([300, 10], [800, 33], self.max_health, 'boss_health_bar')

    def run(self, dt, gravity, projectiles, player):
        super().run(dt, 0)

        self.update_attrs()
        self.attack()

        if self.warp_timer > 0:
            position = [self.position[0]-self.game.camera.scroll[0], self.position[1]-self.game.camera.scroll[1]]

            position[0] %= self.game.screen.get_width()
            position[1] %= self.game.screen.get_height()

            self.position = [position[0]+self.game.camera.scroll[0], position[1]+self.game.camera.scroll[1]]

            self.velocity = [20, 20]
            self.warp_timer -= self.game.dt

            dx = self.velocity[0]
            dy = self.velocity[1]

            self.angle = -math.degrees(math.atan2(dy, dx))

            return

        dx = player.position[0]-self.center[0]
        dy = player.position[1]-self.center[1]
        self.velocity = [player.position[0]-self.position[0], player.position[1]-self.position[1]]

        self.x_counter += 0.05
        self.y_counter += 0.02

        self.warp_timer = 0

        self.angle = -math.degrees(math.atan2(dy, dx))

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

    def attack(self):
        self.game.projectiles.append(Projectile(self, [self.game.entity_manager.player], self.position.copy(), self.image.get_size(), self.damage_amount, 2))

        if self.phase == 1:
            if self.warp_timer == 0 and random.randint(1, 100) == 1:
                self.warp_timer = 1

    def update_attrs(self):
        if self.health <= self.max_health*3/4:
            self.phase = 1
