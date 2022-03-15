from turtle import width
import pygame
from pygame import gfxdraw
import math
pygame.init()

# recommendation - width and height should be the same value and not less than 265
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
bg_img = pygame.image.load('images/space.png')
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
pygame.display.set_caption("Simulação de planetas")

colors = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'yellow_out': (255, 231, 3),
    'yellow_mid': (255, 236, 181),
    'blue': (21, 120, 196)
}


def draw_circle(x, y, radius, color):
    gfxdraw.aacircle(WIN, int(x), int(y), int(radius), color)
    gfxdraw.filled_circle(WIN, int(x), int(y), int(radius), color)


def draw_orbit(x, y, radius, color):
    gfxdraw.aacircle(WIN, int(x), int(y), int(radius), color)


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def main():
    run = True
    clock = pygame.time.Clock()

    # use the width or height depending on which is smaller, so that there is nothing outside of view
    scale_dir = min(WIDTH, HEIGHT)
    # 1 pixel is 40/(scale_dir-200) cm irl (200 is the ammount of pixels that the orbit will not use)
    scale = 80/(scale_dir-200)

    # Planet values
    planet_real_distance_to_sun = 40  # 40 cm
    planet_distance_to_sun = planet_real_distance_to_sun / scale  # 40 cm irl
    planet_x = (WIDTH/2)  # planet x coord
    planet_y = (HEIGHT/2) - planet_distance_to_sun  # planet y coord
    planet_radius = 1.5 / scale  # 1cm irl
    planet_velocity = 1  # player vel (explained below)

    angle = 0  # angle to calculate the circular motion
    getTicksLastFrame = 0  # calculate deltatime

    font = pygame.font.SysFont(None, 24)  # Text font

    while run:
        clock.tick(60)

        WIN.blit(bg_img, (0, 0))

        # Draw the sun
        sun_x, sun_y = WIDTH/2, HEIGHT/2  # middle of the window
        # convert 2.5 cm (radius of the real sun) to pixels
        radius = 5 / scale
        draw_circle(sun_x, sun_y, radius, colors['yellow_out'])
        draw_circle(sun_x, sun_y, radius-5, colors['yellow_mid'])

        draw_orbit(sun_x, sun_y, 40/scale, colors['white'])

        # Draw the planet

        planet_x = math.cos(angle) * planet_distance_to_sun + (WIDTH/2)

        planet_y = math.sin(angle) * planet_distance_to_sun + (HEIGHT/2)

        # angle made between the X axis and the planet
        real_angle = math.degrees(math.atan2(math.sin(angle), math.cos(angle)))

        if (real_angle < 0):
            real_angle = abs(180 + real_angle) + 180

        draw_circle(planet_x, planet_y,
                    planet_radius, colors['blue'])

        # Render velocity vectors
        if (real_angle < 180):
            vector_x = -100
        else:
            vector_x = 100

        if (planet_y - (HEIGHT/2) != 0):
            vector_y = -((planet_x-(WIDTH/2)))/(planet_y-(HEIGHT/2)) * vector_x
        else:
            vector_y = 0

        direction = pygame.math.Vector2(
            vector_x, vector_y)
        # divide by 2 so that the line wont get too big
        direction.scale_to_length((planet_velocity * planet_distance_to_sun)/2)

        pygame.draw.line(WIN, colors['white'],
                         (planet_x, planet_y), (planet_x + direction.x, planet_y + direction.y))

        # Render the velocity
        img = font.render(
            f'{planet_velocity*planet_real_distance_to_sun}cm/s', True, colors['white'])
        WIN.blit(img, (planet_x, planet_y+30))

        ticks = pygame.time.get_ticks()

        # deltaTime in seconds.
        deltaTime = (ticks - getTicksLastFrame) / 1000.0
        getTicksLastFrame = ticks

        # 1: T = 6.3s
        #    Ang_Vel = 1rad/s
        #    Real_Vel = 40 cm/s
        angle += planet_velocity * deltaTime

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.quit()


main()
