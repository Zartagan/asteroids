import pygame, random
from circleshape import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self):
        # Clear the previous image
        self.image.fill((0,0,0,0))  # Clear with transparent color
        # Draw the triangle on self.image instead of the screen
        pygame.draw.circle(self.image, "white", (self.radius, self.radius), self.radius, 2)
    
    def update(self, dt):
        self.position += (self.velocity * dt)
        self.rect.center = self.position  # Add this line
        self.draw()
    
    
    def split(self):
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.kill()
        else:
            random_angle = random.uniform(20, 50)
            vector_1 = self.velocity.rotate(random_angle)
            vector_2 = self.velocity.rotate(-random_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            
            new_asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_1.velocity = vector_1 * 1.2  # Set and scale velocity
            
            new_asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_2.velocity = vector_2 * 1.2  # Set and scale velocity
            
            self.kill()