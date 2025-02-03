import pygame
import sys
import pytmx #Imported the pytmx module
pygame.init() #Simply initialises pygame and all its modules
pygame.font.init() #Initialise the fonts I want to use
from classes import Button, box



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (127, 255, 212)

game_state = bool(False)

def load_tmx_map(filename):
    return pytmx.load_pygame(filename)

map_one = load_tmx_map("./Maps/base_map.tmx")

def render_map(surface, tmx_data):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    surface.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))



pygame.display.set_caption("Title Screen") #Sets the title of the window to "Title Screen"
icon = pygame.image.load(".\Images\icon.png") #Loads the image "icon.png" into the variable "icon"
icon = pygame.transform.scale(icon, (500, 500))
pygame.display.set_icon(icon) #Sets the icon of the window to the image "icon.png"
display_list = pygame.display.get_desktop_sizes() #Obtains resolutions of all the displays
resolution = display_list[0]
screen = pygame.display.set_mode(display_list[0],flags=pygame.FULLSCREEN,depth=0,display=0,vsync=0) #A bit more complex here in that it renders the display to my monitor's resolution, 
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial",260,True) #Added the titlefont
small_title = pygame.font.SysFont("Arial", 100, True)
timer_font = pygame.font.Font(None, 36)


screen_buttons = []
screen_button = Button("START", ((resolution[0] - 100) // 2 -100, 3 * ((resolution[1] - 100) // 4)), (100, 100), BLACK, WHITE)
screen_exit_button = Button("EXIT", (((resolution[0] - 100) // 2) +100, 3 * ((resolution[1] - 100) // 4)), (100, 100), BLACK, WHITE)
screen_buttons.append(screen_button)
screen_buttons.append(screen_exit_button)

def start_screen(screen_colour, title_colour, resolution):
    screen.fill(screen_colour)
    title_text = font.render("SUPERFIGHTERS",True , title_colour)
    t_text_width = title_text.get_width()
    t_text_height = title_text.get_height()

    screen.blit(title_text, (resolution[0] // 2 - t_text_width // 2, resolution[1] // 2 - t_text_height // 2))
    for button in screen_buttons:
        button.draw(screen)


choice_buttons = []
one_player = Button("ONE PLAYER", ((resolution[0] - 100) // 7, ((resolution[1]) // 2)), (100, 100), WHITE)
two_player = Button("TWO PLAYER", ((resolution[0] - 100) // 7, ((resolution[1]) // 2)+100), (100, 100), WHITE)
tutorial = Button("TUTORIAL", ((resolution[0] - 100) // 7, ((resolution[1]) // 2)+200), (100, 100), WHITE)
setup = Button("SETUP", ((resolution[0] - 100) // 7, ((resolution[1]) // 2)+300), (100, 100), WHITE)
choice_buttons.append(one_player)
choice_buttons.append(two_player)
choice_buttons.append(tutorial)
choice_buttons.append(setup)

def choice_screen(screen_colour, title_colour, resolution):
    pygame.display.set_caption("Game Modes")
    screen.fill(screen_colour)
    title_text = font.render("SUPERFIGHTERS",True , title_colour)
    main_text_width = title_text.get_width()
    main_text_height = title_text.get_height()

    screen.blit(title_text, ((resolution[0]) // 2 - main_text_width // 2, (resolution[1]-400) // 2 - main_text_height // 2))
    for button in choice_buttons:
        button.draw(screen)

# onep_buttons = []
# one_player = Button("ONE PLAYER", ((resolution[0] - 100) // 7, ((resolution[1]) // 2)), (100, 100), WHITE)
# two_player = Button("TWO PLAYER", ((resolution[0] - 100) // 7, ((resolution[1]) // 2)+100), (100, 100), WHITE)
# tutorial = Button("TUTORIAL", ((resolution[0] - 100) // 7, ((resolution[1]) // 2)+200), (100, 100), WHITE)
# setup = Button("SETUP", ((resolution[0] - 100) // 7, ((resolution[1]) // 2)+300), (100, 100), WHITE)
# onep_buttons.append(one_player)
# onep_buttons.append(two_player)
# onep_buttons.append(tutorial)
# onep_buttons.append(setup)

onep_boxes = []
box_width = 500
box_height = 500
onep_box = box((box_width,box_height), ((resolution[0] - box_width) // 2, ((resolution[1] - box_height) // 2)), WHITE)
onep_box.surface.blit(icon)
onep_boxes.append(onep_box)

onep_buttons = []
start_game = Button("BEGIN",((resolution[0] // 2) -120, 3 * ((resolution[1] // 4))), (100, 100), WHITE)
onep_buttons.append(start_game)

def oneplayer_screen(screen_colour, title_colour, resolution):
    pygame.display.set_caption("One PLayer Mode")
    screen.fill(screen_colour)
    title_text = small_title.render("SUPERFIGHTERS",True , title_colour)
    main_text_width = title_text.get_width()
    main_text_height = title_text.get_height()
    screen.blit(title_text, ((resolution[0]- main_text_width) // 2, (resolution[1]-800 - main_text_height) // 2))
    for box in onep_boxes:
        box.draw(screen)
    for button in onep_buttons:
        button.draw(screen)


def gameplay_screen():
    pygame.display.set_caption("Gameplay")
    render_map(screen, map_one)












screen_selector = "start"

if __name__ == "__main__":    
    game_state = True
    while game_state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_loc = pygame.mouse.get_pos()

            if screen_selector == "start":
                for start_button in screen_buttons:
                    if event.type == pygame.MOUSEBUTTONDOWN: #If the mouse is clicked
                        if start_button.rect.collidepoint(mouse_loc): #If the mouse is clicked within the button boundaries 
                            if start_button.text == "START": #Self explanatory 
                                screen_selector = "MAIN"
                            elif start_button.text == "EXIT":
                                game_state = False

            if screen_selector == "MAIN":
                for choice_button in choice_buttons:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if choice_button.rect.collidepoint(mouse_loc):
                            if choice_button.text == "ONE PLAYER":
                                screen_selector = "ONE PLAYER"
                                print("ONE PLAYER")
                            elif choice_button.text == "TWO PLAYER":
                                screen_selector = "TWO PLAYER"
                                print("TWO PLAYER")

            if screen_selector == "ONE PLAYER":
                for onep_button in onep_buttons:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if choice_button.rect.collidepoint(mouse_loc):
                            if onep_button.text == "START GAME":
                                screen_selector = "GAMEPLAY"
                                print("GAMEPLAY")
                

        if screen_selector == "start":
            start_screen(BLACK, WHITE, resolution)

        if screen_selector == "MAIN":
            choice_screen(BLACK, WHITE, resolution)
        
        if screen_selector == "ONE PLAYER":
            oneplayer_screen(BLACK, WHITE, resolution)

        if screen_selector == "GAMEPLAY":
            gameplay_screen()

        


        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()


