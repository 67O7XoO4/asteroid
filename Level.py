import logging
import pygame
from pygame.locals import *
import math

TEXT_COLOR      = (255,255,255)
TEXT_SIZE       = 40

class Level(pygame.sprite.Sprite):
    """ level of the game """
    def __init__(self, pygame):
        """
        Args:
            pygame (_type_): pygame instance
        """
        super().__init__() 
        
        self.num = 0
        
        self.sysfont = pygame.font.SysFont(None, TEXT_SIZE)
        # is the text animated ?
        self.animate = False
        self.animationFrame=0
        self._update_image()
        
        
    def next(self):
        self.num +=1
        self._update_image()
        self.animate = True

        
    def _update_image(self):
        self.image = self.sysfont.render('Level: '+ str(self.num), True, TEXT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (4,8)
        self.original_image = self.image

                
    def update(self, pressed_keys):
        if self.animate:
                
            self.animationFrame+=1
            
            if self.animationFrame < 10:
                factor = self.animationFrame
                self.image = pygame.transform.scale(self.original_image, 
                                                    (self.rect.width+factor, self.rect.height+factor) )
            elif self.animationFrame < 20:
                factor = self.animationFrame - 10
                self.image = pygame.transform.scale(self.original_image, 
                                                    (self.rect.width-factor, self.rect.height-factor))
            elif self.animationFrame < 30:
                factor = self.animationFrame - 20
                self.image = pygame.transform.scale(self.original_image,
                                                    (self.rect.width+factor, self.rect.height+factor))
            elif self.animationFrame < 40:
                factor = self.animationFrame - 30
                self.image = pygame.transform.scale(self.original_image, 
                                                    (self.rect.width-factor, self.rect.height-factor))
            else:
                self.animate = False
                self.animationFrame=0
                self.image = self.original_image
                
            self.rect = self.image.get_rect()


    def on_out_of_bound(self, width, height):
        pass