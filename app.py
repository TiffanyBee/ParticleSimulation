import pygame
import math
import random
import numpy as np
pygame.init()

WIDTH = 800
HEIGHT = 600

particles = []
class Boid:
    def __init__(self, x, y): 
        self.mass = 1
        self.position = np.array([float(x), float(y)])
        self.acceleration = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])
        self.speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        self.max_speed = 1.5
        self.max_force = 1

    def applyForce(self, force):
        self.acceleration[0] += force[0] / self.mass
        self.acceleration[1] += force[1] / self.mass

    def updatePosition(self):
        new_velocity = self.velocity + self.acceleration
        if np.linalg.norm(new_velocity) < self.max_speed:
            self.velocity += new_velocity
        else:
            self.velocity = (new_velocity / np.linalg.norm(new_velocity)) * self.max_speed

        
        new_position = self.position + self.velocity
        if new_position[0] < 0:
            new_position[0] = WIDTH
        elif new_position[0] > WIDTH:
            new_position[0] = 0
        if new_position[1] < 0:
            new_position[1] = HEIGHT
        elif new_position[1] > HEIGHT:
            new_position[1] = 0

        self.position = new_position
        self.acceleration = np.array([0.0, 0.0])

    def seperation(self, seperation_radius, boids):
        seperation_vector = np.array([0.0, 0.0])
        for boid in boids:
            if boid != self:
                distance = math.hypot(self.position[0] - boid.position[0], self.position[1] - boid.position[1])
                if distance < seperation_radius:
                    diff = self.position - boid.position
                    seperation_vector += (diff) / ((diff[0])**2 + (diff[1]**2)) if ((diff[0])**2 + (diff[1]**2)) > 0 else np.array([.1, .1])

        return seperation_vector

    def alignment(self, alignment_radius, boids):
        alignment_vector = np.array([0.0, 0.0])
        count = 0
        for boid in boids:
            if boid != self:
                distance = math.hypot(self.position[0] - boid.position[0], self.position[1] - boid.position[1])
                if distance < alignment_radius:
                    alignment_vector += boid.velocity
                    count += 1

        alignment_vector = (1/count) * alignment_vector if count > 0 else alignment_vector
        return alignment_vector
        # remember to calculate steer alignment

    def cohesion(self, cohesion_radius, boids):
        cohesion_vector = np.array([0.0, 0.0])
        count = 0
        for boid in boids:
            if boid != self:
                distance = math.hypot(self.position[0] - boid.position[0], self.position[1] - boid.position[1])
                if distance < cohesion_radius:
                    cohesion_vector += boid.position
                    count += 1
        cohesion_vector = (1/count) * cohesion_vector if count > 0 else cohesion_vector
        return cohesion_vector
            # remember to calculate steer cohesion

    def steeringForce(self, seperation_radius, alignment_radius, cohesion_radius, weights,boids):
        seperation_vector = self.seperation(seperation_radius, boids)
        alignment_vector = self.alignment(alignment_radius, boids)
        cohesion_vector = self.cohesion(cohesion_radius, boids)

        steer_alignment = alignment_vector - self.velocity
        steer_cohesion = cohesion_vector - self.position

        # Calculate the steering force based on the three behaviors
        steering_force = weights[0] *seperation_vector + weights[1] *steer_alignment + weights[2] * steer_cohesion
        if np.linalg.norm(steering_force) > self.max_force:
            steering_force = (steering_force / np.linalg.norm(steering_force)) * self.max_force
        return steering_force
        



class Flock:
    def __init__(self, flock_size):
        self.boids = []
        self.size = flock_size

    def populateFlock(self):
        for i in range(self.size):
            self.boids.append(Boid(random.random() * WIDTH, random.random() * HEIGHT))

            angle = (i / self.size) * 2 * 3.14159

            self.boids[i].velocity = np.array([math.cos(angle), math.sin(angle)]) * 2

    def updateFlock(self):
        for boid in self.boids:
            steering_force = boid.steeringForce(70, 50, 100, [1.0, 1.0, 3.0], self.boids)
            boid.applyForce(steering_force)
            boid.updatePosition()

    def renderFlock(self, screen):
        for boid in self.boids:
            pygame.draw.circle(screen, (255, 255, 255), (boid.position[0], boid.position[1]), 5)

flock = Flock(200)
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
    clock.tick(30)

pygame.quit()