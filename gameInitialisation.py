import pygame as pyg #I realised it would be easier later on to shorten pygame to pyg
def init():
    pyg.init() #Simply initialises pyg and all its modules
    pyg.font.init() #Initialise the fonts I want to use
    display_list = pyg.display.get_desktop_sizes() #Obtains resolutions of all the displays
    screen = pyg.display.set_mode(display_list[0],flags=pyg.FULLSCREEN,depth=0,display=0,vsync=0) #A bit more complex here in that it renders the display to my monitor's resolution, 
    #A few more comments to explain the above:
    #Essentially, the first part sets the resolution of the default display, the second part is a flag that ensures that it is fullscreen, the third enables the correct colours to be used, the fourth enables the default display to be selected, whilst the last one turns off Vsync
    clock = pyg.time.Clock #Creates an object called clock to track time
    title_font = pyg.font.SysFont("Arial",40,True) #Added the titlefont
