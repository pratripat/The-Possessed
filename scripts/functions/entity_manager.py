import pygame, copy
from .funcs import *
from scripts.player import Player
from scripts.demon import Demon
from scripts.hound import Hound
from scripts.loot_box import LootBox
from scripts.door import Door
from scripts.octo import Octo
from scripts.eye import Eye

class Entity_Manager:
    def __init__(self, world, player_data=None, final_level=False):
        self.world = world
        self.level_transition = pygame.mixer.Sound('data/sfx/level_transition.wav')
        self.player = Player(self.world.animation_handler, self.get_entity(self.world.tilemap, 'player')[0], player_data)
        self.enemies = [Demon(self.world.animation_handler, position) for position in self.get_entity(self.world.tilemap, 'demon')] + [Hound(self.world.animation_handler, position) for position in self.get_entity(self.world.tilemap, 'hound')]
        self.loot_boxes = [LootBox(self.world.animation_handler, position) for position in self.get_entity(self.world.tilemap, 'lootbox')]
        self.dropped_entities = []
        self.boss = None
        self.end_level_delay = 2

        try:
            self.door = Door(self.get_entity(self.world.tilemap, 'door')[0], self.world.tilemap)
        except:
            if not final_level:
                boss_ids = ['octo', 'eye']
                bosses = [Octo(self.world.camera, self.world.animation_handler, [0,0]), Eye(self.world.animation_handler, [0,0])]
                for i, id in enumerate(boss_ids):
                    try:
                        position = self.get_entity(self.world.tilemap, id)[0]
                        self.boss = bosses[i]
                        self.boss.position = position
                    except:
                        continue

            self.door = None

    def run(self, surface, scroll, collidables, projectiles, particles, dt, gravity):
        enemies = self.enemies.copy()

        if self.boss:
            enemies.append(self.boss)

        for loot_box in self.loot_boxes:
            loot_box.run(dt)

        for enemy in self.enemies[:]:
            enemy.move(collidables, dt)
            enemy.run(scroll, dt, self.player)
            enemy.attacks(self.player, projectiles)

            if enemy.dead():
                self.enemies.remove(enemy)
                particles.add_particle(enemy.center, [0,0], size=10, decrementation=0.2, color=(41,43,48), intensity=5, number=20, collidables=collidables)

        self.player.move(collidables, dt)
        self.player.run(dt, particles)
        self.player.attacks(enemies, projectiles)

        if self.boss:
            self.boss.run(dt, gravity, projectiles, self.player)
            self.boss.move(collidables, dt)

            if self.boss.dead():
                if self.end_level_delay > 0:
                    self.end_level_delay -= dt
                    return

                self.world.skill_menu.run(surface)
                self.finish_level()

        if self.door:
            if rect_rect_collision(self.player.rect, self.door.rect):
                self.level_transition.play()
                self.finish_level()

        for projectile in projectiles:
            for lootbox in self.loot_boxes:
                if projectile.owner == self.player and not lootbox.opened:
                    if rect_rect_collision(projectile.rect, lootbox.rect):
                        lootbox.open(self.dropped_entities)

        for entity in self.dropped_entities:
            entity.update(dt, gravity, collidables)

    def render(self, surface, scroll):
        for loot_box in self.loot_boxes:
            loot_box.render(surface, scroll)

        for enemy in self.enemies:
            enemy.render(surface, scroll, (0,0,0))

        if self.door:
            self.door.render(surface, scroll)

        self.player.render(surface, scroll, (0,0,0))

        if self.boss:
            self.boss.render(surface, scroll)

        for entity in self.dropped_entities:
            entity.render(surface, scroll)

    def render_ui(self, surface, font):
        if self.boss:
            self.boss.health_bar.position[0] = surface.get_width()/2-self.boss.health_bar.dimensions[0]/2
            self.boss.health_bar.render(surface, self.boss.health, (171,108,132))

        self.player.health_bar.position[1] = surface.get_height()-self.player.health_bar.dimensions[1]-10
        self.player.health_bar.render(surface, self.player.health, (171,108,132), [20,0])
        self.player.skill_manager.render_skills(surface, font)

        self.player.inventory.position[0] = self.player.health_bar.position[0]+self.player.health_bar.dimensions[0]+10
        self.player.inventory.position[1] = surface.get_height()-self.player.inventory.size-10
        self.player.inventory.render(surface)

    def get_entity(self, tilemap, id):
        tiles = tilemap.get_tiles(id)
        positions = [[tile.x, tile.y] for tile in tiles]

        return positions

    def equip_dropped_entity(self):
        for entity in self.dropped_entities[:]:
            if rect_rect_collision(entity.rect, self.player.rect):
                self.player.inventory.pick_item(entity.id, self.dropped_entities)
                self.dropped_entities.remove(entity)
                break

    def drop_player_item(self):
        self.player.inventory.drop_item(self.dropped_entities)
        self.player.load_weapon()

    def finish_level(self):
        self.world.level += 1
        self.world.load_level(self.world.level)
