import pygame, math, random
from scripts.functions.particle import Particle_System

def get_circle_surface(radius, color):
    surface = pygame.Surface((radius*2, radius*2))
    surface.set_colorkey((0,0,0))
    pygame.draw.circle(surface, color, (radius, radius), radius)
    return surface

class Renderer:
    def __init__(self, game):
        self.game = game

    def render(self):
        rendered = False
        visible_tiles = ['ground', 'pillar', 'rock', 'torch', 'door']
        self.game.screen.fill((0,0,0))

        for tile in self.game.tilemap.entities:
            if tile['layer'] == 0 and not rendered:
                self.game.entity_manager.render()
                rendered = True

            if tile['id'] in visible_tiles:
                position = [tile['position'][0]+tile['offset'][0]-self.game.camera.scroll[0], tile['position'][1]+tile['offset'][1]-self.game.camera.scroll[1]]
                self.game.screen.blit(tile['image'], position)

                if tile['id'] == 'torch':
                    light_sin = math.sin(self.game.game_time)*10
                    light_radius = round(150+light_sin)
                    circle_surf = get_circle_surface(light_radius, (41,43,48))
                    self.game.screen.blit(circle_surf, (tile['position'][0]-self.game.camera.scroll[0]-light_radius+24, tile['position'][1]-self.game.camera.scroll[1]-light_radius+20), special_flags=pygame.BLEND_RGBA_ADD)

                    light_sin = math.sin(self.game.game_time+1)*10
                    light_radius = round(50+light_sin)
                    circle_surf = pygame.transform.scale(circle_surf, (light_radius*2, light_radius*2))
                    self.game.screen.blit(circle_surf, (tile['position'][0]-self.game.camera.scroll[0]-light_radius+24, tile['position'][1]-self.game.camera.scroll[1]-light_radius+20), special_flags=pygame.BLEND_RGBA_ADD)

                    if random.randrange(1,60) == 1:
                        self.game.particles.add_particle([tile['position'][0]+24, tile['position'][1]+20], [0,-1], 10, 0.1, (41,43,48), pygame.BLEND_RGBA_ADD, 0.5, 1)

        self.game.particles.render(self.game.screen, self.game.camera.scroll)

        purple_surf = pygame.Surface(self.game.screen.get_size())
        purple_surf.fill((77,16,89))

        sin = math.sin(self.game.game_time)*50
        horizontal_radius = round(self.game.screen.get_width()+sin)
        vertical_radius = round(self.game.screen.get_height()+sin)

        pygame.draw.ellipse(purple_surf, (31,10,31), (self.game.screen.get_width()//2-(horizontal_radius+200)//2, self.game.screen.get_height()//2-(vertical_radius+200)//2, (horizontal_radius+200), (vertical_radius+200)))
        pygame.draw.ellipse(purple_surf, (0,0,0), (self.game.screen.get_width()//2-horizontal_radius//2, self.game.screen.get_height()//2-vertical_radius//2, horizontal_radius, vertical_radius))

        self.game.screen.blit(purple_surf, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

        self.game.entity_manager.render_ui()
