from settings import *
from .functions.entity import Entity
from .functions.projectile import Projectile

class Hound(Entity):
    def __init__(self, animations, position):
        super().__init__(animations, 'hound', position, False, 'idle')
        self.directions = {k : False for k in ['up', 'right', 'down', 'left']}
        self.speed = 6
        self.health = 100
        self.attack_damage = 10
        self.movement_timer = 30
        self.invincible_timer = 0
        self.attack_timer = 30
        self.active = False

    #Updates and moves the hound towards the player
    def run(self, scroll, dt, player):
        self.directions['down'] = True
        if self.movement_timer <= 0:
            self.move_towards_player(scroll, player)
            self.movement()

        self.update(dt)

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        if self.active:
            if player.center[0] < self.center[0]:
                self.flip(False)
            elif player.center[0] > self.center[0]:
                self.flip(True)

        if self.movement_timer > 0:
            self.movement_timer -= 1

    #Moves the hound
    def movement(self):
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

        #Gravity only (hounds do not jump in this game)
        if self.directions['down']:
            self.velocity[1] += gravity

        #Limiting velocity
        self.velocity[1] = min(8, self.velocity[1])

        self.directions = {k : False for k in ['up', 'right', 'down', 'left']}

        self.update_animations(animation_state)

    #Sets animation of the hound
    def update_animations(self, animation_state):
        if self.invincible_timer > 0:
            animation_state = 'damage'

        self.set_animation(animation_state)

    #Sets movement towards the player if the hound is on screen
    def move_towards_player(self, scroll, player):
        self.active = False
        if not self.invincible_timer > 0 and self.on_screen(scroll, player) and not player.invisible:
            self.active = True
            if player.center[0] < self.center[0]:
                self.directions['left'] = True
            elif player.center[0] > self.center[0]:
                self.directions['right'] = True

    #Returns if hound can be seen by the player
    def on_screen(self, scroll, player):
        return (
            abs(self.center[0]-player.center[0]) < 900 and
            abs(self.center[1]-player.center[1]) < 900 and
            self.center[0]-scroll[0] > 0 and self.center[0]-scroll[0] < screen.get_width() and
            self.center[1]-scroll[1] > 0 and self.center[1]-scroll[1] < screen.get_height()
        )

    #Reduces health
    def damage(self, damage):
        if self.invincible_timer == 0:
            self.health -= damage
            self.invincible_timer = 40

    #Adds projectile against the player
    def attacks(self, player, projectiles):
        self.attack_timer -= 1

        if self.attack_timer == 0 and not player.invisible:
            hound_image = self.current_animation.image
            projectiles.append(Projectile(self, [player], self.position, hound_image.get_size(), self.attack_damage, 5))
            self.attack_timer = 30

    #Returns if the hound's health is 0
    def dead(self):
        return self.health <= 0
