import os
import pygame
from pygame.locals import *
import math

class AssetLoader():
    """ Utility class to load specific sprite image from a sprite collection image  """
    def __init__(self, pygame):
        """
        Args:
            pygame (_type_): pygame instance
        """
        self.sprite_images = pygame.image.load(os.path.join("assets","asteroids-2x.png")).convert_alpha()
        self.pygame = pygame
        

        
    def loadImage(self,x,y, width, height, ratio=None) -> pygame.Surface :
        """extract the image at the given coordinate
        Args:
            x (_type_): coordinate
            y (_type_): coordinate
            width (_type_): size of the extracted image
            height (_type_): size of the extracted image
            ratio (_type_, optional): apply a scale ratio if any. Defaults to None.

        Returns:
            pygame.Surface: the extracted image
        """
        image = self.sprite_images.subsurface(x,y,width,height)
        if ratio:
            rect = image.get_rect()
            image = pygame.transform.scale(image, 
                                        (rect.width * ratio, 
                                         rect.height * ratio) )
        return image

    def playSound(self, soundName):
        sound = pygame.mixer.Sound(os.path.join('assets', soundName+'.wav'))
        pygame.mixer.Sound.play(sound)
