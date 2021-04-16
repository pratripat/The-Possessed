import pygame, sys, json

pygame.init()

width = 1000
height = 700
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
screen.set_colorkey((0,0,0))
pygame.display.set_caption('Platformer')

clock = pygame.time.Clock()

colors = json.load(open('data/configs/colors.json', 'r'))

directions = {'up': False, 'down': True, 'right': False, 'left': False}
gravity = 1
