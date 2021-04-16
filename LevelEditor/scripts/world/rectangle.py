from LevelEditor.settings import *

class Rectangle:
    def __init__(self):
        self.is_creating = False
        self.starting_location = []
        self.ending_location = []

    def show(self):
        #Renders the rectangle if the dimensions have been defined
        if len(self.ending_location) != 0:
            pygame.draw.rect(screen, colors['yellow'], (self.starting_location[0], self.starting_location[1], self.ending_location[0]-self.starting_location[0], self.ending_location[1]-self.starting_location[1]), 2)

    def create(self, location):
        if not self.is_creating:
            self.starting_location = location
            self.is_creating = True

        self.ending_location = location

    def finish(self, location):
        #Adds the last position
        self.ending_location = location
        self.is_creating = False

    def destroy(self):
        #Clears all the positions
        self.is_creating = False
        self.starting_location = []
        self.ending_location = []
