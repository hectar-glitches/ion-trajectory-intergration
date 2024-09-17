import pygame
import math
pygame.init()

WHITE = (255, 255, 255)
BLUE = (176,224,230)

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


pygame.display.set_caption("Ion Trajectory")

class Ion:
    def __init__(self, x, y, init_velocity, charge, mass, time, color):
        self.x = x
        self.y = y
        self.init_velocity = init_velocity
        self.charge = charge
        self.mass = mass
        self.time = time
        self.color = color
        self.motion = []

    def draw(self, win):
        pygame.draw.arc(win, self.color, (WIDTH/2 - radius, HEIGHT/2 - radius, 2*radius, 2*radius), 0, math.radians(90), 2)



    def trajectory(self):
        """
        magnetic field strength = B
        electric field strength = E
        initial gyrophase = theta_0
        drift velocity = U
        """
        E = 50
        B = 10
        theta_0 = 0
        time = 0

        angular_position = self.charge * B / self.mass

        U = E * B / B**2
        gyroradius = (self.mass * U) / self.charge * E

        motion = []

        while time != self.time:
            self.x = gyroradius * ((angular_position * time + theta_0) - math.sin(angular_position * time + theta_0))
            self.y = gyroradius * (1 - math.cos(angular_position * time + theta_0))
            time += 1

            motion.append((self.x, self.y))





def main():
    run = True
    clock = pygame.time.Clock()

    hydrogen  = Ion(0, 0, 10, +1, 1, 5, WHITE)
    helium = Ion(0, 0, 5, +2, +2, 5, BLUE)

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

    pygame.QUIT()

main()