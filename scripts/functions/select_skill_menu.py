import pygame, json, sys
from .button import Button

class Select_skill_menu:
    def __init__(self, font, player_skill_manager):
        self.n = 0
        self.font = font
        self.player_skill_manager = player_skill_manager
        self.all_skills = json.load(open('data/configs/skills/all_skills.json', 'r'))
        self.skills = self.all_skills[self.n:self.n+2]
        self.skill_descriptions = json.load(open('data/configs/skills/description.json', 'r'))
        self.current_selected_button = None

        self.load_buttons(font)

    def add_current_skill_to_player(self):
        if not self.current_selected_button:
            return

        self.player_skill_manager.add_skill(self.current_selected_button.text.lower())
        self.n += 2
        self.skills = self.all_skills[self.n:self.n+2]
        self.current_selected_button = None
        self.running = False

        self.load_buttons(self.font)

    def select_button(self, button):
        self.current_selected_button = button

    def load_buttons(self, font):
        positions = [70, 410]

        self.buttons = []
        self.button_positions = []

        self.buttons.append(Button({'x':240, 'y':480, 'w':120, 'h':60},
        {'color':(171,108,132), 'hover_color':(97,56,84), 'font_color':(41,43,48), 'alpha':255},
        {'text':'choose skill', 'font_renderer':font}, center=False, type='choose_skill'))
        self.button_positions.append([240, 480])

        for i, skill in enumerate(self.skills):
            button = Button({'x':positions[i], 'y':220, 'w':120, 'h':60},
            {'color':(171,108,132), 'hover_color':(97,56,84), 'font_color':(41,43,48), 'alpha':255},
            {'text':skill.capitalize(), 'font_renderer':font}, center=False, type='skill')

            self.buttons.append(button)
            self.button_positions.append([positions[i], 220])

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.type == 'skill':
                        button.on_click(self.select_button, [button])
                    elif button.type == 'choose_skill':
                        button.on_click(self.add_current_skill_to_player)

    def render(self, surface):
        if not self.running:
            return

        center = [surface.get_width()/2, surface.get_height()/2]

        surface.blit(self.background, (0,0))
        surface.fill((100,100,100), special_flags=pygame.BLEND_RGBA_MULT)

        pygame.draw.rect(surface, (41,43,48), (center[0]-300, center[1]-300, 600, 600), border_radius=30)

        self.font.render(surface, 'you have reached', [center[0]+20, center[1]-200], color=(97,56,84), scale=2, center=[True, True])
        self.font.render(surface, 'you have reached', [center[0]+16, center[1]-204], color=(171,108,132), scale=2, center=[True, True])

        self.font.render(surface, 'one step closer to me.', [center[0]+20, center[1]-150], color=(97,56,84), scale=2, center=[True, True])
        self.font.render(surface, 'one step closer to me.', [center[0]+16, center[1]-154], color=(171,108,132), scale=2, center=[True, True])

        if self.current_selected_button:
            x, y = self.current_selected_button.x-10, self.current_selected_button.y-10
            w, h = self.current_selected_button.w+20, self.current_selected_button.h+20

            pygame.draw.rect(surface, (97,56,84), (x, y, w, h), border_radius=20)

            self.font.render(surface, 'description:', [center[0]-230, y+140], color=(97,56,84))
            self.font.render(surface, 'description:', [center[0]-234, y+136], color=(171,108,132))

            description = self.skill_descriptions[self.current_selected_button.text.lower()]
            self.font.render(surface, description, [center[0]-230, y+190], color=(97,56,84))
            self.font.render(surface, description, [center[0]-234, y+186], color=(171,108,132))

        for i, button in enumerate(self.buttons):
            position = self.button_positions[i]
            button.x = position[0] + center[0]-300
            button.y = position[1] + center[1]-300

            button.show(surface, border_radius=20, scale=0.75)

        pygame.display.update()

    def update(self):
        for button in self.buttons:
            button.update()

    def run(self, surface):
        self.background = surface.copy()
        self.running = True

        pygame.mixer.music.load('data/music/skill_selector.wav')
        pygame.mixer.music.play(-1)

        while self.running:
            self.event_loop()
            self.update()
            self.render(surface)
