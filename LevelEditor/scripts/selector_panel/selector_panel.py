from LevelEditor.settings import *
from .selector import Selector
import json

class Selector_Panel:
    def __init__(self, w, h):
        self.w = w
        self.h = h

        self.initialize_selectors()

    def show(self):
        #Rendering background
        pygame.draw.rect(screen, colors['selector'], (0,0,self.w, self.h))

        #Rendering the names of the selectors
        for selector in self.selectors:
            selector.show_label()

        #Showing the images of the selectors
        self.current_selector.show()

    def run(self, position, clicked):
        if clicked:
            for selector in self.selectors:
                if selector.is_clicked(position):
                    #If the selector is clicked, setting it to the current selector
                    self.current_selector = selector
                    selection['image'] = selector.selected_image
                    break

        #Updating the current selector
        self.current_selector.run(position, clicked)

    def initialize_selectors(self):
        self.selectors = []

        #Loads the json file for the selector configuration
        data = json.load(open('data/configs/selectors.json', 'r'))

        x = 10
        y = 10

        for entity in data:
            filename = data[entity]['spritesheet_path']
            id = data[entity]['id']
            resize = data[entity]['resize']
            scale = data[entity]['scale']
            autotile_config_path = data[entity]['autotile_config']

            position = [x, y]

            #Adding the selectors to the selector panel
            selector = Selector(position, filename, id, autotile_config_path, resize, scale)
            selector.load_images(len(data)*20+10)
            self.selectors.append(selector)

            y += 20

        #The current selector is the first selector
        self.current_selector = self.selectors[0]

    def get_image_with_id(self, id):
        #Returns selector's image if the selector's id is the same as the given id
        for selector in self.selectors:
            if selector.id == id:
                return selector.images

        return []

    def is_mouse_hovering(self, position):
        #Returns if the mouse is hovering over the selector panel
        return (
            position[0] < self.w and
            position[1] < self.h
        )
