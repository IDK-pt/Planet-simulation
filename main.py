import pygame
from pygame import gfxdraw
import math
pygame.init()

# recommendation - width and height should be the same value and not less than 265
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
bg_img = pygame.image.load('images/space.png')
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
pygame.display.set_caption("Simulação de planetas")

colors = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'yellow_out': (255, 231, 3),
    'yellow_mid': (255, 236, 181),
    'blue': (21, 120, 196),
    'green': (86, 181, 79),
    'red': (231, 35, 59)
}


def draw_circle(x, y, radius, color):
    gfxdraw.aacircle(WIN, int(x), int(y), int(radius), color)
    gfxdraw.filled_circle(WIN, int(x), int(y), int(radius), color)


def draw_orbit(x, y, radius, color):
    gfxdraw.aacircle(WIN, int(x), int(y), int(radius), color)


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
    angle1 = 0  # angle to calculate the moons circular motion
    getTicksLastFrame = 0  # calculate deltatime

    font = pygame.font.SysFont(None, 24)  # Text font

    animation_on = False

    class Button():
        def __init__(self, color, font, x, y, width, height, text):
            self.color = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text
            self.font = font

        def draw(self, win):
            pygame.draw.rect(win, self.color, (self.x, self.y,
                                               self.width, self.height), 0)
            text = self.font.render(self.text, 1, colors['white'])
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

        def update(self, win, color, text):
            self.color = color
            self.text = text

        def checkClick(self, pos):
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    return True
            return False

    # SUBTRACT THE SAME VALUES OF THE SIZE ON THE WIDTH AND HEIGHT
    btn = Button(colors['green'], font, WIDTH-110,
                 HEIGHT-60, 100, 50, 'Iniciar')

    # ----
    # FIRST, CALCULATE EVERYTHING, THEN, CHECK FOR ANIMATION STATUS AND RENDER ACCORDINGLY
    # ----

    while run:
        clock.tick(60)

        WIN.blit(bg_img, (0, 0))

        btn.draw(WIN)

        # --- Calculations and functionality ---

        # Sun calculation
        sun_x, sun_y = WIDTH/2, HEIGHT/2  # middle of the window
        # convert 2.5 cm (radius of the real sun) to pixels
        radius = 5 / scale

        # Planet coords calculation

        planet_x = math.cos(angle) * planet_distance_to_sun + (WIDTH/2)

        planet_y = math.sin(angle) * planet_distance_to_sun + (HEIGHT/2)

        # Moon experiment
        '''
        moon_x = math.cos(angle1) * 40

        moon_y = math.sin(angle1) * 40

        draw_circle(planet_x + moon_x, planet_y + moon_y,
                    4, colors['white'])
        '''

        # Calculate the angle made between the X axis and the planet
        real_angle = math.degrees(math.atan2(math.sin(angle), math.cos(angle)))

        if (real_angle < 0):
            real_angle = abs(180 + real_angle) + 180

        # Calculate velocity vector
        if (real_angle < 180):
            velocity_vector_x = -100
        else:
            velocity_vector_x = 100

        if (planet_y - (HEIGHT/2) != 0):
            velocity_vector_y = -((planet_x-(WIDTH/2))) / \
                (planet_y-(HEIGHT/2)) * velocity_vector_x
        else:
            velocity_vector_y = 0

        velocity_direction = pygame.math.Vector2(
            velocity_vector_x, velocity_vector_y)
        # divide by 2 so that the line wont get too big
        velocity_direction.scale_to_length(
            (planet_velocity * planet_distance_to_sun)/2)

        # Gravitational force calculation
        gravitation_vector_x = (WIDTH/2) - planet_x
        gravitation_vector_y = (HEIGHT/2) - planet_y

        gravitation_direction = pygame.math.Vector2(
            gravitation_vector_x, gravitation_vector_y)

        gravitation_direction.scale_to_length(WIDTH/7)

        ticks = pygame.time.get_ticks()

        # Calculate deltaTime in seconds
        deltaTime = (ticks - getTicksLastFrame) / 1000.0
        getTicksLastFrame = ticks

        # 1: T = 6.3s
        #    Ang_Vel = 1rad/s
        #    Real_Vel = 40 cm/s

        if animation_on:
            angle += planet_velocity * deltaTime

        # Moon experiment
        #angle1 += 6 * deltaTime

        # --- Render everything ---

        # Sun
        draw_circle(sun_x, sun_y, radius, colors['yellow_out'])
        draw_circle(sun_x, sun_y, radius-5, colors['yellow_mid'])

        # Planet orbit
        draw_orbit(sun_x, sun_y, 40/scale, colors['white'])

        # Planet
        draw_circle(planet_x, planet_y,
                    planet_radius, colors['blue'])

        if animation_on:
            # Velocity vector
            pygame.gfxdraw.line(WIN, int(planet_x), int(planet_y), int(planet_x +
                                velocity_direction.x), int(planet_y + velocity_direction.y), colors['white'])

            # Gravitational force vector
            pygame.gfxdraw.line(WIN, int(planet_x), int(planet_y), int(planet_x +
                                gravitation_direction.x), int(planet_y + gravitation_direction.y), colors['white'])

            # Velocity indicator
            img = font.render(
                f'{planet_velocity*planet_real_distance_to_sun}cm/s', True, colors['white'])
            WIN.blit(img, (planet_x, planet_y+30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn.checkClick(pygame.mouse.get_pos()):

                    if animation_on:
                        btn.update(WIN, colors['green'], 'Iniciar')

                        # Restart all the values
                        angle = 0
                        angle1 = 0
                    else:
                        btn.update(WIN, colors['red'], 'Recomeçar')

                    animation_on = not animation_on

        pygame.display.update()

    pygame.quit()


main()
