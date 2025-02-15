import pygame
import pytmx

pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyTMX Collision Test")
clock = pygame.time.Clock()

tmx_data = pytmx.load_pygame("./collisions_test/world.tmx")
# tile_size = tmx_data.tilewidth
# collision_rects = []
# print(tmx_data.objects)
# for obj in tmx_data.:
#     print(obj.name)
array = []
for layer in tmx_data.layers:
    if layer == 'Main':
        for item in layer:
            array.append(item)
print(array)

# for obj in tmx_data.objects:
#     if obj.name == "Collisions":
#         collision_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
#         print(collision_rects)