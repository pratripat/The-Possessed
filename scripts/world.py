import math
from settings import *
from scripts.functions.camera import Camera
from scripts.functions.renderer import Renderer
from scripts.functions.tilemap import TileMap
from scripts.functions.animation_handler import Animation_Handler
from scripts.functions.entity_manager import Entity_Manager
from scripts.functions.particle import Particle_System
from scripts.functions.font_renderer import Font

class World:
    def __init__(self):
        self.animation_handler = Animation_Handler()
        self.particles = Particle_System()
        self.tilemap = TileMap(f'data/saved.json')
        self.tilemap.load_map()
        self.renderer = Renderer()
        self.entity_manager = Entity_Manager(self.animation_handler, self.tilemap)
        self.camera = Camera()
        self.camera.set_target(self.entity_manager.player)
        self.camera.set_movement(0.05)
        self.font = Font('data/graphics/spritesheet/character_spritesheet')
        self.projectiles = []
        self.game_time = 0

        self.collidables = self.tilemap.get_tiles('ground', 0)

    @property
    def dt(self):
        fps = clock.get_fps()

        if fps != 0:
            return 1/fps

        return 0

    def run(self):
        clock.tick(100)

        self.game_time += self.dt

        self.camera.update(screen)

        self.entity_manager.run(self.camera.scroll, self.collidables, self.projectiles, self.particles, self.dt)
        self.particles.run()

        for projectile in self.projectiles[:]:
            projectile.update(self.camera, self.particles)

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
                    self.entity_manager.player.attack()
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
        pygame.mixer.music.load('data/music/game_music.wav')
        pygame.mixer.music.play(-1)
        while True:
            self.event_loop()
            self.run()
