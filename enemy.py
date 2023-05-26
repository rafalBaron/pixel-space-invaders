import pygame, random
from CONST import *


class Enemy(pygame.Rect):

    def __init__(self,x,y,type):

        self.x = x
        self.y = y
        self.h = 32
        self.w = 32
        self.type = str(type)
        self.direction = "left"

    def move(self):
        if self.direction == "left":
            self.x -= enemy_speed
            if self.x <= border:
                self.direction = "right"
                self.y += random.choice([30])
        else:
            self.x += enemy_speed
            if self.x >= draw_screen_size[0] - border - self.w:
                self.direction = "left"
                self.y += random.choice([30])