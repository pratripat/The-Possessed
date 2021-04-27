import pygame, math, random
from .boss import Boss
from .functions.health_bar import Health_Bar
from .functions.projectile import Projectile

class Blob:
    def __init__(self, player, position, velocity=None):
        self.image = pygame.image.load('data/graphics/images/octo_projectile.png').convert()
        self.image.set_colorkey((0,0,0))
        self.damage = 10
        self.speed = 5

        self.position = [position[0]-self.image.get_width()/2, position[1]-self.image.get_height()/2]
        self.velocity = self.normalized_vector(player, velocity)

        blob_sound_sfx = pygame.mixer.Sound('data/sfx/blob_sound.wav')
        blob_sound_sfx.play()

    def normalized_vector(self, player, velocity):
        if velocity:
            velocity[0] *= self.speed
            velocity[1] *= self.speed

            return velocity

        velocity = [player.center[0]-self.position[0], player.center[1]-self.position[1]]
        magnitude = math.sqrt(velocity[0]*velocity[0]+velocity[1]*velocity[1])
        velocity[0] /= magnitude
        velocity[1] /= magnitude

        velocity[0] *= self.speed
        velocity[1] *= self.speed

        return velocity

    def render(self, surface, scroll):
        surface.blit(self.image, [self.position[0]-scroll[0], self.position[1]-scroll[1]])

    def update(self, dt, projectiles, owner, player):
        self.position[0] += round(self.velocity[0]*dt*60)
        self.position[1] += round(self.velocity[1]*dt*60)

        self.add_projectile(projectiles, owner, [player])

    def add_projectile(self, projectiles, owner, player):
        projectiles.append(Projectile(owner, player, self.position, self.image.get_size(), self.damage, 2))

    def is_offscreen(self, scroll, dimensions):
        return (
            self.position[0]-scroll[0]-self.image.get_width() < -dimensions[0] or
            self.position[1]-scroll[1]-self.image.get_height() < -dimensions[1] or
            self.position[0]-scroll[0]+self.image.get_width() > dimensions[0]*2 or
            self.position[1]-scroll[1]+self.image.get_height() > dimensions[1]*2
        )

class Octo(Boss):
    def __init__(self, camera, animations, position):
        super().__init__(animations, 'octo', position)
        self.camera = camera
        self.max_health = 600
        self.health = self.max_health
        self.speed = 3
        self.phase = 0

        self.health_bar = Health_Bar([300, 10], [800, 33], self.max_health, 'octo_health_bar')
        self.blobs = []

        self.attack_timer = self.max_attack_timer = 2
        self.move_timer = self.max_move_timer = 10
        self.moving_time = 2
        self.turn = 0

    def update_attrs(self, dt):
        if self.health <= self.max_health/4:
            self.phase = 3

        elif self.health <= self.max_health/2:
            self.phase = 2
            self.max_attack_timer = 3

        elif self.health <= self.max_health*3/4:
            self.phase = 1
            self.max_attack_timer = 3

        if self.move_timer > 0:
            self.move_timer -= dt

        if round(self.move_timer) <= 0:
            self.directions[['left', 'right'][self.turn]] = True
            self.moving_time -= dt
            self.move_timer = -self.moving_time

            if round(self.move_timer) == 0:
                self.move_timer = self.max_move_timer
                self.moving_time = 2
                self.turn += 1
                self.turn %= 2

        if self.attack_timer > 0:
            self.attack_timer -= dt

    def attack(self, player):
        if self.is_dead:
            return

        if round(self.attack_timer) == 0:
            self.attack_timer = self.max_attack_timer

            if self.phase == 0:
                self.blobs.append(Blob(player, self.center))

            if self.phase == 1:
                velocity = player.center[0]-self.center[0]
                velocity /= abs(velocity)

                for i in range(3):
                    if i != 1:
                        self.blobs.append(Blob(player, self.center, [velocity, random.uniform(min(0, i-1), max(0, i-1))]))
                        continue

                    self.blobs.append(Blob(player, self.center, [velocity, 0]))

            if self.phase > 1:
                if self.phase == 2:
                    n = 10
                else:
                    n = 15

                angle = random.randint(0, 90)
                length = 1

                for i in range(n):
                    velocity = [0,0]
                    velocity[0] = length*math.cos(math.radians(angle))
                    velocity[1] = length*math.sin(math.radians(angle))

                    self.blobs.append(Blob(player, self.center, velocity))

                    angle += 360/n

            self.camera.set_screen_shake(5, 7)

    def render(self, surface, scroll):
        super().render(surface, scroll)

        for blob in self.blobs[:]:
            blob.render(surface, scroll)

            if blob.is_offscreen(scroll, surface.get_size()):
                self.blobs.remove(blob)

    def run(self, dt, gravity, projectiles, player):
        super().run(dt, gravity)

        for blob in self.blobs:
            blob.update(dt, projectiles, self, player)

        self.update_attrs(dt)
        self.attack(player)
