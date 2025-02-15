import pygame
import pytmx
from classes import Player

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

# Load TMX Map
tmx_data = pytmx.load_pygame(".\collisions_test\world.tmx")
tile_size = tmx_data.tilewidth

# Get collision objects from the 'Collisions' layer
collision_rects = []
for layer in tmx_data.objectgroups:
    if layer.name == "Collisions":
        for obj in layer:
            collision_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

# Ensure objects are scaled properly
map_width = tmx_data.width * tile_size
map_height = tmx_data.height * tile_size

# Player setup
player = Player((50, 50), collision_rects)

# Draw tiles
def draw_map(surface, tmx_data):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    surface.blit(tile, (x * tile_size, y * tile_size))

# Camera adjustment
def apply_camera_offset(rect):
    return rect.move(-player.rect.x + WIDTH // 2, -player.rect.y + HEIGHT // 2)

# Game Loop
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    player.update(keys)
    
    draw_map(screen, tmx_data)
    player.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
