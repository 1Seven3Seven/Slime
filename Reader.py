import os
import pygame


def main():
    potential_folders = os.listdir("pictures")
    potential_folders = [folder for folder in potential_folders if os.path.isdir(f"pictures/{folder}")]

    assert len(potential_folders), "No folders found"

    padding = len(str(len(potential_folders)))
    for i, folder in enumerate(potential_folders, start=1):
        print(f"{str(i).ljust(padding)} -> {folder}")

    print()
    choice = int(input("> ")) - 1

    folder = potential_folders[choice]

    picture_names = os.listdir(f"pictures/{folder}")
    picture_names = [int(name.split('.')[0][5:]) for name in picture_names]  # Remove .png and 'Image'
    picture_names.sort()
    picture_names = [f"pictures/{folder}/Image{name}.png" for name in picture_names]  # Return to string & add directory

    img = pygame.image.load(picture_names[0])
    size = img.get_size()

    pygame.init()
    pygame.display.set_caption("Slime Replay Time")
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    index = 0

    surf = pygame.image.load(picture_names[0])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        screen.fill((0, 0, 0))

        screen.blit(surf, (0, 0))

        index += 1
        if index < len(picture_names):
            surf = pygame.image.load(picture_names[index])

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
