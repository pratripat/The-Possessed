import pygame
import json

#Initializing pygame and few parameters
pygame.init()

width = 1000
height = 700
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE+pygame.SCALED)
pygame.display.set_caption('Level Editor')

clock = pygame.time.Clock()

res = 48

rows = height//res
cols = width//res

scroll = [0,0]

colors = json.load(open('data/configs/colors.json', 'r'))

selection = {
    'image': None
}
