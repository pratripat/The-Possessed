from .skill import Skill
import pygame

def secs_to_mins(seconds):
    if seconds >= 60:
        return f'{seconds//60:02d}:{seconds-60:02d}'

    return f'00:{seconds:02d}'

class Skill_Manager:
    def __init__(self, owner):
        self.owner = owner
        self.icon_background_image = pygame.image.load('data/graphics/images/icon_background.png')
        self.skills = [None for _ in range(6)]
        self.skills[0] = Skill('instant_health', 30, 1)
        self.skills[1] = Skill('extra_speed', 50, 30)
        self.skills[2] = Skill('extra_damage', 50, 20)
        self.skills[3] = Skill('thorns', 50, 20)
        self.skills[4] = Skill('invisibility', 20, 20)
        self.skills[5] = Skill('invincibility', 20, 20)
        self.selected_skill = None
        self.current_skills = []

    def update_skills(self, dt):
        for skill in self.skills:
            if skill:
                skill.update(dt)

        for skill in self.current_skills[:]:
            if skill.type == 'instant_health' and skill.using_timer > 0:
                self.owner.health = self.owner.max_health
            if skill.type == 'extra_speed':
                if skill.using_timer > 0:
                    self.owner.speed = 9
                else:
                    self.owner.speed = 6
            if skill.type == 'extra_damage':
                if skill.using_timer > 0:
                    self.owner.attack_damage = 30
                else:
                    self.owner.attack_damage = 20
            if skill.type == 'thorns':
                if skill.using_timer > 0:
                    self.owner.thorns = True
                else:
                    self.owner.thorns = False
            if skill.type == 'invisibility':
                if skill.using_timer > 0:
                    self.owner.invisible = True
                    self.owner.id = 'invisible_player'
                else:
                    self.owner.invisible = False
                    self.owner.id = 'player'
            if skill.type == 'invincibility':
                if skill.using_timer > 0:
                    self.owner.invincible = True
                else:
                    self.owner.invincible = False

            if skill.waiting_timer == 0:
                self.current_skills.remove(skill)

    def render_skills(self, surface, font):
        position = [surface.get_width()/2-(len(self.skills)*50)/2, surface.get_height()-50]
        for skill in self.skills:
            if skill in self.current_skills and self.selected_skill.waiting_timer > 0:
                if self.selected_skill.using_timer > 0:
                    font.render(surface, f'Using skill currently', [surface.get_width()/2+4, surface.get_height()-154], center=[True, True], scale=1.5, color=(41,43,48))
                    font.render(surface, f'Using skill currently', [surface.get_width()/2+2, surface.get_height()-152], center=[True, True], scale=1.5, color=(97,56,84))
                    font.render(surface, f'Using skill currently', [surface.get_width()/2, surface.get_height()-150], center=[True, True], scale=1.5, color=(171,108,132))

                font.render(surface, f'Skill active again in {secs_to_mins(round(self.selected_skill.waiting_timer))}', [surface.get_width()/2+4, surface.get_height()-104], center=[True, True], scale=1.5, color=(41,43,48))
                font.render(surface, f'Skill active again in {secs_to_mins(round(self.selected_skill.waiting_timer))}', [surface.get_width()/2+2, surface.get_height()-102], center=[True, True], scale=1.5, color=(97,56,84))
                font.render(surface, f'Skill active again in {secs_to_mins(round(self.selected_skill.waiting_timer))}', [surface.get_width()/2, surface.get_height()-100], center=[True, True], scale=1.5, color=(171,108,132))
            elif skill == self.selected_skill and self.selected_skill:
                    font.render(surface, 'Right click to use', [surface.get_width()/2+4, surface.get_height()-104], center=[True, True], scale=1.5, color=(41,43,48))
                    font.render(surface, 'Right click to use', [surface.get_width()/2+2, surface.get_height()-102], center=[True, True], scale=1.5, color=(97,56,84))
                    font.render(surface, 'Right click to use', [surface.get_width()/2, surface.get_height()-100], center=[True, True], scale=1.5, color=(171,108,132))

            if skill == self.selected_skill and skill:
                surf = pygame.Surface((48,48))
                surf.fill((255,232,225))
                surface.blit(surf, position, special_flags=pygame.BLEND_RGBA_ADD)
            else:
                surface.blit(self.icon_background_image, position, special_flags=pygame.BLEND_RGBA_ADD)

            if skill:
                skill.render_icon(surface, position)

            position[0] += 50

    def set_selected_skill(self, i):
        if self.skills[i]:
            self.selected_skill = self.skills[i]

    def use_selected_skill(self):
        if self.selected_skill and self.selected_skill not in self.current_skills:
            self.current_skills.append(self.selected_skill)
            self.selected_skill.use()
