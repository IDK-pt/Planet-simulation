import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação de planetas")

colors = {
    'black': (0, 0, 0),
    'white': (255, 255, 255)
}


class Planet():

    def __init__(self, mass, radius, orbit, start_velocity, color):
        self.x = WIDTH/2
        self.y = (HEIGHT/2) + orbit


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        WIN.fill(colors['black'])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


main()
