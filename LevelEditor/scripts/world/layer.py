from .image import Image

class Layer:
    def __init__(self, editor, n):
        self.editor = editor
        self.images = []
        self.updates = []
        self.undo_cooldown = 0
        self.initial_undo_cooldown = 50
        self.n = n

    def show(self, surface=None):
        if not surface:
            surface = self.editor.screen

        #Renders images
        for image in self.images:
            image.show(surface)

        if self.undo_cooldown > 0:
            self.undo_cooldown -= 1

    def add_image(self, position, selection):
        #Adds an image if there is already a selected image from the selector panel
        if selection:
            j, i = (position[0]+self.editor.world.scroll[0])//self.editor.res, (position[1]+self.editor.world.scroll[1])//self.editor.res
            offset = selection.offset

            image = self.get_image_with_index(i, j)

            if image:
                img = Image(self.editor, j, i, j*self.editor.res, i*self.editor.res, offset, selection=selection)
                self.images.append(img)
                self.images.remove(image)
                return img
            else:
                image = Image(self.editor, j, i, j*self.editor.res, i*self.editor.res, offset, selection=selection)
                self.images.append(image)
                return image

    def fill(self, position, selection):
        #Fills images at the required location
        image = self.add_image(position, selection)
        image.fill(self.images, selection)

    def autotile(self, images, selection_panel):
        #Auto tile all the images within the rectangle
        for image in images:
            selection_panel_images = selection_panel.get_images_with_name(image.group_name)
            image.autotile(self.images, selection_panel_images)

    def update(self, selection):
        #Adds a copy of images for later undoing
        if selection:
            images = []
            for image in self.images:
                data = {
                    'id': image.id,
                    'filepath': image.filepath,
                    'group_name': image.group_name,
                    'image': image.image,
                    'index': image.index,
                    'scale':image.scale
                }

                img = Image(self.editor, image.j, image.i, image.position[0], image.position[1], image.offset, data=data)
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
