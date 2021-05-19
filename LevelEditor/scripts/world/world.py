from ..funcs import *
from .layer import Layer
from .image import Image
from .rectangle import Rectangle
import json, os

class World:
    def __init__(self, editor):
        self.editor = editor
        self.scroll = [0,0]
        self.rectangle = Rectangle(editor)
        self.layers = [Layer(editor, 0)]
        self.current_layer = self.layers[0]

    def render(self):
        #Renders the layers with alpha
        surface = pygame.Surface((self.editor.screen.get_width(), self.editor.screen.get_height()))
        surface.set_colorkey((0,0,0))
        surface.set_alpha(128)
        for layer in self.layers:
            layer.show(surface)

        self.editor.screen.blit(surface, (0,0))

        #Renders the current layer
        self.current_layer.show(self.editor.screen)

        #Renders the rectangle
        self.rectangle.show()

    def render_current_selection(self, position, selection):
        #Renders the current selected image, on the world
        if selection:
            surface = pygame.Surface(selection.image.get_size())
            surface.set_colorkey((0,0,0))
            surface.set_alpha(128)
            surface.blit(selection.image, (0,0))

            j, i = (position[0]+self.editor.world.scroll[0])//self.editor.res, (position[1]+self.editor.world.scroll[1])//self.editor.res
            self.editor.screen.blit(surface, ((j*self.editor.res-self.editor.world.scroll[0]), (i*self.editor.res-self.editor.world.scroll[1])))

    def run(self, clicked, position, selection):
        #Removes the rectangle and adds an image
        if not clicked:
            return

        self.rectangle.destroy()
        self.current_layer.add_image(position, selection)

    def fill(self, position, selection):
        #Fills the current layer
        self.current_layer.fill(position, selection)

    def autotile(self, selection_panel):
        #Autotiles all the images
        if len(self.rectangle.ending_location) != 0 and not self.rectangle.is_creating:
            images = self.get_images_within_rectangle()
            self.current_layer.autotile(images, selection_panel)

    def update(self, selection):
        #Updates the current layer
        self.current_layer.update(selection)

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
        n = self.current_layer.n - i

        for layer in self.layers:
            if layer.n == n:
                self.current_layer = layer
                return

        if self.current_layer.is_empty():
            return

        layer = Layer(self.editor, n)
        self.layers.append(layer)
        self.current_layer = layer

        def get_n(elem):
            return elem.n

        self.layers.sort(key=get_n)

    def save(self):
        #Saves the data (images) into a json file
        data = {}

        for layer in self.layers:
            for image in layer.images:
                data[f'{image.j};{image.i}:{layer.n}'] = [
                    image.id, image.filepath, image.index, image.scale
                ]

        file = open('data/saved.json', 'w')
        data = json.dump(data, file)
        file.close()

    def load(self, filename):
        #Opens the file
        data = json.load(open(filename, 'r'))

        for position, list in data.items():
            pos, layer = position.split(':')
            id, filepath, index, scale = list

            #Gets the specific layer for the image
            layer = self.get_layer(int(layer))
            path = f'data/graphics/spritesheet/{filepath}.png'

            #Loads image and offset
            try:
                image = load_images_from_spritesheet(path)[int(index)]
                dimensions = [image.get_width()*int(scale), image.get_height()*int(scale)]
                offset = self.load_image_offset(id, dimensions, int(index), image)

                image = pygame.transform.scale(image, dimensions)

            except Exception as e:
                try:
                    print('WORLD LOADING ERROR: ', e)
                    image = pygame.image.load(path).convert()
                    dimensions = [image.get_width()*int(scale), image.get_height()*int(scale)]
                    image.set_colorkey((0,0,0))

                    offset = self.load_image_offset(id, dimensions, int(index), image)

                    image = pygame.transform.scale(image, dimensions)
                except:
                    print('WORLD IMAGE LOADING ERROR: ignored image with path', path)

            #Loads the group name
            FILEPATH = 'data/configs/groups'
            for group in os.listdir(FILEPATH):
                for file in os.listdir(FILEPATH+'/'+group):
                    data = json.load(open(FILEPATH+'/'+group+'/'+file, 'r'))
                    data_filepath = data['filename'].split('.')[0].split('/')[-1]

                    if data['id'] == id and data_filepath == filepath:
                        group_name = group
                        break
                else:
                    continue
                break

            #Converts the position from string ('x;y') to int
            x, y = pos.split(';')
            x, y = int(float(x)), int(float(y))

            data = {
                'id': id,
                'filepath': filepath,
                'group_name': group_name,
                'image': image,
                'index': index,
                'scale': scale,
                'autotile_config_path': f'data/config/autotile/{id}_autotile_config.json'
            }

            #Loads the image object
            image_object = Image(self.editor, x, y, x*self.editor.res, y*self.editor.res, offset, data=data)

            #Adds the image to the layer
            layer.images.append(image_object)

    def load_image_offset(self, id, dimensions, index, image):
        #Loads offset
        try:
            offset_data = json.load(open(f'data/configs/offsets/{id}_offset.json', 'r'))
            offset = offset_data[str(index)]
            offset[0] *= dimensions[0]/image.get_width()
            offset[1] *= dimensions[1]/image.get_height()
        except Exception as e:
            offset = [0,0]

        return offset

    def get_layer(self, n):
        #Returns layer 'n' if already assigned
        for layer in self.layers:
            if layer.n == n:
                return layer

        #Else creates a new layer and assigns it 'n'
        layer = Layer(self.editor, n)
        self.layers.append(layer)
        return layer

    def delete(self):
        #Deletes all the images from the current layer within the rectangle
        if len(self.rectangle.ending_location) != 0 and not self.rectangle.is_creating:
            images = self.get_images_within_rectangle()
            self.current_layer.remove(images)
