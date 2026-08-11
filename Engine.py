import random
import pygame
import sys



scale = 10

class Particle:
    def __init__(self, x, y, vx, vy, ax, ay, radius, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.radius = radius
        self.color = color

    def update(self, dt):
        self.vx = self.vx + (self.ax)*dt
        self.x = self.x + (self.vx)*dt
        self.vy = self.vy +(self.ay)*dt
        self.y = self.y + (self.vy)*dt

    def check_bounds(self, width, height):
        floor_y = height / scale
        wall_x = width / scale

        if self.y >= floor_y -self.radius:
            self.y = floor_y - self.radius
            self.vy = -self.vy

        if self.x >= wall_x - self.radius:
            self.x = wall_x - self.radius
            self.vx = -self.vx

        if self.y <= self.radius:
            self.y = self.radius
            self.vy = -self.vy

        if self.x <= self.radius:
            self.x = self.radius
            self.vx = -self.vx

    def collison(self, other):
        ...
            
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int((self.x)*scale), int((self.y)*scale)), (self.radius)*scale)







P1 = Particle(x = 0, y = 0, vx = 10, vy = 0, ax = 0, ay = 9.8, radius = 0.5, color = (255, 0, 0))
P2 = Particle(x = 100, y = 0, vx = 10, vy = 0, ax = 0, ay = 9.8, radius = 0.5, color = (0, 0, 255))

particles = [P1, P2]




pygame.init()

WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Sim")
clock = pygame.time.Clock()

running = True
while running:
    # 1. handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    dt = clock.tick(60) / 1000.0
    

    # 2. update physics  
    for p in particles:
        p.update(dt)
        p.check_bounds(WIDTH, HEIGHT)
    #P1.update(dt)
    #P2.update(dt)
    #P1.check_bounds(WIDTH, HEIGHT)
    #P2.check_bounds(WIDTH, HEIGHT)
    # 3. draw
    screen.fill((20, 20, 30))
    for p in particles:
        p.draw(screen)
    #P1.draw(screen)
    #P2.draw(screen)
    pygame.display.flip()

    # 4. cap frame rate
    #dt = clock.tick(60) / 1000.0  # dt in seconds, capped at 60fps

pygame.quit()