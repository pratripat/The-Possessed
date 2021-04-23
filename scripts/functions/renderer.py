import pygame, math, random
from scripts.functions.particle import Particle_System

def get_circle_surface(radius, color):
    surface = pygame.Surface((radius*2, radius*2))
    surface.set_colorkey((0,0,0))
    pygame.draw.circle(surface, color, (radius, radius), radius)
    return surface

class Renderer:
    def render(self, screen, font, tilemap, particles, entities, scroll, game_time):
        rendered = False
        visible_tiles = ['ground', 'decoration', 'pillar', 'rock', 'torch']
        screen.fill((0,0,0))

        for tile in tilemap.tiles:
            if tile['layer'] == 0 and not rendered:
                entities.render(screen, scroll)
                rendered = True

            if tile['id'] in visible_tiles:
                position = [tile['position'][0]+tile['offset'][0]-scroll[0], tile['position'][1]+tile['offset'][1]-scroll[1]]
                screen.blit(tile['image'], position)

                if tile['id'] == 'torch':
                    light_sin = math.sin(game_time)*10
                    light_radius = round(150+light_sin)
                    circle_surf = get_circle_surface(light_radius, (41,43,48))
                    screen.blit(circle_surf, (tile['position'][0]-scroll[0]-light_radius+24, tile['position'][1]-scroll[1]-light_radius+20), special_flags=pygame.BLEND_RGBA_ADD)

                    light_sin = math.sin(game_time+1)*10
                    light_radius = round(50+light_sin)
                    circle_surf = pygame.transform.scale(circle_surf, (light_radius*2, light_radius*2))
                    screen.blit(circle_surf, (tile['position'][0]-scroll[0]-light_radius+24, tile['position'][1]-scroll[1]-light_radius+20), special_flags=pygame.BLEND_RGBA_ADD)

                    if random.randrange(1,60) == 1:
                        particles.add_particle([tile['position'][0]+24, tile['position'][1]+20], [0,-1], 10, 0.1, (41,43,48), pygame.BLEND_RGBA_ADD, 0.5, 1)

        particles.render(screen, scroll)
        entities.render_ui(screen, font)
