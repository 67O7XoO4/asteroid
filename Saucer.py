import random
import pygame
from pygame.locals import *
import math
import logging


class Saucer(pygame.sprite.Sprite):
    """ a flying saucer over the space """

    MAX_Y_SPEED = 4

    def __init__(self, loader, screen_size = None, on_flying_saucer_killed=None):
        """
         create an fying saucer starting from the edge of the screen 
        Args:
            pygame (_type_): the pygame instance
            screen_size (_type_): width and height of the screen
        """
        super().__init__() 

        # saucer type: bigger (1) or smaller (2)
        self.type = random.randrange(1, 3)
        # callback function to notify when the flying saucer is killed
        self.on_flying_saucer_killed = on_flying_saucer_killed            
        
        # saucer shape
        self.image = loader.loadImage(160*3 - 64, 160, 96, 80)
        
        self.rect = self.image.get_rect()
        # scale image according to the asteroid type
        self.image = pygame.transform.scale(self.image, (self.rect.width/self.type, self.rect.height/self.type))
        self.rect = self.image.get_rect()

        # start position
        # choose from where does the saucer come (left or right)          
        match random.randrange(1, 3):
            case 1:
                # from the left
                self.rect.top = random.randrange(self.rect.height, screen_size[1] - self.rect.height)
                self.rect.right = 2
                self.x_direction = 1
            case 2:
                # from the right
                self.rect.top = random.randrange(self.rect.height, screen_size[1] - self.rect.height)
                self.rect.left = screen_size[0] - 2
                self.x_direction = -1
                
                
        #speed projection 
        self.x_speed  = self.x_direction*(1 + random.randrange(0, 4))
        self.y_speed  = random.randrange(-1, 2)

               
    def set_collided(self) -> int:
        """ saucer has collided. Return the score value  """        
        self.kill()
        self.on_flying_saucer_killed() 
        match self.type:
            case 1:     
                value = 200
            case 2:     
                value = 1000
        return value


    def update(self, pressed_keys):
        self.rect.move_ip(self.x_speed,self.y_speed)
        
        match random.randrange(1, 10):
            case 1:
                self.y_speed = min (Saucer.MAX_Y_SPEED, self.y_speed  + 1)
            case 2:
                self.y_speed = max (- Saucer.MAX_Y_SPEED, self.y_speed  - 1)
            case other:
                pass # stay the same
        
        
    def on_out_of_bound(self, width, height):
        """ when saucer goes out from left or right edge of the screen
           it disappears   """
        rect = self.rect
        if rect.right < 0:
            self.kill()
            self.on_flying_saucer_killed()
            
        if rect.left > width:
            self.kill()
            self.on_flying_saucer_killed()
        
        if rect.top > height:
            rect.bottom= 1

        if rect.bottom < 0:
            rect.top = height - 1

