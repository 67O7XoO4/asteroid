import logging
import pygame
from pygame.locals import *
import math

TEXT_COLOR      = (255,255,255)
TEXT_SIZE       = 40

class Score(pygame.sprite.Sprite):
    """ Score of the game """
    def __init__(self, pygame, center):
        """
        Args:
            pygame : pygame instance
        """
        super().__init__() 
        
        self.score = 0
        self.sysfont = pygame.font.SysFont(None, TEXT_SIZE)
        self.center = center
        self._update_image()
        
    def _update_image(self):
        self.image = self.sysfont.render(str(self.score), True, TEXT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (self.center, 24)
        
    def increment(self, inc=1):
        self.score+=inc
        
        
    def update(self, pressed_keys):
        self._update_image()

    def on_out_of_bound(self, width, height):
        pass