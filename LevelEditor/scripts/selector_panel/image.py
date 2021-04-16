from LevelEditor.settings import *

class Image:
    def __init__(self, position, offset, image, id, index, autotile_config_path):
        self.position = position
        self.offset = offset
        self.image = image
        self.id = id
        self.index = index
        self.autotile_config_path = autotile_config_path

    def show(self):
        #Rendering image
        screen.blit(self.image, self.position)

    def is_clicked(self, position):
        #Checking if the mouse has clicked the image
        x, y = position

        return (
            x > self.position[0] and
            x < self.position[0] + self.get_width() and
            y > self.position[1] and
            y < self.position[1] + self.get_height()
        )

    def get_width(self):
        #Returns image width
        return self.image.get_width()

    def get_height(self):
        #Returns image height
        return self.image.get_height()
