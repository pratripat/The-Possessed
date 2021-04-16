from settings import *
from scripts.functions.entity import Entity
from scripts.functions.health_bar import Health_Bar
from scripts.functions.projectile import Projectile
from scripts.functions.skill_manager import Skill_Manager
from scripts.functions.inventory import Inventory

class Player(Entity):
    def __init__(self, animations, position):
        super().__init__(animations, 'player', position, False, 'idle')
        self.speed = 6
        self.airtimer = 0
        self.coin_counter = 0
        self.invincible_timer = 0
        self.movement_timer = 30
        self.attack_damage = 20
        self.health = self.max_health = 100

        self.attack_animation = self.animations.get_animation('stick')
        self.attack_timer = self.attack_animation.animation_data.duration()
        self.attacking = False
        self.thorns = False
        self.invincible = False
        self.invisible = False

        self.health_bar = Health_Bar([10,10], [200,40], self.max_health)
        self.skill_manager = Skill_Manager(self)
        self.inventory = Inventory(2, [10,80])
        self.inventory.add_item('stick')

    def render(self, surface, scroll, colorkey):
        super().render(surface, scroll, colorkey)

        if self.attacking:
            offset = [0,0]

            if self.flipped:
                offset[0] += self.image.get_width()

            self.attack_animation.render(screen, [self.position[0]-scroll[0]-offset[0], self.position[1]-scroll[1]-offset[1]], self.flipped, (0,0,0))

            if self.attack_animation.frame == self.attack_animation.animation_data.duration():
                self.attack_animation.frame = 0
                self.attacking = False

    def run(self, dt, particles):
        if self.movement_timer <= 0:
            self.movement(dt, particles)

        self.update(dt)
        self.skill_manager.update_skills(dt)

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        if self.attacking:
            self.attack_animation.run(dt)

        if self.movement_timer > 0:
            self.movement_timer -= 1

    def movement(self, dt, particles):
        animation_state = 'idle'

        if self.collisions['bottom']:
            self.airtimer = 0
            self.velocity[1] = 0
        elif self.airtimer == 0:
            self.airtimer = 6

        #Sets the velocity of the player horizontally
        if directions['left'] and (not self.attacking or self.airtimer > 3):
            self.velocity[0] -= 1
            self.velocity[0] = max(-self.speed, self.velocity[0])
            self.flip(True)
            animation_state = 'run'
        elif directions['right'] and (not self.attacking or self.airtimer > 3):
            self.velocity[0] += 1
            self.velocity[0] = min(self.velocity[0], self.speed)
            self.flip(False)
            animation_state = 'run'
        else:
            self.velocity[0] = 0

        #Gravity
        if directions['down']:
            self.velocity[1] += gravity
        #Jump
        elif directions['up'] and not self.attacking:
            if self.airtimer < 6:
                self.velocity[1] -= 3
                self.airtimer += 1
                particles.add_particle([self.position[0]+self.image.get_width()/2, self.position[1]+self.image.get_height()], [0,1], 3, 0.1, (41,43,48), 0, 1, 1)

            #If player is at max height, setting the upward movement false and allowing player to fall
            else:
                directions['up'] = False
                directions['down'] = True

        #Setting limit to player's velocity
        self.velocity[1] = min(8, self.velocity[1])

        self.update_animations(dt, animation_state)

    #Sets player animation
    def update_animations(self, dt, animation_state):
        if self.airtimer > 3:
            animation_state = 'jump'

        self.set_animation(animation_state)

    #Sets attacking attribute to true
    def attack(self):
        if not self.attacking:
            self.attacking = True

    #Adds projectile at position and sets the zombies as the enemies (the ones who will get hurt from the projectile)
    def attacks(self, enemies, projectiles):
        if self.thorns:
            projectiles.append(Projectile(enemies, self.position, self.image.get_size(), self.attack_damage, 2))

        if self.attack_timer > 0:
            self.attack_timer -= 1

        if self.attacking and self.attack_timer == 0:
            weapon_image = self.attack_animation.image

            if self.flipped:
                offset = self.image.get_width()
            else:
                offset = 0

            projectiles.append(Projectile(enemies, [self.position[0]-offset, self.position[1]], weapon_image.get_size(), self.attack_damage, self.attack_animation.animation_data.duration()))
            self.attack_timer = self.attack_animation.animation_data.duration()

    #Reduces player health
    def damage(self, damage):
        if self.invincible_timer == 0 and not self.invincible:
            self.health -= damage
            self.invincible_timer = 12

    #Returns if player health is 0
    def dead(self):
        return self.health <= 0
