import math
from settings import *
from scripts.functions.camera import Camera
from scripts.functions.renderer import Renderer
from scripts.functions.tilemap import TileMap
from scripts.functions.animation_handler import Animation_Handler
from scripts.functions.entity_manager import Entity_Manager
from scripts.functions.particle import Particle_System
from scripts.functions.font_renderer import Font
from scripts.functions.select_skill_menu import Select_skill_menu

class World:
    def __init__(self):
        self.animation_handler = Animation_Handler()
        self.particles = Particle_System()
        self.renderer = Renderer()
        self.camera = Camera()
        self.camera.set_movement(0.05)
        self.font = Font('data/graphics/spritesheet/character_spritesheet')

        self.projectiles = []
        self.level_order = json.load(open('data/configs/level_order.json', 'r'))
        self.level = 0
        self.load_level(self.level)

        self.skill_menu = Select_skill_menu(self.font, self.entity_manager.player.skill_manager)

    @property
    def dt(self):
        fps = clock.get_fps()

        if fps != 0:
            return 1/fps

        return 0.001

    def load_level(self, level):
        if self.level_order[self.level].split('_')[0] == 'boss':
            pygame.mixer.music.load('data/music/boss_fight.wav')
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.load('data/music/game_music.wav')
            pygame.mixer.music.play(-1)

        if self.level >= 1:
            player_data = self.entity_manager.player.get_data()
        else:
            player_data = None

        self.tilemap = TileMap(f'data/levels/{self.level_order[self.level]}.json')
        self.tilemap.load_map()
        self.entity_manager = Entity_Manager(self, player_data=player_data)
        self.camera.set_target(self.entity_manager.player)

        self.particles.clear()
        self.projectiles.clear()

        self.collidables = self.tilemap.get_tiles('ground')
        self.game_time = 0

    def run(self):
        clock.tick(60)

        self.game_time += self.dt

        self.camera.update(screen)

        self.entity_manager.run(screen, self.camera.scroll, self.collidables, self.projectiles, self.particles, self.dt, gravity)
        self.particles.run()

        for projectile in self.projectiles[:]:
            projectile.update(self.camera)

            if projectile.destroyed:
                self.projectiles.remove(projectile)

        self.renderer.render(screen, self.font, self.tilemap, self.particles, self.entity_manager, self.camera.scroll, self.game_time)

        pygame.display.update()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.entity_manager.player.attack(self.projectiles)
                if event.button == 3:
                    self.entity_manager.player.skill_manager.use_selected_skill()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_1:
                    self.entity_manager.player.skill_manager.set_selected_skill(0)
                if event.key == pygame.K_2:
                    self.entity_manager.player.skill_manager.set_selected_skill(1)
                if event.key == pygame.K_3:
                    self.entity_manager.player.skill_manager.set_selected_skill(2)
                if event.key == pygame.K_4:
                    self.entity_manager.player.skill_manager.set_selected_skill(3)
                if event.key == pygame.K_5:
                    self.entity_manager.player.skill_manager.set_selected_skill(4)
                if event.key == pygame.K_6:
                    self.entity_manager.player.skill_manager.set_selected_skill(5)

                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.entity_manager.player.inventory.select_next_item()

                if event.key == pygame.K_e:
                    self.entity_manager.equip_dropped_entity()

                if event.key == pygame.K_q:
                    self.entity_manager.drop_player_item()

                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    directions['left'] = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    directions['right'] = True
                if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    directions['up'] = True
                    directions['down'] = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    directions['left'] = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    directions['right'] = False
                if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    directions['up'] = False
                    directions['down'] = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    #Starts the game
    def main_loop(self):
        while True:
            self.event_loop()
            self.run()
