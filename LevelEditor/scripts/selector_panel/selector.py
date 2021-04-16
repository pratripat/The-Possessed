from LevelEditor.settings import *
from LevelEditor.scripts.funcs import load_images_from_spritesheet
from .image import Image
import json

class Selector:
    def __init__(self, position, filename, id, autotile_config_path, resize, scale):
        self.position = position
        self.filename = filename
        self.id = id
        self.autotile_config_path = autotile_config_path
        self.resize = resize
        self.scale = scale

        self.images = []
        self.selected_image = None
        self.font = pygame.font.SysFont('comicsans', 30)
        self.label = self.font.render(self.id.capitalize(), 1, colors['white'])

    def show_label(self):
        #Renders the name of the selector
        screen.blit(self.label, self.position)

    def show(self):
        #Renders the images
        for image in self.images:
            image.show()

        #Renders border over the current selected image
        if self.selected_image:
            pygame.draw.rect(screen, colors['yellow'], (self.selected_image.position[0], self.selected_image.position[1], self.selected_image.get_width(), self.selected_image.get_height()), 2)

    def run(self, position, clicked):
        if clicked:
            for image in self.images:
                if image.is_clicked(position):
                    #Sets the current image to the image the mouse is over
                    self.selected_image = image
                    selection['image'] = image
                    break

    def load_images(self, position):
        x = 10
        y = position

        images = load_images_from_spritesheet(self.filename)

        if len(images) == 0:
            try:
                image = pygame.image.load(self.filename)
                dimensions = self.load_image_dimensions(image)
                offset = self.load_image_offset(image, dimensions, 0)
                image = pygame.transform.scale(image, dimensions)
                self.images.append(Image([x, y], offset, image, self.id, 0, self.autotile_config_path))
            except Exception as e:
                print(e)
                print(f'{self.filename} may have caused the problem?')

            return

        for i, image in enumerate(images):
            if y > height:
                x += res+10
                y = 100

            dimensions = self.load_image_dimensions(image)
            offset = self.load_image_offset(image, dimensions, i)

            image = pygame.transform.scale(image, dimensions)

            #Adds the images to the selector images list
            self.images.append(Image([x, y], offset, image, self.id, i, self.autotile_config_path))

            y += image.get_height()+10

    def load_image_offset(self, image, dimensions, i):
        try:
            data = json.load(open(f'data/configs/offsets/{self.id}_offset.json', 'r'))
            offset = data[i]
            offset[0] *= dimensions[0]/image.get_width()
            offset[1] *= dimensions[1]/image.get_height()
        except:
            offset = [0,0]

        return offset

    def load_image_dimensions(self, image):
        if self.resize:
            if self.scale:
                dimensions = (image.get_width()*self.scale, image.get_height()*self.scale)
            else:
                dimensions = (res, res)

        return dimensions

    def is_clicked(self, position):
        #Returns if the selector is clicked
        x, y = position

        return (
            x > self.position[0] and
            x < self.position[0] + self.get_width() and
            y > self.position[1] and
            y < self.position[1] + self.get_height()
        )

    def get_width(self):
        #Returns image width
        return self.label.get_width()

    def get_height(self):
        #Returns image height
        return self.label.get_height()
