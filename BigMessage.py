import logging
import pygame
from pygame.locals import *
import math

TEXT_COLOR      = (255,255,255)
TEXT_SIZE       = 200

class BigMessage(pygame.sprite.Sprite):
    """ Message "Game over" """
    def __init__(self, pygame, message, position, remove_after_display=False):
        """
        Args:
            pygame (_type_): pygame instance
        """
        super().__init__() 
        
        self.sysfont = pygame.font.SysFont(None, TEXT_SIZE)
        # is the text animated ?
        self.animate = True
        self.animationFrame=0
        # is the message to be removed after animation display ?
        self.remove_after_display = remove_after_display
        
        self.image = self.sysfont.render(message, True, TEXT_COLOR)
        self.rect = self.image.get_rect()

        self.position = position
        self.rect.center = position
        self.original_image = self.image

                
    def update(self, pressed_keys):
        if self.animate:
                
            self.animationFrame+=1

            if self.animationFrame < 50:
                self.image = pygame.transform.scale_by(self.original_image,  self.animationFrame*2/100)
                self.rect = self.image.get_rect()
                self.rect.center = self.position
        
            else:
                self.animate = False
                self.animationFrame=0
        elif self.remove_after_display:
            self.kill()
        

    def on_out_of_bound(self, width, height):
        pass