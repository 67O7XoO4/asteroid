import random
import pygame
from pygame.locals import *
import math

DEFAULT_SPEED = 15

class ExplosionItem(pygame.sprite.Sprite):
    """ A debris projected in the space by an explosion """
    def __init__(self, loader, position, direction, big_one=False):
        """
        Args:
            loader : image loader instance
            position : (x,y) coordinate. start position of the sprite in the screen
            direction : in degree. in which direction the item goes
            big_one : is a big explosion ?
        """
        super().__init__() 
        # self.image and self.rect used to draw the sprite
        self.image = loader.loadImage(160*3-32, 160+96+32, 32, 32)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, 
                                        (self.rect.width/3, self.rect.height/3) )

        self.rect = self.image.get_rect()
        
        self.rect.center = position
                
        self.animate_frame=0
        if big_one:
            speed = DEFAULT_SPEED/3;
            self.animate_stop = random.randrange(32, 64)
        else:
            speed = DEFAULT_SPEED;
            self.animate_stop = random.randrange(4, 8)
        
        #speed projection on axes
        self.x_speed = speed*math.cos(math.radians(direction))
        self.y_speed =  - speed*math.sin(math.radians(direction))

        
    def update(self, pressed_keys):
        """ask the sprite to update itself """        
        if self.animate_frame < self.animate_stop:
            self.animate_frame +=1
            self.rect.move_ip(self.x_speed,self.y_speed)
        else:
            self.kill()            


    def on_out_of_bound(self, width, height):
        # remove it if out of bound
        self.kill()