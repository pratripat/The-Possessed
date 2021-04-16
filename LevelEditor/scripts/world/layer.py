from LevelEditor.settings import *
from .image import Image

class Layer:
    def __init__(self, n):
        self.images = []
        self.updates = []
        self.undo_cooldown = 0
        self.initial_undo_cooldown = 50
        self.n = n

    def show(self, surface=screen):
        #Renders images
        for image in self.images:
            image.show(surface)

        if self.undo_cooldown > 0:
            self.undo_cooldown -= 1

    def add_image(self, position):
        #Adds an image if there is already a selected image from the selector panel
        if selection['image']:
            j, i = (position[0]+scroll[0])//res, (position[1]+scroll[1])//res
            offset = selection['image'].offset

            image = self.get_image_with_index(i, j)

            if image:
                img = Image(j, i, j*res, i*res, offset)
                self.images.append(img)
                self.images.remove(image)
                return img
            else:
                image = Image(j, i, j*res, i*res, offset)
                self.images.append(image)
                return image

    def fill(self, position):
        #Fills images at the required location
        image = self.add_image(position)
        image.fill(self.images)

    def autotile(self, images, selector_panel):
        #Auto tile all the images within the rectangle
        for image in images:
            selector_panel_images = selector_panel.get_image_with_id(image.id)
            image.autotile(self.images, selector_panel_images)

    def update(self):
        #Adds a copy of images for later undoing
        if selection['image']:
            images = []
            for image in self.images:
                img = Image(image.j, image.i, image.position[0], image.position[1], image.offset, data={'id': image.id, 'image': image.image, 'index': image.index})
                img.image = image.image
                img.id = image.id
                img.autotile_config = image.autotile_config
                images.append(img)

            self.updates.append(images)
            self.updates[-200:]

    def undo(self):
        #Undos
        if self.undo_cooldown == 0 and len(self.updates) != 0:
            self.images = self.updates.pop()
            self.undo_cooldown = self.initial_undo_cooldown

    def remove(self, images):
        #Removes images within the rectangle
        for image in images:
            if image in self.images[:]:
                self.images.remove(image)

    def get_image_with_index(self, i, j):
        #Returns images within rectangle
        for image in self.images:
            if image.i == i and image.j == j:
                return image

        return None

    def is_empty(self):
        #Returns if the layer has no images currently
        return len(self.images) == 0
