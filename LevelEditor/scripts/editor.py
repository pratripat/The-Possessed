from LevelEditor.settings import *
from .world.world import World
from .selector_panel.selector_panel import Selector_Panel
from .event_handler import Event_Handler
import sys

class Editor:
    def __init__(self):
        self.event_handler = Event_Handler()
        self.world = World()
        self.selector_panel = Selector_Panel(200,height)

    def get_fps(self):
        fps = clock.get_fps()

        if fps:
            return fps

        return 1/0.0001

    def load(self, filename):
        self.world.load(filename)

    def run(self):
        clock.tick()

        #Runs the functions of the world and selector according to the events like mouse clicked
        self.event_handler.update()

        position = self.event_handler.get_mouse_position()
        left_mouse_button = self.event_handler.get_mouse_clicked(0)

        if self.event_handler.get_key_pressed(pygame.K_w):
            scroll[1] -= 500/clock.get_fps()
        if self.event_handler.get_key_pressed(pygame.K_a):
            scroll[0] -= 500/clock.get_fps()
        if self.event_handler.get_key_pressed(pygame.K_s):
            scroll[1] += 500/clock.get_fps()
        if self.event_handler.get_key_pressed(pygame.K_d):
            scroll[0] += 500/clock.get_fps()

        self.world.show()
        self.world.render_current_selection(position)
        self.selector_panel.show()

        self.selector_panel.run(position, left_mouse_button)

        if not self.selector_panel.is_mouse_hovering(position):
            self.world.run(position, left_mouse_button)
            self.world.create_rectangle(position, self.event_handler.get_mouse_clicked(2))

        self.keyboard_commands()

    def keyboard_commands(self):
        #Keyboard shortcuts or commands
        ctrl_key = self.event_handler.get_key_pressed(pygame.K_LCTRL) or self.event_handler.get_key_pressed(pygame.K_RCTRL)

        if ctrl_key and self.event_handler.get_mouse_clicked(0):
            self.world.fill(self.event_handler.get_mouse_position())
        if ctrl_key and self.event_handler.get_key_pressed(pygame.K_t):
            self.world.autotile(self.selector_panel)
        if ctrl_key and self.event_handler.get_key_pressed(pygame.K_z):
            self.world.undo()
        if ctrl_key and self.event_handler.get_key_pressed(pygame.K_s):
            self.world.save()
        if self.event_handler.get_key_pressed(pygame.K_DELETE):
            self.world.delete()

    def event_loop(self):
        #Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Updates world on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.world.update()
            #Adds layer to the world according to the key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_UP:
                    self.world.add_layer(-1)
                if event.key == pygame.K_DOWN:
                    self.world.add_layer(1)
            #Updates screen
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    def main_loop(self):
        #Runs the event loop and run function continuously
        while True:
            self.event_loop()
            self.run()

            pygame.display.update()
