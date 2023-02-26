import math
import os
from datetime import datetime

import pygame

DIFFUSE_SPEED = 0.5


class Point:
    def __init__(self, position: list[float, float], direction: float, playground_size: tuple[int, int]):
        """
        :param position: The starting position of the point.
        :param direction: The direction, in radians, to initially move in.
        :param playground_size: The size of the area in which the point moves.
        """

        self.position: list[float, float] = position
        self.direction: float = direction

        self.vector = [math.cos(direction), -math.sin(direction)]

        self.playground_size: tuple[int, int] = playground_size

    def move(self):
        """
Moves the point in the direction of its vector.
Bounces off the edges of the playground.
        """

        self.position[0] += self.vector[0]
        if self.position[0] < 0:
            self.position[0] = 0
            self.vector[0] = -self.vector[0]
        elif self.position[0] > self.playground_size[0]:
            self.position[0] = self.playground_size[0]
            self.vector[0] = -self.vector[0]

        self.position[1] += self.vector[1]
        if self.position[1] < 0:
            self.position[1] = 0
            self.vector[1] = -self.vector[1]
        elif self.position[1] > self.playground_size[1]:
            self.position[1] = self.playground_size[1]
            self.vector[1] = -self.vector[1]


def lerp(a, b, c):
    return (c * a) + ((1 - c) * b)


def get_current_date_time_as_str() -> str:
    """
Simply gets the current date and time and returns it in a nice format '%Y-%m-%d %H;%M;%S'.
    :return: The date and time as a string.
    """

    return datetime.now().strftime("%Y.%m.%d %H;%M;%S")


def create_directory(path: str) -> str:
    """
Small function to create a directory if it doesn't exist.
    :param path: The directory to create.
    :return: The directory created, identical to path.
    """

    if not os.path.exists(path):
        os.makedirs(path)
    return path


def blur_pixel(x: int, y: int, surface_pix_arr: pygame.PixelArray, surface_pix_arr_copy: pygame.PixelArray):
    """
Blurs the given pixel by taking the average of each pixel in a 3x3 grid centered on it.
    :param x: The x coord of the pixel to be blurred.
    :param y: The y coord of the pixel to be blurred.
    :param surface_pix_arr: The pixel array of the surface to be blurred.
    :param surface_pix_arr_copy: The pixel array of the surface to be blurred before blurring occurs as to prevent using
    already blured pixels.
    """

    colour_sum = [0, 0, 0]  # The sum of all RGB values of each pixel around the one we are handling

    for x_offset in range(-1, 2):
        for y_offset in range(-1, 2):

            a = x + x_offset
            b = y + y_offset

            if a < 0:
                a = 0
            elif a > surface_pix_arr.shape[0] - 1:
                a = surface_pix_arr.shape[0] - 1

            if b < 0:
                b = 0
            elif b > surface_pix_arr.shape[1] - 1:
                b = surface_pix_arr.shape[1] - 1

            colour_at_ab = pygame.Color(surface_pix_arr_copy[a, b])[1:4]  # Remove alpha

            colour_sum = [a + b for a, b in zip(colour_sum, colour_at_ab)]

    original_colour = pygame.Color(surface_pix_arr_copy[x, y])[1:4]
    colour_average = [int(a / 9) for a in colour_sum]

    diffused_colour = [lerp(original_colour[a], colour_average[a], DIFFUSE_SPEED) for a in range(3)]

    surface_pix_arr[x, y] = pygame.Color(diffused_colour)


def blur_surface(surface: pygame.Surface):
    """
Blurs the given surface.
    :param surface: Surface to be blurred
    """

    surface_pix_arr = pygame.PixelArray(surface)
    surface_pix_arr_copy = pygame.PixelArray(surface.copy())

    x_size, y_size = surface_pix_arr.shape

    for x in range(x_size):
        for y in range(y_size):
            blur_pixel(x, y, surface_pix_arr, surface_pix_arr_copy)

    surface_pix_arr.close()


def main():
    pygame.init()
    pygame.display.set_caption("Slime Time")
    window_size = (500, 500)
    screen = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()

    reduction_surface = pygame.Surface(window_size)
    reduction_surface.fill((1, 1, 1))

    points: list[Point] = []
    for r in range(1000):
        points.append(
            Point([250, 250], 2 * math.pi * r / 1000, window_size)
        )

    folder = f"pictures/{get_current_date_time_as_str()}"
    create_directory(folder)

    counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        counter += 1

        screen.blit(reduction_surface, (0, 0), special_flags=pygame.BLEND_RGB_SUB)

        blur_surface(screen)

        for point in points:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(point.position[0], point.position[1], 1, 1))

            point.move()

        pygame.display.flip()

        pygame.image.save(screen, f"{folder}/Image{counter}.png")

        clock.tick(60)


if __name__ == "__main__":
    main()
