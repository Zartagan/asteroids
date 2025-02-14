import pygame
from circleshape import CircleShape
from constants import *


class Player(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # Initialize the sprite
        CircleShape.__init__(self, x, y, PLAYER_RADIUS)
        
        # Create a surface for the triangle
        self.image = pygame.Surface((PLAYER_RADIUS * 2, PLAYER_RADIUS * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rotation = 0
        self.shot_timer = 0

    def triangle(self):
        # Calculate relative to center of our surface
        center = pygame.Vector2(self.radius, self.radius)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = center + forward * self.radius
        b = center - forward * self.radius - right
        c = center - forward * self.radius + right
        return [a, b, c]
    
    def draw(self):
        # Clear the previous image
        self.image.fill((0,0,0,0))  # Clear with transparent color
        # Draw the triangle on self.image instead of the screen
        pygame.draw.polygon(self.image, "white", self.triangle(), 2)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        # Update the rect position to match the new position
        self.rect.center = self.position

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:  # Add this!
            self.shoot()
        
        self.draw()

        self.shot_timer -= dt

    
    def shoot(self):
        if self.shot_timer <= 0.0:
            shot = Shot(self.position.x, self.position.y)
            direction = pygame.Vector2(0, 1).rotate(self.rotation)
            shot.velocity = direction * PLAYER_SHOOT_SPEED
            self.shot_timer = PLAYER_SHOOT_COOLDOWN
            return shot
        
    
class Shot(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        CircleShape.__init__(self, x, y, SHOT_RADIUS)
        
        self.image = pygame.Surface((SHOT_RADIUS * 2, SHOT_RADIUS * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = pygame.Vector2(0, 0)  # Will be set by player's shoot method

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position
        self.draw()

    def draw(self):
        # Clear the previous image
        self.image.fill((0,0,0,0))  # Clear with transparent color
        # Draw the triangle on self.image instead of the screen
        pygame.draw.circle(self.image, "white", (self.radius, self.radius), self.radius, 2)