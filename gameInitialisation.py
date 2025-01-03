import pygame
def init():
    pygame.init() #Simply initialises pygame and all its modules
    display_list = pygame.display.get_desktop_sizes() #Obtains resolutions of all the displays
    screen = pygame.display.set_mode(display_list[0],flags=pygame.FULLSCREEN,depth=0,display=0,vsync=0) #A bit more complex here in that it renders the display to my monitor's resolution, 
    #A few more comments to explain the above:
    #Essentially, the first part sets the resolution of the default display, the second part is a flag that ensures that it is fullscreen, the third enables the correct colours to be used, the fourth enables the default display to be selected, whilst the last one turns off Vsync
    clock = pygame.time.Clock #Creates an object called clock to track time
init()