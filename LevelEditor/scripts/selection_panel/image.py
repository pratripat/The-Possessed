class Image:
    def __init__(self, editor, index, scale, id, group_name, filepath, position, offset, image, autotile_config_path):
        self.editor = editor
        self.index = index
        self.scale = scale
        self.id = id
        self.filepath = filepath
        self.group_name = group_name
        self.position = position
        self.offset = offset
        self.image = image
        self.autotile_config_path = autotile_config_path

    #Renders the image
    def render(self):
        self.editor.screen.blit(self.image, self.position)

    #Returns if the mouse is over the image
    def clicked(self, position):
        return (
            position[0] > self.position[0] and
            position[1] > self.position[1] and
            position[0] < self.position[0]+self.image.get_width() and
            position[1] < self.position[1]+self.image.get_height()
        )
