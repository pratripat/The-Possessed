from settings import *
from scripts.functions.entity import Entity
from scripts.functions.health_bar import Health_Bar
from scripts.functions.projectile import Projectile
from scripts.functions.skill_manager import Skill_Manager
from scripts.functions.inventory import Inventory
from scripts.functions.weapon import Weapon

class Player(Entity):
    INVENTORY_LENGTH = 2
    SKILLS_LENGTH = 3

    DATA = {
        'health': 100,
        'inventory_items': [None for _ in range(INVENTORY_LENGTH)],
        'inventory_ids': ['' for _ in range(INVENTORY_LENGTH)],
        'inventory_current_item_index': 0,
        'skills': [None for _ in range(SKILLS_LENGTH)],
        'current_skills': [],
        'selected_skill': None
    }

    def __init__(self, animations, position, data=None):
        if data != None:
            self.DATA = data

        super().__init__(animations, 'player', position, False, 'idle')
        self.speed = 6
        self.airtimer = 0
        self.coin_counter = 0
        self.invincible_timer = 0
        self.movement_timer = 30
        self.attack_damage = 20
        self.health = self.DATA['health']
        self.max_health = 100
        self.attack_damage = 10

        self.attacking = False
        self.thorns = False
        self.invincible = False
        self.invisible = False

        self.health_bar = Health_Bar([10,10], [200,40], self.max_health)
        self.skill_manager = Skill_Manager(self, self.DATA)
        self.inventory = Inventory(self, [10, 80], self.DATA)

        self.damage_sfx = pygame.mixer.Sound('data/sfx/damage_player.wav')

        if self.load_weapon():
            self.attack_timer = self.weapon.duration
        else:
            self.attack_timer = 0

    def render(self, surface, scroll, colorkey):
        super().render(surface, scroll, colorkey)

        if self.attacking:
            self.weapon.render(surface, scroll)

    def run(self, dt, particles):
        if self.movement_timer <= 0:
            self.movement(dt, particles)

        self.update(dt)
        self.skill_manager.update_skills(dt)

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        if self.attacking:
            self.weapon.run(dt)

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
        if directions['left'] and not directions['right'] and (not self.attacking or self.airtimer > 3):
            self.velocity[0] -= 1
            self.velocity[0] = max(-self.speed, self.velocity[0])
            self.flip(True)
            animation_state = 'run'
        if directions['right'] and not directions['left'] and (not self.attacking or self.airtimer > 3):
            self.velocity[0] += 1
            self.velocity[0] = min(self.velocity[0], self.speed)
            self.flip(False)
            animation_state = 'run'
        if not directions['left'] and not directions['right']:
            self.velocity[0] -= self.velocity[0] * 6 * dt

        #Gravity
        if directions['down']:
            self.velocity[1] += gravity
        #Jump
        elif directions['up'] and not self.attacking:
            if self.airtimer < 6:
                self.velocity[1] -= 2
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
    def attack(self, projectiles):
        if not self.attacking:
            projectiles.append(Projectile(self, [], self.position, self.image.get_size(), 0, 2))
            self.attacking = True

            if not self.load_weapon():
                self.attacking = False

    #Adds projectile at position and sets the zombies as the enemies (the ones who will get hurt from the projectile)
    def attacks(self, enemies, projectiles):
        if self.thorns:
            projectiles.append(Projectile(self, enemies, self.position, self.image.get_size(), self.attack_damage, 2))

        if self.attack_timer > 0:
            self.attack_timer -= 1

        if self.attacking and self.attack_timer == 0:
            self.weapon.attack(enemies, projectiles)
            self.attack_timer = self.weapon.duration*2

    #Reduces player health
    def damage(self, damage):
        if self.invincible_timer == 0 and not self.invincible:
            self.health -= damage
            self.invincible_timer = 12
            self.damage_sfx.play()

    #Returns if player health is 0
    def dead(self):
        return self.health <= 0

    def load_weapon(self):
        weapon_id = self.inventory.get_current_item_id()

        if weapon_id != '':
            self.weapon = Weapon(weapon_id, self.animations, self)
            return True

        self.weapon = None
        return False

    def get_data(self):
        return {
            'health': self.health,
            'inventory_items': self.inventory.items,
            'inventory_ids': self.inventory.ids,
            'inventory_current_item_index': self.inventory.current_item_index,
            'skills': self.skill_manager.skills,
            'current_skills': self.skill_manager.current_skills,
            'selected_skill': self.skill_manager.selected_skill
        }
