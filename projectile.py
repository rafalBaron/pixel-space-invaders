import pygame
from CONST import *

class Projectile(pygame.Rect):

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.h = 19
        self.w = 8
        self.type = str(type)

    def move(self):
        if self.type == "1":
            self.y -= projectile_speed
        else:
            self.y += projectile_speed