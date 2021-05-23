import pygame
from scripts.functions.entity import Entity
from scripts.functions.projectile import Projectile

class Demon(Entity):
    def __init__(self, game, animations, position):
        super().__init__(animations, 'demon', position, False, 'idle')
        self.game = game
        self.directions = {k : False for k in ['up', 'right', 'down', 'left']}
        self.speed = 2
        self.health = 50
        self.attack_damage = 10
        self.movement_timer = 30
        self.invincible_timer = 0
        self.attack_timer = 30
        self.active = False

        self.damage_sfx = pygame.mixer.Sound('data/sfx/damage_enemy2.wav')

    #Updates and moves the demon towards the player
    def run(self):
        self.directions['down'] = True
        if self.movement_timer <= 0:
            self.move_towards_player()
            self.movement()

        self.update(self.game.dt)

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        if self.active:
            if self.game.entity_manager.player.position[0] < self.position[0]:
                self.flip(True)
            elif self.game.entity_manager.player.position[0] > self.position[0]:
                self.flip(False)

        if self.movement_timer > 0:
            self.movement_timer -= 1

    #Moves the demon
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

        #Gravity only (demons do not jump in this game)
        if self.directions['down']:
            self.velocity[1] += 1

        #Limiting velocity
        self.velocity[1] = min(8, self.velocity[1])

        self.directions = {k : False for k in ['up', 'right', 'down', 'left']}

        self.update_animations(animation_state)

    #Sets animation of the demon
    def update_animations(self, animation_state):
        if self.invincible_timer > 0:
            animation_state = 'damage'

        self.set_animation(animation_state)

    #Sets movement towards the player if the demon is on screen
    def move_towards_player(self):
        self.active = False
        if not self.invincible_timer > 0 and self.on_screen() and not self.game.entity_manager.player.invisible:
            self.active = True
            if self.game.entity_manager.player.position[0] < self.position[0]:
                self.directions['left'] = True
            elif self.game.entity_manager.player.position[0] > self.position[0]:
                self.directions['right'] = True

    #Returns if demon can be seen by the player
    def on_screen(self):
        return (
            abs(self.center[0]-self.game.entity_manager.player.center[0]) < 900 and
            abs(self.center[1]-self.game.entity_manager.player.center[1]) < 900 and
            self.center[0]-self.game.camera.scroll[0] > 0 and self.center[0]-self.game.camera.scroll[0] < self.game.screen.get_width() and
            self.center[1]-self.game.camera.scroll[1] > 0 and self.center[1]-self.game.camera.scroll[1] < self.game.screen.get_height()
        )

    #Reduces health
    def damage(self, damage):
        if self.invincible_timer == 0:
            self.health -= damage
            self.invincible_timer = 40
            self.damage_sfx.play()

    #Adds projectile against the player
    def attacks(self, player, projectiles):
        self.attack_timer -= 1

        if self.attack_timer == 0 and not player.invisible:
            demon_image = self.current_animation.image
            projectiles.append(Projectile(self, [player], self.position, demon_image.get_size(), self.attack_damage, 5))
            self.attack_timer = 30

    #Returns if the demon's health is 0
    def dead(self):
        return self.health <= 0
