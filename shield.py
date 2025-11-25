import pygame
import random
from circleshape import CircleShape
from constants import SHEILD_RADIUS, SHIELD_DURATION_SECONDS, LINE_WIDTH
from logger import log_event



class ShieldPickup(CircleShape):
    def __init__(self,x,y):
        super().__init__(x, y, SHEILD_RADIUS)



    def draw(self,screen):
        pygame.draw.circle(
            screen,
            "cyan",
            self.position,
            self.radius,
            LINE_WIDTH,
        )

    def update(self,dt):
        pass
