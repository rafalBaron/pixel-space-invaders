import pygame
from CONST import *


class Player(pygame.Rect):

    def __init__(self):
        self.x = int(draw_screen_size[0]/2)
        self.y = 147
        self.h = 32
        self.w = 32
        self.hp = 3
