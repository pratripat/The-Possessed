import pygame
from scripts.player import Player
from scripts.demon import Demon
from scripts.hound import Hound
from scripts.soul import Soul

class Entity_Manager:
    def __init__(self, animations, tilemap):
        self.player = Player(animations, self.get_player_position(tilemap))
        self.demons = [Demon(animations, position) for position in self.get_enemy_positions(tilemap, 'demon')]
        self.hounds = [Hound(animations, position) for position in self.get_enemy_positions(tilemap, 'hound')]
        self.souls = [Soul(animations, position) for position in self.get_enemy_positions(tilemap, 'soul')]
        self.enemies = self.demons + self.hounds + self.souls

    def run(self, scroll, collidables, projectiles, particles, dt):
        for enemy in self.enemies[:]:
            enemy.move(collidables, dt)
            enemy.run(scroll, dt, self.player)
            enemy.attacks(self.player, projectiles)

            if enemy.dead():
                self.enemies.remove(enemy)
                particles.add_particle(enemy.center, [0,0], size=10, decrementation=0.2, color=(41,43,48), intensity=5, number=20, collidables=collidables)

        self.player.move(collidables, dt)
        self.player.run(dt, particles)
        self.player.attacks(self.enemies, projectiles)

    def render(self, surface, scroll):
        for enemy in self.enemies:
            enemy.render(surface, scroll, (0,0,0))

        self.player.render(surface, scroll, (0,0,0))

    def render_ui(self, surface, font):
        self.player.health_bar.render(surface, self.player.health, (171,108,132))
        self.player.skill_manager.render_skills(surface, font)
        self.player.inventory.render(surface)

    def get_player_position(self, tilemap):
        player_tile = tilemap.get_tiles('player')[0]
        return [player_tile.x, player_tile.y]

    def get_enemy_positions(self, tilemap, id):
        enemy_tiles = tilemap.get_tiles(id)
        enemy_positions = [[tile.x, tile.y] for tile in enemy_tiles]

        return enemy_positions
