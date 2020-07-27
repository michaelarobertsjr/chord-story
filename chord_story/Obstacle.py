
import random
import pygame


class Obstacle:
    def __init__(self, stringNo):

        num = int(stringNo)

        if num == 5:
            self._rect = pygame.Rect((300, 15, 15, 15))
        if num == 4:
            self._rect = pygame.Rect((300, 45, 15, 15))
        if num == 3:
            self._rect = pygame.Rect((300, 75, 15, 15))
        if num == 2:
            self._rect = pygame.Rect((300, 105, 15, 15))
        if num == 1:
            self._rect = pygame.Rect((300, 135, 15, 15))
        if num == 0:
            self._rect = pygame.Rect((300, 165, 15, 15))

        self._color = (255, 255, 255)
        self._stringNum = num

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        self._rect = rect

    @property
    def stringNum(self):
        return self._stringNum

    @stringNum.setter
    def stringNum(self, stringNum):
        self._stringNum = stringNum

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color