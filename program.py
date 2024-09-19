import pygame
import math
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0,0,0)
BLUE = (176,224,230)

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


"""
magnetic field strength = B
electric field strength = E
initial gyrophase = theta_0
drift velocity = U
"""

E = 50
B = 10
theta_0 = 0


pygame.display.set_caption("Ion Trajectory")

class Ion:
    def __init__(self, x, y, charge, mass, time, color):
        self.x = x
        self.y = y
        self.charge = charge
        self.mass = mass
        self.time = time
        self.color = color

    def draw(self, WIN):
        points = self.trajectory()
        pygame.draw.lines(WIN, self.color, False, points, 2)



    def trajectory(self):
        self.motion = []
        self.t = 0

        dt = 0.01

        angular_position = self.charge * B / self.mass

        U = E * B / B**2
        gyroradius = (self.mass * U) / self.charge * E

        while self.t < self.time:
            x = gyroradius * ((angular_position * self.t + theta_0) - math.sin(angular_position * self.t + theta_0))
            y = gyroradius * (1 - math.cos(angular_position * self.t + theta_0))

            x += WIDTH//2
            y += HEIGHT//2

            self.motion.append((x, y))

            self.t += dt


        
        return self.motion


def main():
    run = True
    clock = pygame.time.Clock()

    hydrogen  = Ion(0, 0, +6, 1, 5, BLACK)
    helium = Ion(0, 0, +2, +2, 5, BLUE)

    ions = [hydrogen, helium]

    while run:
        clock.tick(60)
        WIN.fill(WHITE)
        pygame.display.update()    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        for ion in ions:
            ion.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()