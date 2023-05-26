import pygame

class Life(pygame.Rect):

    def __init__(self,x):
        self.x = x
        self.y = 2
        self.h = 16
        self.w = 16