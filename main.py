import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *


def main():

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = .03

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (updatable, drawable, shots)

    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    AsteroidField()



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
    
        # player.update(dt)
        updatable.update(dt)

        shot = player.update(dt)
        if shot:  # if a shot was created
            shots.add(shot)

        screen.fill("black")
        # player.draw(screen)
        drawable.draw(screen)

        for asteroid in asteroids:
            if CircleShape.check_collision(player, asteroid) == False:
                print("Game Over")
                pygame.QUIT()

        for asteroid in asteroids:
            for shot in shots:
                if CircleShape.check_collision(shot, asteroid) == False:
                    asteroid.split()

        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()