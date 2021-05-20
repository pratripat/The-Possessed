from .projectile import Projectile
import json

class Weapon:
    def __init__(self, id, animations, owner):
        self.id = id
        self.owner = owner
        self.animation = animations.get_animation(self.id)
        self.initial_damage = self.damage = json.load(open('data/configs/weapons/weapons.json', 'r'))[self.id]

    def render(self, surface, scroll, colorkey=(0,0,0)):
        if self.owner.attacking:
            offset = [0,0]

            if self.owner.flipped:
                offset[0] += self.owner.image.get_width()/2

            self.animation.render(surface, [self.owner.position[0]-scroll[0]-offset[0], self.owner.position[1]-scroll[1]-offset[1]], self.owner.flipped, colorkey)

            if self.animation.frame == self.animation.animation_data.duration():
                self.animation.frame = 0
                self.owner.attacking = False

    def run(self, dt):
        self.animation.run(dt)

    def attack(self, enemies, projectiles):
        if self.owner.flipped:
            offset = self.owner.image.get_width()
        else:
            offset = 0

        projectiles.append(Projectile(self.owner, enemies, [self.owner.position[0]-offset, self.owner.position[1]], self.animation.image.get_size(), self.damage, self.duration))

    def extra_damage(self):
        self.damage = self.initial_damage * 2

    def reset_damage(self):
        self.damage = self.initial_damage

    @property
    def duration(self):
        return self.animation.animation_data.duration()
