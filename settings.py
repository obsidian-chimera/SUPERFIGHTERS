import pygame
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (127, 255, 212)
BACKGROUND = '#fcdfcd'

FRAMERATE = 100
TILE_SIZE = 64

display_list = pygame.display.get_desktop_sizes() #Obtains resolutions of all the displays
resolution = display_list[0]
LIVES = 3
KILL_XP = 100
DAMAGE_XP = 10