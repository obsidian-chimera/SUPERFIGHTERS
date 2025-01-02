import pygame
def init():
    pygame.init() #Simply initialises pygame and all its modules
    screen = pygame.display.set_mode([1920,1080],flags=pygame.FULLSCREEN,depth=0,display=0,vsync=1) #A bit more complex here in that it renders the display to my monitor's resolution

init()