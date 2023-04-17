import pygame
import sys
import colorsys
import os

images_dir = "images"
if not os.path.exists(images_dir):
    os.makedirs(images_dir)


WIDTH = 800
HEIGHT = 600
GRID_SIZE = 16
GRID_COLOR = (200, 200, 200)
BACKGROUND_COLOR = (245, 245, 245)
COLOR_PALETTE_POS = (10, HEIGHT - 280)
COLOR_PALETTE_SIZE = 15
COLOR_PALETTE_GRID_SIZE = 16
PALETTE_CONTAINER_PADDING = 5
selected_color_index = 0
CLEAR_BUTTON_POS = (10, HEIGHT - 50)
CLEAR_BUTTON_SIZE = (80, 30)
CLEAR_BUTTON_COLOR = (50, 50, 200)
CLEAR_BUTTON_TEXT_COLOR = (255, 255, 255)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


grid = []
for x in range(0, WIDTH, GRID_SIZE):
    grid.append([])
    for y in range(0, HEIGHT, GRID_SIZE):
        color = BACKGROUND_COLOR if (x // GRID_SIZE % 2 == 0) ^ (y // GRID_SIZE % 2 == 0) else (200, 200, 200)
        grid[-1].append(color)

color_palette = []
for i in range(256):
    hue = i / 256
    saturation = (i % 16) / 15
    value = 1 - (i // 16) / 15
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
    color_palette.append((r, g, b))

def draw_grid():
    for x, col in enumerate(grid):
        for y, color in enumerate(col):
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

def draw_color_palette():
    container_x = COLOR_PALETTE_POS[0] - PALETTE_CONTAINER_PADDING
    container_y = COLOR_PALETTE_POS[1] - PALETTE_CONTAINER_PADDING
    container_width = COLOR_PALETTE_GRID_SIZE * (COLOR_PALETTE_SIZE + 1) + PALETTE_CONTAINER_PADDING * 2
    container_height = COLOR_PALETTE_GRID_SIZE * (COLOR_PALETTE_SIZE + 1) + PALETTE_CONTAINER_PADDING * 2
    container_color = (100, 100, 100)
    pygame.draw.rect(screen, container_color, (container_x, container_y, container_width, container_height), 0)

    for i, color in enumerate(color_palette):
        x = i % COLOR_PALETTE_GRID_SIZE
        y = i // COLOR_PALETTE_GRID_SIZE
        pygame.draw.rect(screen, color, (COLOR_PALETTE_POS[0] + x * (COLOR_PALETTE_SIZE + 1), COLOR_PALETTE_POS[1] + y * (COLOR_PALETTE_SIZE + 1), COLOR_PALETTE_SIZE, COLOR_PALETTE_SIZE), 0)

def draw_clear_button():
    pygame.draw.rect(screen, CLEAR_BUTTON_COLOR, (*CLEAR_BUTTON_POS, *CLEAR_BUTTON_SIZE), 0)
    font = pygame.font.Font(None, 24)
    label = font.render("Clear", True, CLEAR_BUTTON_TEXT_COLOR)
    screen.blit(label, (CLEAR_BUTTON_POS[0] + 20, CLEAR_BUTTON_POS[1] + 5))

def save_image():
    min_x, min_y, max_x, max_y = WIDTH, HEIGHT, 0, 0

    for x, col in enumerate(grid):
        for y, color in enumerate(col):
            if color != BACKGROUND_COLOR and color != (200, 200, 200):
                min_x = min(min_x, x * GRID_SIZE)
                min_y = min(min_y, y * GRID_SIZE)
                max_x = max(max_x, (x + 1) * GRID_SIZE)
                max_y = max(max_y, (y + 1) * GRID_SIZE)


    if min_x == WIDTH and min_y == HEIGHT and max_x == 0 and max_y == 0:
        return

    cropped_width = max_x - min_x
    cropped_height = max_y - min_y
    surface = pygame.Surface((cropped_width, cropped_height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))  

    for x, col in enumerate(grid):
        for y, color in enumerate(col):
            if color != BACKGROUND_COLOR and color != (200, 200, 200):
                pygame.draw.rect(surface, color, ((x * GRID_SIZE) - min_x, (y * GRID_SIZE) - min_y, GRID_SIZE, GRID_SIZE), 0)

    filename = f"image_{len(os.listdir(images_dir))}.png"
    filepath = os.path.join(images_dir, filename)
    pygame.image.save(surface, filepath)

def main():
    drawing = False
    color = (0, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_image()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()

                    if (COLOR_PALETTE_POS[1] <= y <= COLOR_PALETTE_POS[1] + COLOR_PALETTE_GRID_SIZE * (COLOR_PALETTE_SIZE + 1)) and (COLOR_PALETTE_POS[0] <= x <= COLOR_PALETTE_POS[0] + COLOR_PALETTE_GRID_SIZE * (COLOR_PALETTE_SIZE + 1)):
                        palette_x = (x - COLOR_PALETTE_POS[0]) // (COLOR_PALETTE_SIZE + 1)
                        palette_y = (y - COLOR_PALETTE_POS[1]) // (COLOR_PALETTE_SIZE + 1)
                        i = palette_y * COLOR_PALETTE_GRID_SIZE + palette_x
                        if 0 <= i < len(color_palette):
                            color = color_palette[i]
                    else:
                        drawing = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False

        if drawing:
            x, y = pygame.mouse.get_pos()
            grid_x = x // GRID_SIZE
            grid_y = y // GRID_SIZE
            grid[grid_x][grid_y] = color

        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        draw_color_palette()

        pygame.display.flip()


if __name__ == "__main__":
    main()
