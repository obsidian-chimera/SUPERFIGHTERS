import pygame 
import pygame_menu #Verily easily creates menu screens
import sys
from classes import Player, Enemy

def init():
    pygame.init() #Simply initialises pygame and all its modules
    pygame.font.init() #Initialise the fonts I want to use
    display_list = pygame.display.get_desktop_sizes() #Obtains resolutions of all the displays
    screen = pygame.display.set_mode(display_list[0],flags=pygame.FULLSCREEN,depth=0,display=0,vsync=0) #A bit more complex here in that it renders the display to my monitor's resolution, 
    pygame.display.set_caption("Title Screen") #Sets the title of the window to "Title Screen"
    
    font = pygame.font.SysFont("Arial",40,True) #Added the titlefont
        

    # #A few more comments to explain the above:
    # #Essentially, the first part sets the resolution of the default display, the second part is a flag that ensures that it is fullscreen, the third enables the correct colours to be used, the fourth enables the default display to be selected, whilst the last one turns off Vsync
    # main_menu = pygame_m.Menu("START",1920,1080, theme=pygame_m.themes.THEME_BLUE,) 
    # #main_menu.add_button("START","GAME STARTED")
    # clock = pygame.time.Clock #Creates an object called clock to track time

    # #pygame.set_caption("Menu") #Sets the title of the window to "Game"

    player = Player()
    player_group = pygame.sprite.Group(player)

    enemies = pygame.sprite.Group()
    for i in range(5):
        enemy = Enemy(i * 150 + 50, -50)
        enemies.add(enemy)
