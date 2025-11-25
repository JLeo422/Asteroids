import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event



class Asteroid(CircleShape):
    def __init__(self,x,y, radius):
        super().__init__(x, y, radius)




    def draw(self,screen):
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH,
        )


    def update(self,dt):
        self.position += self.velocity * dt

    def split(self):
        #saving the states
        old_radius = self.radius
        old_velocity = self.velocity
        #destorying asteroid
        self.kill()
        
        #check if the smallest
        if old_radius <= ASTEROID_MIN_RADIUS:
            return

        
        log_event("asteroid_split")

        angle = random.uniform(20,50)

        v1 = old_velocity.rotate(angle)
        v2 = old_velocity.rotate(-angle)

        new_radius = old_radius - ASTEROID_MIN_RADIUS


        a1 = Asteroid(self.position.x,self.position.y,new_radius)
        a1.velocity = v1 * 1.2

        a2 = Asteroid(self.position.x,self.position.y,new_radius)
        a2.velocity = v2 * 1.2





