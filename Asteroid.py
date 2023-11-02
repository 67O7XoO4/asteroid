import random
import pygame
from pygame.locals import *
import math
import logging


class Asteroid(pygame.sprite.Sprite):
    """ an asteroid flying over the space """

    DEFAULT_SPEED = 2
    MAX_TYPE = 3

    def __init__(self, loader, screen_size = None, parent_asteroid = None):
        """
         create an Asteroid from a parent asteroid (passing the parent_asteroid parameter)
         *OR* from the edge of the screen (passing the screen_size parameter)
        Args:
            pygame (_type_): the pygame instance
            screen_size (_type_): width and height of the screen
            parent_asteroid (_type_): another asteroid
        """
        super().__init__() 
        
        if parent_asteroid is None:
            # asteroid type: bigger to smaller : #1, #2 or #3 (but not #3) 
            self.type = random.randrange(1, 3)
        else:
            # create an asteroid from a bigger one 
            # asteroid type smaller  
            self.type = parent_asteroid.type + 1
            
        # where the asteroid goes
        angle = random.randrange(-60, 60)
        # and at the given speed
        speed = Asteroid.DEFAULT_SPEED + random.randrange(-1, 2)

        # needed to operate asteroid rotation
        self.rotate_angle = 0
        self.rotation_speed = random.randrange(-5, 6);

        # random asteroid shape
        match random.randrange(1, 4):
            case 1:     
                self.image = loader.loadImage(0, 0, 160, 160)
            case 2:     
                self.image = loader.loadImage(160, 0, 160, 160)
            case 3:     
                self.image = loader.loadImage(160*2, 0, 160, 160)
        
        self.rect = self.image.get_rect()
        # scale image according to the asteroid type
        self.image = pygame.transform.scale(self.image, (self.rect.width/self.type, self.rect.height/self.type))
        self.rect = self.image.get_rect()
        # save original image to enable image rotating
        self.original_image = self.image 
        self.original_rect = self.rect;

        # start position
        if parent_asteroid is None:
            # choose from where does the asteroid come (from what border of the screen)          
            match random.randrange(1, 5):
                case 1:
                    # from the top
                    self.rect.bottom = 2
                    self.rect.left = random.randrange(self.rect.width, screen_size[0] - self.rect.width)
                    
                    angle += 270  
                case 2:
                    # from the bottom
                    self.rect.top = screen_size[1] - 2
                    self.rect.left = random.randrange(self.rect.width, screen_size[0] - self.rect.width)
                    
                    angle += 90
                case 3:
                    # from the left
                    self.rect.top = random.randrange(self.rect.height, screen_size[1] - self.rect.height)
                    self.rect.right = 2
                    
                    angle += 0 # just to be fair
                case 4:
                    # from the right
                    self.rect.top = random.randrange(self.rect.height, screen_size[1] - self.rect.height)
                    self.rect.left = screen_size[0] - 2
                    
                    angle += 180
        else:
            self.rect.center = parent_asteroid.original_rect.center

        #speed projection on axes
        self.x_speed = speed*math.cos(math.radians(angle))
        self.y_speed =  - speed*math.sin(math.radians(angle))
            
        # need to round the value 
        if self.x_speed > 0:
            # to the superior int 
            self.x_speed = math.ceil(self.x_speed)
        else:
            # to the inferior int
            self.x_speed = math.floor(self.x_speed)

        if self.y_speed > 0:
            self.y_speed = math.ceil(self.y_speed)
        else:
            self.y_speed = math.floor(self.y_speed)

               
    def set_collided(self) -> int:
        """ Asteroid has collided """        
        self.kill()


    def update(self, pressed_keys):
        self.original_rect.move_ip(self.x_speed,self.y_speed)
        
        self.rotate_angle = (self.rotate_angle + self.rotation_speed) % 360
            
        self.image = pygame.transform.rotate(self.original_image, self.rotate_angle)
        #place the rotated image at the correct center
        self.rect = self.image.get_rect(center =  self.original_rect.center)

        
    def on_out_of_bound(self, width, height):
        """ when asteroid goes out from an edge of the screen
           it appears on the opposite edge  """
        rect = self.original_rect
        if rect.right < 0:
            rect.left = width - 1
            
        if rect.left > width:
            rect.right = 1
            
        if rect.top > height:
            rect.bottom= 1

        if rect.bottom < 0:
            rect.top = height - 1
