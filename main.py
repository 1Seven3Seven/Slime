import math

import pygame


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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        screen.blit(reduction_surface, (0, 0), special_flags=pygame.BLEND_RGB_SUB)

        for point in points:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(point.position[0], point.position[1], 1, 1))

            point.move()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
