import os
import pygame
from pygame.locals import *
import math

from AssetLoader import AssetLoader

DEFAULT_SPEED = 12

class Missile(pygame.sprite.Sprite):
    """ a missile shot by the player """
    def __init__(self, assetLoader : AssetLoader, position, direction):
        """
        Args:
            pygame : pygame instance
            position : (x,y) coordinate. start position of the sprite in the screen
            direction : in degree. in which direction the missile goes
        """
        super().__init__() 
        
        assetLoader.playSound('fire')
        
        # self.image and self.rect used to draw the sprite
        self.image = self.image = assetLoader.loadImage(160*3, 160+96+32, 32, 32)
        self.rect = self.image.get_rect()
        
        self.rect.center = position
        
        #speed projection on axes
        self.x_speed = DEFAULT_SPEED*math.cos(math.radians(direction))
        self.y_speed =  - DEFAULT_SPEED*math.sin(math.radians(direction))
        
        
    def update(self, pressed_keys):
        """ask the sprite to update itself """        
        self.rect.move_ip(self.x_speed,self.y_speed)


    def on_out_of_bound(self, width, height):
        # remove the missile from the game if out of bound
        self.kill()
        
    def set_collided(self):
        return 0