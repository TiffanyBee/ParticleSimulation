import pygame
import math
pygame.init()

WIDTH = 800
HEIGHT = 600

particles = []
class Boid:
    def __init__(self, x, y): 
        self.mass = 1
        self.position = pygame.math.Vector2(x, y)
        self.acceleration = pygame.math.Vector2(0,0)
        self.velocity = pygame.math.Vector2(0,0)

    def applyForce(self, force):
        self.acceleration.x += force.x / self.mass
        self.acceleration.y += force.y / self.mass

    def updatePosition(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration = pygame.math.Vector2(0,0)

    def update(self):
        pass

class Flock:
    def __init__(self, flock_size):
        self.boids = []
        self.size = flock_size

    def populateFlock(self):
        for i in range(self.size):
            self.boids.append(Boid(WIDTH//2, HEIGHT//2))

            angle = (i / self.size) * 2 * 3.14159

            self.boids[i].velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * 2

    def updateFlock(self):
        for boid in self.boids:
            boid.updatePosition()

    def renderFlock(self, screen):
        for boid in self.boids:
            pygame.draw.circle(screen, (255, 255, 255), (boid.position[0], boid.position[1]), 5)

flock = Flock(10)
flock.populateFlock()
clock = pygame.time.Clock()   

run = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flocking Simulation")
while run: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           run = False

    flock.updateFlock()
    screen.fill((0, 0, 0))
    flock.renderFlock(screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()