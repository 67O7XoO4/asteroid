import logging
import math
import os
import random
import pygame
from pygame.locals import *

from Asteroid import Asteroid
from ExplosionItem import ExplosionItem
from BigMessage import BigMessage
from AssetLoader import AssetLoader
from Level import Level
from Life import Life
from Missile import Missile
from Player import Player
from Saucer import Saucer
from Score import Score

# USER Event : a new asteroid arises
NEW_ASTEROID_EVENT                  = USEREVENT+1
LIVE_LOST_EVENT                     = USEREVENT+2
END_OF_STATE_OF_GRACE_EVENT         = USEREVENT+3
END_OF_STATE_OF_GRACE_ALPHA_EVENT   = USEREVENT+4
NEW_FLYING_SAUCER_EVENT             = USEREVENT+5
NEW_FLYING_SAUCER_SHOT_EVENT        = USEREVENT+6

SCREEN_WIDTH    = 1024
SCREEN_HEIGHT   = 800
FPS             = 50
 
class App:
    """ App running the main loop of the game, managing events, updates and redraw of the screen """
    
    def __init__(self):
        self._running = True # is the app running ?
        self._screen = None
        # Screen information
        self.size = self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init() # enable sounds
        pygame.init()
        pygame.display.set_caption("Asteroid")
        # not clear : https://stackoverflow.com/questions/29135147/what-do-hwsurface-and-doublebuf-do
        self._screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.background = pygame.image.load(os.path.join("assets","background.jpeg")).convert()
        self.background = pygame.transform.scale(self.background, self.size)
        self._screen.blit(self.background, (0,0))


    def execute(self):
        """ To be called to start the game 
            main loop:
                - init
                - while running
                    - manage events
                    - update
                    - render (redraw)
                cleanup before exit
        """
        
        self.init()
        
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.update()
            self.render()
            self.fps.tick(FPS)
            
        self.cleanup()
 
         
         
    def init(self):
        """ initialize the game: the screen, the clock, the sprites """
        
        self._running = True
        self._game_over = False
        
        self.fps = pygame.time.Clock()

        # all sprites of the game must be in this group
        self.sprites = pygame.sprite.Group()
        # game level
        self.level = Level(pygame)
        self.sprites.add(self.level)
        # score
        self.score = Score(pygame, self.width/2)
        self.sprites.add(self.score)

        self.asset_loader = AssetLoader(pygame)

        self.player = Player(self.asset_loader, (self.width/2, self.height/2))
        self.sprites.add(self.player)
        pygame.time.set_timer(END_OF_STATE_OF_GRACE_EVENT, 3000, 1)

        # 3 remainig lives
        self.remaining_lives = pygame.sprite.Group()
        for x in range(1,4):
            life = Life(self.asset_loader, self.width - 40*x)
            self.sprites.add(life)
            self.remaining_lives.add(life)
            
        # missiles from the player (not from saucer) 
        self.missiles  = pygame.sprite.Group()
        # all others group: asteroids, saucer and saucer's missile
        self.ennemies  = pygame.sprite.Group()   

        self.flying_saucer = None
        
        
        
    def cleanup(self):
        pygame.quit()
 
 
    def on_event(self, event):
        """ deals with events in a game """
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not self.player.collided:
                # missile shot
                missile = Missile(self.asset_loader, self.player.get_missile_position(), self.player.angle)
                self.sprites.add(missile)
                self.missiles.add(missile)
            if self._game_over :
                # start a next Game
                self.init()
                self.sprites.add(BigMessage(pygame,"Go go go !!", (self.width/2, self.height/2), True))
                
        if event.type == END_OF_STATE_OF_GRACE_EVENT:
            self.player.state_of_grace = False

        if event.type == NEW_FLYING_SAUCER_SHOT_EVENT:
            if self.flying_saucer is not None:
                # missile shot
                (x1, y1) = self.flying_saucer.rect.center
                (x2, y2) = self.player.rect.center
                angle = math.degrees(math.atan2((y1 - y2), (x2 - x1) ))
                diff= 80 - self.level.num*5
                missile = Missile(self.asset_loader, (x1, y1), angle + random.randrange(-diff, +diff))
                self.sprites.add(missile)
                self.ennemies.add(missile)
                #next shot
                pygame.time.set_timer(NEW_FLYING_SAUCER_SHOT_EVENT,  random.randrange(250, 3000 - self.level.num*100), 1)

            
        if event.type == NEW_ASTEROID_EVENT:
            # new asteroid arise 
            self.create_asteroid()
              
        if (event.type == NEW_FLYING_SAUCER_EVENT):
            # new saucer arise 
            self.create_flying_saucer()
            
        if event.type == LIVE_LOST_EVENT:
            if len(self.remaining_lives)==0: 
                # GAME OVER
                self.sprites.add(BigMessage(pygame,"Game Over !!", (self.width/2, self.height/2)))
                self._game_over = True
            else:
                # restore the player at the center of the screen
                self.player.reset_to_start_position()
                self.sprites.add(self.player)
                pygame.time.set_timer(END_OF_STATE_OF_GRACE_ALPHA_EVENT, 100, 30)
                pygame.time.set_timer(END_OF_STATE_OF_GRACE_EVENT, 3000, 1)

            
        if event.type == END_OF_STATE_OF_GRACE_ALPHA_EVENT:
            # new asteroid arise 
            self.player.make_it_blink()

        if event.type == pygame.QUIT:
            # screen is closed => end of the game
            self._running = False


    def create_asteroid(self, parent_asteroid=None):
        asteroid = Asteroid(self.asset_loader, parent_asteroid = parent_asteroid, screen_size=self.size)
        self.sprites.add(asteroid)  
        self.ennemies.add(asteroid)

    def create_flying_saucer(self):
        self.flying_saucer = Saucer(self.asset_loader, self.size, self.on_flying_saucer_killed)
        self.sprites.add(self.flying_saucer)  
        self.ennemies.add(self.flying_saucer)
        #start shooting
        pygame.time.set_timer(NEW_FLYING_SAUCER_SHOT_EVENT,  random.randrange(250, 2500), 1)


    def on_flying_saucer_killed(self):
        self.flying_saucer = None
        pygame.time.set_timer(NEW_FLYING_SAUCER_SHOT_EVENT, 0) # stop shooting
        
        
    def add_explosion(self, center, big_one=False):
        if big_one:
            step =  2
            self.asset_loader.playSound('bangLarge')
        else:
            step = 10
            self.asset_loader.playSound('bangSmall')
        
        for x in range(0, 360, step):
            self.sprites.add(ExplosionItem(self.asset_loader,center, x, big_one))          
            
    
    def update(self):
        """ check collisions, update status of all items of the game 
            update game status
        """
        
        # check missiles and ennemies collisions
        collided = pygame.sprite.groupcollide(self.missiles, self.ennemies, True, False,
                                   collided=pygame.sprite.collide_rect_ratio(.5))
        
        for collided_missiles, collideds in collided.items():
            for collided in collideds:
                # explosion animation
                self.add_explosion(collided.rect.center)

                value = collided.set_collided()
                # increment user score with the value of the collided item
                self.score.increment(value) 

                if isinstance(collided, Asteroid) and collided.type < Asteroid.MAX_TYPE:
                    # create 2 smaller asteroids 
                    self.create_asteroid(collided)
                    self.create_asteroid(collided)
        
        if not self.player.collided and not self.player.state_of_grace:
            # check player and asteroid collisions
            collided = pygame.sprite.spritecollide(self.player, self.ennemies, True, 
                                    collided=pygame.sprite.collide_rect_ratio(.5))
            if len(collided) > 0 :

                # the callback is not called : calling it now
                if self.flying_saucer in collided:
                    self.on_flying_saucer_killed()

                # display a big explosion animation 
                self.add_explosion(self.player.rect.center, True)
                self.add_explosion(self.player.rect.center, False)
                # set player as collided
                self.player.set_collided()
                                    
                # remove one live if any
                if len(self.remaining_lives)>0:
                    remaining_live = self.remaining_lives.sprites()[0]
                    remaining_live.kill()
                    self.add_explosion(remaining_live.rect.center, False)
                
                # wait before restart the game
                pygame.time.set_timer(LIVE_LOST_EVENT, 2000, 1)
            
        # call each sprite to update itself
        self.sprites.update(pygame.key.get_pressed())
        
        # check for sprites out of screen
        for sprite in self.sprites:
            if self.is_out_of_bound(sprite):
                sprite.on_out_of_bound(self.width, self.height)

        # next level ?
        if len(self.ennemies) == 0:
            self.level.next()
            # create first asteroid
            self.create_asteroid()      
            # next asteroids will be created by random events.
            # frequency : trigger every 0 - 1 seconds
            pygame.time.set_timer(NEW_ASTEROID_EVENT, random.randrange(0, 1000), 1+self.level.num*2)
            if (self.level.num>1): # no saucer in the first level
                # a flying saucer will appear within 10 secs
                pygame.time.set_timer(NEW_FLYING_SAUCER_EVENT, random.randrange(0, 10000), 1)
            # if not self.flying_saucer:
            #     pygame.time.set_timer(NEW_FLYING_SAUCER_EVENT, random.randrange(0, 1000), 1)
            

    
    def render(self):
        """ redraw all items and display the scene """
        self._screen.blit(self.background, (0,0))
        self.sprites.draw(self._screen)
        pygame.display.update()
        
        
    def is_out_of_bound(self, sprite):
        """ return True if the sprite is outside of the screen """
        return not sprite.rect.colliderect(self._screen.get_rect());
    