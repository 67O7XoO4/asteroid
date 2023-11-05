import os
import pygame
from pygame.locals import *
import math

from AssetLoader import AssetLoader

ROTATION_SPEED      = 5     # angle in degree
SPEEDUP             = 0.3   # how much the ship speedup
MAX_SPEED           = 8     # max speed
NATURAL_SLOWDOWN    = 0.995  # how much the ship slowdown 


class Player(pygame.sprite.Sprite):
    """ Sprite of the player. Actually a space ship """
    
    def __init__(self, loader : AssetLoader, position):
        """
        Args:
            loader (AssetLoader): AssetLoader instance
            position : (x,y) coordinate. start position of the ship in the screen
        """
        super().__init__() 
        
        self.asset_loader = loader
        # has the player been collided ?
        self.collided = False
        # in state of grace, the spaceship cannot be collided        
        self.state_of_grace = True
        # just to make it blink while in state of grace
        self.state_of_grace_alpha = False
        
        self.imageNoEngine = loader.loadImage(64*3, 160+96, 96, 64, 0.75)
        self.imageWithEngine = loader.loadImage(64*3+96, 160+96, 96, 64, 0.75)
        # the original non rotated image (can be With Engine or without engine)
        self.original_image = self.imageNoEngine;
        # the currently displayed image (that can be rotated)
        self.image = self.original_image
        
        self.rect = self.image.get_rect()
        self.original_rect = self.rect;
        
        self.start_position = position 
        self.reset_to_start_position()
        
            
    def reset_to_start_position(self):
        """ set the spaceship at its start position in an initial state """
        self.image = self.imageNoEngine
        self.rect.center = self.start_position
        self.original_rect = self.rect;
        self.x_speed = 0
        self.y_speed = 0
        self.angle = 90 # rotation angle of the sprite
        self.collided = False
        self.state_of_grace = True


    def set_collided(self):
        self.collided = True
        self.kill()
        
    def get_missile_position(self):
        return self.rect.center

 
    def update(self, pressed_keys):
        """ask the sprite to update itself according to its state and to the currently pressed keys
        Args:
            pressed_keys : currently pressed keys
        """
        
        if self.collided:
            return
        
        # left / right keys: rotate the ship
        if pressed_keys[K_LEFT]:
            self.angle+= ROTATION_SPEED
        if pressed_keys[K_RIGHT]:
            self.angle-= ROTATION_SPEED
        # modulo
        self.angle = self.angle % 360
        
        self.original_image = self.imageNoEngine
        
        # up keys: accelerate  
        if pressed_keys[K_UP] and self.x_speed<MAX_SPEED and self.y_speed<MAX_SPEED:
            #  use alternate image with a "flame" behind the ship to simulate speed up
            self.original_image = self.imageWithEngine 
            self.asset_loader.playSound('thrust')
            
            # speed projection on axes
            self.x_speed += SPEEDUP*math.cos(math.radians(self.angle))
            self.y_speed -=  SPEEDUP*math.sin(math.radians(self.angle))
        
        if not pressed_keys[K_UP]:
            # no key pressed : natural slown down 
            self.x_speed = self.x_speed * NATURAL_SLOWDOWN
            self.y_speed = self.y_speed * NATURAL_SLOWDOWN
                
        # move sprite
        self.original_rect.move_ip(self.x_speed,self.y_speed)
        #image rotation
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        #place the rotated image at the correct center
        self.rect = self.image.get_rect(center =  self.original_rect.center)
        # "no collision" state
        if self.state_of_grace:
            if self.state_of_grace_alpha:
                self.image.set_alpha(125)
            else:
                self.image.set_alpha(200)


    def make_it_blink(self):
            self.state_of_grace_alpha = not self.state_of_grace_alpha         
        
    def on_out_of_bound(self, width, height):
        """ when spaceship goes out from an edge of the screen
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
            

        
