import pygame
import random
import sys
from classes import Player, Enemy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

game_state = bool(False)

pygame.init() #Simply initialises pygame and all its modules
pygame.font.init() #Initialise the fonts I want to use
display_list = pygame.display.get_desktop_sizes() #Obtains resolutions of all the displays
resolution = display_list[0]
screen = pygame.display.set_mode(display_list[0],flags=pygame.FULLSCREEN,depth=0,display=0,vsync=0) #A bit more complex here in that it renders the display to my monitor's resolution, 
pygame.display.set_caption("Title Screen") #Sets the title of the window to "Title Screen"
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial",40,True) #Added the titlefont
timer_font = pygame.font.Font(None, 36)  
    



