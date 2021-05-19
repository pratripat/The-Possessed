from ..funcs import load_images_from_spritesheet
import pygame, json

class Image:
    def __init__(self, editor, j, i, x, y, offset, data=None, selection=None):
        self.editor = editor
        self.i = i
        self.j = j
        self.position = [x,y]
        self.offset = offset

        if data:
            self.id = data['id']
            self.filepath = data['filepath']
            self.group_name = data['group_name']
            self.image = data['image']
            self.index = data['index']
            self.scale = data['scale']
        elif selection:
            self.id = selection.id
            self.filepath = selection.filepath
            self.group_name = selection.group_name
            self.image = selection.image
            self.index = selection.index
            self.scale = selection.scale

        try:
            if selection:
                self.autotile_config = json.load(open(selection.autotile_config_path, 'r'))
                return

            self.autotile_config = json.load(open(data['autotile_config_path'], 'r'))
        except:
            self.autotile_config = None

    def show(self, surface=None):
        if not surface:
            surface = self.editor.screen
        #Renders the image according to the self.editor.world.scroll
        surface.blit(self.image, [self.position[0]+self.offset[0]-self.editor.world.scroll[0], self.position[1]+self.offset[1]-self.editor.world.scroll[1]])

    def fill(self, images, selection, depth=950):
        if depth == 0:
            return

        for dir in [(0,-1), (1,0), (0,1), (-1,0)]:
            i, j = self.i+dir[1], self.j+dir[0]

            if i-self.editor.world.scroll[1]//self.editor.res >= 0 and i-self.editor.world.scroll[1]//self.editor.res < self.editor.screen.get_height()//self.editor.res+1 and j-self.editor.world.scroll[0]//self.editor.res >= 0 and j-self.editor.world.scroll[0]//self.editor.res < self.editor.screen.get_width()//self.editor.res+1:
                neighbor = self.get_image_with_index(i, j, images)

                #If the neighbor is not yet defined, the neighbor becomes an image object and is put into the images list
                if not neighbor:
                    neighbor = Image(self.editor, j, i, j*self.editor.res, i*self.editor.res, self.offset, selection=selection)
                    images.append(neighbor)
                    neighbor.fill(images, selection, depth-1)

    def autotile(self, images, selector_panel_images):
        if self.autotile_config:
            neighbors = self.get_neighbors(images)

            binary = '0000'

            #Sets binary according to the neighbors around the image
            for neighbor in neighbors:
                if neighbor and neighbor.id == self.id:
                    binary += '1'
                else:
                    binary += '0'

            #Gets the image according to the binary and the configuration file
            try:
                key = str(int(binary, 2))
                index = self.autotile_config[key]

                images = load_images_from_spritesheet(f'data/graphics/spritesheet/{self.filepath}.png')
                image = images[index]

                self.image = pygame.transform.scale(image, (image.get_width()*self.scale, image.get_height()*self.scale))
                self.index = index

                try:
                    offset_data = json.load(open(f'data/configs/offsets/{self.id}_offset.json', 'r'))
                    offset = offset_data[str(self.index)]
                    offset[0] *= self.scale
                    offset[1] *= self.scale
                except Exception as e:
                    # print(e)
                    offset = [0,0]

                self.offset = offset

            except Exception as e:
                print('AUTOTILE ERROR: ', e)

    def get_neighbors(self, images):
        #Returns neighbor images
        neighbors = []

        for dir in [(0,-1), (1,0), (0,1), (-1,0)]:
            i, j = self.i+dir[1], self.j+dir[0]
            if i-self.editor.world.scroll[1]//self.editor.res >= 0 and i-self.editor.world.scroll[1]//self.editor.res < self.editor.screen.get_height()//self.editor.res+1 and j-self.editor.world.scroll[0]//self.editor.res >= 0 and j-self.editor.world.scroll[0]//self.editor.res < self.editor.screen.get_width()//self.editor.res+1:
                neighbor = self.get_image_with_index(i, j, images)
                neighbors.append(neighbor)

        return neighbors

    def get_neighbors_diagonally(self, images):
        neighbors = []

        for dir in [(-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0)]:
            i, j = self.i+dir[1], self.j+dir[0]
            if i-self.editor.world.scroll[1]//self.editor.res >= 0 and i-self.editor.world.scroll[1]//self.editor.res < self.editor.screen.get_height()//self.editor.res+1 and j-self.editor.world.scroll[0]//self.editor.res >= 0 and j-self.editor.world.scroll[0]//self.editor.res < self.editor.screen.get_width()//self.editor.res+1:
                neighbor = self.get_image_with_index(i, j, images)
                neighbors.append(neighbor)

        return neighbors

    def get_image_with_index(self, i, j, images):
        #Returns image with the same given index (i, j)
        for image in images:
            if image.i == i and image.j == j:
                return image

        return None

    def within(self, starting, ending):
        #Returns image if it is within the rectangle dimension
        sx, sy = starting[0]+self.editor.world.scroll[0], starting[1]+self.editor.world.scroll[1]
        ex, ey = ending[0]+self.editor.world.scroll[0], ending[1]+self.editor.world.scroll[1]

        return (
            self.position[0] > sx and
            self.position[1] > sy and
            self.position[0]+self.get_width() < ex and
            self.position[1]+self.get_height() < ey
        )

    def get_width(self):
        #Returns image width
        return self.image.get_width()

    def get_height(self):
        #Returns image height
        return self.image.get_height()
