import pygame

class Mouse:
    def __init__(self):
        self.position = []
        self.clicked = []

    def update(self):
        #Updates the position and clicked to the pygame mouse
        self.position = pygame.mouse.get_pos()
        self.clicked = pygame.mouse.get_pressed()

class Keyboard:
    def __init__(self):
        self.keys_pressed = []

    def update(self):
        #Updates the key pressed
        self.keys_pressed = pygame.key.get_pressed()

class Event_Handler:
    def __init__(self):
        self.mouse = Mouse()
        self.keyboard = Keyboard()

    def update(self):
        #Handles the mouse and keyboard object
        self.mouse.update()
        self.keyboard.update()

    def get_key_pressed(self, key):
        #Returns if the key is pressed or not
        return self.keyboard.keys_pressed[key]

    def get_mouse_position(self):
        #Returns the position of the mouse
        return self.mouse.position

    def get_mouse_clicked(self, button):
        #Returns if the mouse is clicked
        return self.mouse.clicked[button]
