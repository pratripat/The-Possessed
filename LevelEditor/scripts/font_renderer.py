import pygame
import sys
from .funcs import *

class Font:
    def __init__(self, filename):
        self.filename = filename
        self.characters = [chr(i) for i in range(33, 97)]
        self.space_width = 10
        self.load_characters()

    #Loads all the images from the spritesheet
    def load_characters(self):
        self.images = []
        images = load_images_from_spritesheet(self.filename+'.png')

        for image in images:
            self.images.append(image)

    #Returns the surface on which the text will be rendered
    def get_surface(self, text):
        width = 0
        height = 0

        for chr in text:
            if chr in self.characters:
                index = self.characters.index(chr)
                image = self.images[index]

                width += image.get_width()

                if image.get_height() > height:
                    height = image.get_height()
            elif chr == ' ':
                width += self.space_width

        surface = pygame.Surface((width, height))
        surface.set_colorkey((0,0,0))

        return surface

    #Changes the color of the text
    def change_color(self, surface, old_color, new_color):
        surface.set_colorkey(old_color)
        surf = surface.copy()
        surf.fill(new_color)
        surf.blit(surface, (0,0))
        return surf

    #Renders the text on the surface
    def render(self, screen, text, position, center=(False, False), scale=1, color=None, background_color=None):
        text = text.upper()
        surface = self.get_surface(text)
        surface = pygame.transform.scale(surface, (round(surface.get_width()*scale), round(surface.get_height()*scale)))
        temp_pos = [0,0]

        for chr in text:
            if chr in self.characters:
                index = self.characters.index(chr)
                image = self.images[index]
                image = pygame.transform.scale(image, (round(image.get_width()*scale), round(image.get_height()*scale)))

                surface.blit(image, temp_pos)

                temp_pos[0] += image.get_width()
            elif chr == ' ':
                temp_pos[0] += self.space_width

        if color:
            surface = self.change_color(surface, (255,0,0), color)
            surface.set_colorkey((0,0,0))

        if center[0]:
            position = [position[0]-surface.get_width()/2, position[1]]
        if center[1]:
            position = [position[0], position[1]-surface.get_height()/2]

        if background_color:
            background = pygame.Surface(surface.get_size())
            background.fill(background_color)
            screen.blit(background, position)

        screen.blit(surface, position)
