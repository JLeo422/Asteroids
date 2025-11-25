import pygame
import sys
import random
from constants import (
    SCREEN_HEIGHT, 
    SCREEN_WIDTH,
    SHIELD_DURATION_SECONDS,
    SHIELD_SPAWN_MIN_SECONDS,
    SHIELD_SPAWN_MAX_SECONDS,
    SHIELD_PICKUP_LIFETIME_SECONDS,
)
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from shield import ShieldPickup

def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0

    pygame.font.init()
    font = pygame.font.SysFont(None,30)
    score = 0

    

    print(f"Starting Asteroids with pygame version: {pygame.__version__}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group() #own


    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    ShieldPickup.containers = (powerups, updatable, drawable) #own

    player = Player(SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    shield_pickup = None
    shield_spawn_timer = random.uniform(
        SHIELD_SPAWN_MIN_SECONDS,
        SHIELD_SPAWN_MAX_SECONDS,
    )
    shield_pickup_timer = 0.0


    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


        updatable.update(dt)

        screen.fill("black")

        if shield_pickup is None:
            # No shield in the world: count down to the next spawn
            shield_spawn_timer -= dt
            if shield_spawn_timer <= 0:
                # Spawn a new shield at a random position
                x = random.uniform(SCREEN_WIDTH * 0.1, SCREEN_WIDTH * 0.9)
                y = random.uniform(SCREEN_HEIGHT * 0.1, SCREEN_HEIGHT * 0.9)

                shield_pickup = ShieldPickup(x, y)
                shield_pickup_timer = 0.0  # reset life timer
        else:
            # A shield is active in the world: track how long it has existed
            shield_pickup_timer += dt
            if shield_pickup_timer >= SHIELD_PICKUP_LIFETIME_SECONDS:
                # Time's up, despawn it
                shield_pickup.kill()
                shield_pickup = None
                shield_spawn_timer = random.uniform(
                    SHIELD_SPAWN_MIN_SECONDS,
                    SHIELD_SPAWN_MAX_SECONDS,
                )


        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    score += 10
                    asteroid.split()
                    shot.kill()
                    break

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                if player.shield_timer >0:
                    asteroid.split()
                else:
                    log_event("player_hit")
                    print("Game over!")
                    sys.exit()

        for powerup in list(powerups):
            if player.collides_with(powerup):
                powerup.kill()
                player.shield_timer = SHIELD_DURATION_SECONDS
                log_event("shield_pickup")
                if powerup is shield_pickup:
                    shield_pickup = None
                    shield_spawn_timer = random.uniform(
                        SHIELD_SPAWN_MIN_SECONDS,
                        SHIELD_SPAWN_MAX_SECONDS,
                    )

        for sprite in drawable:
            sprite.draw(screen)

        score_surf = font.render(f"Score: {score}",True,"white")
        screen.blit(score_surf,(10,10))

 

        pygame.display.flip()
        dt = clock.tick(60) /1000





if __name__ == "__main__":
    main()
