import pygame
from .functions.entity import Entity
from .functions.projectile import Projectile

class Boss(Entity):
    def __init__(self, animations, id, position):
        super().__init__(animations, id, position, False, 'idle')
        self.directions = {k : False for k in ['up', 'right', 'down', 'left']}
        self.speed = 1
        self.health = 100
        self.invincible_timer = 0
        self.is_dead = False

        self.damage_sfx = pygame.mixer.Sound('data/sfx/damage_enemy2.wav')
        self.dead_sfx = pygame.mixer.Sound('data/sfx/boss_dead.wav')

    def run(self, dt, gravity):
        self.update(dt)
        if not self.is_dead:
            self.movement(gravity)

            if self.invincible_timer > 0:
                self.invincible_timer -= 1

    def movement(self, gravity):
        if self.is_dead:
            return

        self.directions['down'] = True

        animation_state = 'idle'

        #Horizontal movement
        if self.directions['left']:
            self.velocity[0] -= 1
            self.velocity[0] = max(-self.speed, self.velocity[0])
            self.flip(True)
            animation_state = 'run'
        elif self.directions['right']:
            self.velocity[0] += 1
            self.velocity[0] = min(self.velocity[0], self.speed)
            self.flip(False)
            animation_state = 'run'
        else:
            self.velocity[0] = 0

        if self.directions['down']:
            self.velocity[1] += gravity

        #Limiting velocity
        self.velocity[1] = min(8, self.velocity[1])

        self.directions = {k : False for k in ['up', 'right', 'down', 'left']}

        self.update_animations(animation_state)

    #Sets animation of the boss
    def update_animations(self, animation_state):
        self.set_animation(animation_state)

    def damage(self, damage):
        if self.invincible_timer == 0:
            self.health -= damage
            self.invincible_timer = 12

            self.damage_sfx.play()

    def dead(self):
        if self.health <= 0:
            if not self.is_dead:
                self.set_animation('die')
                self.dead_sfx.play()
                self.is_dead = True
            return True

        return False
