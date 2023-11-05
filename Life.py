import pygame
from pygame.locals import *

from AssetLoader import AssetLoader


class Life(pygame.sprite.Sprite):
    """ Remaining life of the player """
    def __init__(self, loader : AssetLoader, x):
        """
        Args:
            loader (ImageLoader): ImageLoader instance
        """
        super().__init__() 
        self.image = loader.loadImage(64*3, 160+96, 96, 64, 0.5)
        self.image = pygame.transform.rotate(self.image, 90)

        self.rect = self.image.get_rect()
        self.rect.center = (x, 24)
                
        
    def update(self, pressed_keys):
        pass

    def on_out_of_bound(self, width, height):
        pass