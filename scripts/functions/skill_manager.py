from .skill import Skill
import pygame, json

def secs_to_mins(seconds):
    if seconds >= 60:
        return f'{seconds//60:02d}:{seconds-60:02d}'

    return f'00:{seconds:02d}'

class Skill_Manager:
    def __init__(self, owner, data):
        self.owner = owner
        self.icon_background_image = pygame.image.load('data/graphics/images/icon_background.png').convert()
        self.icon_background_image.set_colorkey((0,0,0))
        self.skill_durations = json.load(open('data/configs/skills/skill_duration.json', 'r'))
        self.skills = data['skills']
        self.selected_skill = data['selected_skill']
        self.current_skills = data['current_skills']

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
                if self.owner.weapon:
                    if skill.using_timer > 0:
                        self.owner.weapon.extra_damage()
                    else:
                        self.owner.weapon.reset_damage()

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
                    font.render(surface, f'Using skill currently ({secs_to_mins(round(self.selected_skill.using_timer))})', [surface.get_width()/2+4, surface.get_height()-104], center=[True, True], scale=1.5, color=(41,43,48))
                    font.render(surface, f'Using skill currently ({secs_to_mins(round(self.selected_skill.using_timer))})', [surface.get_width()/2+2, surface.get_height()-102], center=[True, True], scale=1.5, color=(97,56,84))
                    font.render(surface, f'Using skill currently ({secs_to_mins(round(self.selected_skill.using_timer))})', [surface.get_width()/2, surface.get_height()-100], center=[True, True], scale=1.5, color=(171,108,132))
                else:
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

    def add_skill(self, skill_id):
        for i, skill in enumerate(self.skills):
            if skill == None:
                skill_time_duration = self.skill_durations[skill_id]
                self.skills[i] = Skill(skill_id, *skill_time_duration)
                return
