import pygame, os, sys, json

animation_path = 'data/graphics/animations'

class Animation_Data:
    def __init__(self, path, colorkey=(0,0,0)):
        self.path = path
        self.load_frames(colorkey)
        self.load_config()

    #Loads all the animation frames(sorted) and stores it
    def load_frames(self, colorkey):
        paths = []
        self.images = []

        for file in os.listdir(self.path):
            if file.split('.')[-1] == 'png':
                path = self.path+'/'+file
                paths.append(path)

        try:
            paths.sort()
        except Exception as e:
            print(e)
            print('could not sort the animation ->'+self.path)

        for path in paths:
            image = pygame.image.load(path).convert()
            image.set_colorkey(colorkey)
            self.images.append(image)

    #Loads animation configuration
    def load_config(self):
        try:
            self.config = json.load(open(self.path+'/'+'config.json', 'r'))
        except:
            print('not able to load file, using default configuration of animation..')
            self.config = {
                'frames': [5 for _ in range(len(self.images))],
                'loop': True,
                'speed': 1,
                'scale': 1,
                'centered': False
            }
            file = open(self.path+'/'+'config.json', 'w')
            file.write(json.dumps(self.config))
            file.close()

    #Returns total number of frames of the animation
    def get_frames(self):
        return self.config['frames']

    #Returns all the frames in the form of images
    def get_images(self):
        return self.images

    #Returns the scale of the animation
    def get_scale(self):
        return self.config['scale']

    #Returns the time taken(in frames) to finish the animation
    def duration(self):
        return sum(self.config['frames'])

class Animation:
    def __init__(self, animation_data):
        self.animation_data = animation_data
        self.frame = 0
        self.load_image()

    #Gets the image from the current frame
    def load_image(self):
        frames = self.animation_data.get_frames()
        images = self.animation_data.get_images()
        scale = self.animation_data.get_scale()
        self_frame = self.frame

        for i, frame in enumerate(frames):
            if self_frame > frame:
                self_frame -= frame
            else:
                self.image = pygame.transform.scale(images[i], (round(images[i].get_width()*scale), round(images[i].get_height()*scale)))
                break

    #Renders the current image
    def render(self, surface, position, flipped, colorkey):
        offset = [0,0]
        image = self.image
        if flipped:
            image = pygame.transform.flip(self.image, True, False)
        if colorkey:
            image.set_colorkey(colorkey)

        if self.animation_data.config['centered']:
            offset[0] -= image.get_width()//2
            offset[1] -= image.get_height()//2

        surface.blit(image, (position[0]+offset[0], position[1]+offset[1]))

    #Updates the current frame according to delta time
    def run(self, dt):
        self.frame += dt*60*self.animation_data.config['speed']

        if self.frame > self.animation_data.duration():
            if self.animation_data.config['loop']:
                self.frame = 0
            else:
                self.frame = self.animation_data.duration()

        self.load_image()

    #The current image
    @property
    def current_image(self):
        return self.image

#Loads all the animations from the animations folder
class Animation_Handler:
    def __init__(self):
        self.animations = {}

        for animation in os.listdir(animation_path):
            self.animations[animation] = Animation_Data(animation_path+'/'+animation)

    #Returns animation with the animation id
    def get_animation(self, animation_id):
        return Animation(self.animations.get(animation_id))
