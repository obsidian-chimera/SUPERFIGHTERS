import pygame
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (127, 255, 212)
BACKGROUND = '#fcdfcd'

FRAMERATE = 100

display_list = pygame.display.get_desktop_sizes() #Obtains resolutions of all the displays
resolution = display_list[0]