from LevelEditor.settings import *
from LevelEditor.scripts.funcs import *
from .layer import Layer
from .image import Image
from .rectangle import Rectangle
import json

class World:
    def __init__(self):
        self.rectangle = Rectangle()
        self.layers = [Layer(0)]
        self.current_layer = self.layers[0]

    def show(self):
        #Renders background
        screen.fill(colors['world'])

        #Renders the layers with alpha
        surface = pygame.Surface((screen.get_width(), screen.get_height()))
        surface.set_colorkey(colors['black'])
        surface.set_alpha(128)
        for layer in self.layers:
            layer.show(surface)

        screen.blit(surface, (0,0))

        #Renders the current layer
        self.current_layer.show(screen)

        #Renders the rectangle
        self.rectangle.show()

    def render_current_selection(self, position):
        #Renders the current selected image, on the world
        if selection['image']:
            surface = pygame.Surface(selection['image'].image.get_size())
            surface.set_colorkey(colors['black'])
            surface.set_alpha(128)
            surface.blit(selection['image'].image, (0,0))

            j, i = (position[0]+scroll[0])//res, (position[1]+scroll[1])//res
            screen.blit(surface, ((j*res-scroll[0]), (i*res-scroll[1])))

    def run(self, position, clicked):
        #Removes the rectangle and adds an image
        if clicked:
            self.rectangle.destroy()
            self.current_layer.add_image(position)

    def fill(self, position):
        #Fills the current layer
        self.current_layer.fill(position)

    def autotile(self, selector_panel):
        #Autotiles all the images
        if len(self.rectangle.ending_location) != 0 and not self.rectangle.is_creating:
            images = self.get_images_within_rectangle()
            self.current_layer.autotile(images, selector_panel)

    def update(self):
        #Updates the current layer
        self.current_layer.update()

    def undo(self):
        #Undos something in the current layer
        self.current_layer.undo()

    def create_rectangle(self, position, clicked):
        #Creates rectangle
        if clicked:
            self.rectangle.create(position)
        else:
            if self.rectangle.is_creating:
                self.rectangle.finish(position)

    def get_images_within_rectangle(self):
        #Returns image within the rectangle
        images = []

        for image in self.current_layer.images:
            if image.within(self.rectangle.starting_location, self.rectangle.ending_location):
                images.append(image)

        return images

    def add_layer(self, i):
        #Adds layers to the world if there is not any
        def get_n(elem):
            return elem.n

        n = self.current_layer.n - i

        for layer in self.layers:
            if layer.n == n:
                self.current_layer = layer
                return

        if self.current_layer.is_empty():
            return

        layer = Layer(n)
        self.layers.append(layer)
        self.current_layer = layer

        self.layers.sort(key=get_n)

    def save(self):
        #Saves the data (images) into a json file
        data = {}
        i = 0

        for layer in self.layers:
            for image in layer.images:
                data[str(i)] = {
                    'id': image.id,
                    'position': [image.j, image.i],
                    'index': image.index,
                    'layer': layer.n,
                    'dimensions': image.image.get_size()
                }
                i += 1

        file = open('data/saved.json', 'w')
        data = json.dump(data, file)
        file.close()

    def load(self, filename):
        data = json.load(open(filename, 'r'))

        for i in data:
            entity = data[i]
            layer = entity['layer']
            id = entity['id']
            index = entity['index']
            dimensions = entity['dimensions']
            position = entity['position']

            layer = self.get_layer(layer)
            path = f'data/graphics/spritesheet/{id}.png'

            try:
                image = load_images_from_spritesheet(path)[index]

                offset = self.load_image_offset(id, dimensions, index, image)

                image = pygame.transform.scale(image, dimensions)
            except:
                image = pygame.image.load(path).convert()
                image.set_colorkey((0,0,0))

                offset = self.load_image_offset(id, dimensions, index, image)

                image = pygame.transform.scale(image, dimensions)

            image_object = Image(*position, position[0]*res, position[1]*res, offset, {'image':image, 'index':index, 'id':id})
            layer.images.append(image_object)

    def load_image_offset(self, id, dimensions, index, image):
        try:
            offset_data = json.load(open(f'data/configs/offsets/{id}_offset.json', 'r'))
            offset = offset_data[str(index)]
            offset[0] *= dimensions[0]/image.get_width()
            offset[1] *= dimensions[1]/image.get_height()
        except Exception as e:
            offset = [0,0]

        return offset

    def get_layer(self, n):
        for layer in self.layers:
            if layer.n == n:
                return layer

        layer = Layer(n)
        self.layers.append(layer)
        return layer

    def delete(self):
        #Deletes all the images from the current layer within the rectangle
        if len(self.rectangle.ending_location) != 0 and not self.rectangle.is_creating:
            images = self.get_images_within_rectangle()
            self.current_layer.remove(images)
