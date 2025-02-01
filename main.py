import pygame
import sys
import pytmx #Imported the pytmx module
pygame.init() #Simply initialises pygame and all its modules
pygame.font.init() #Initialise the fonts I want to use
from classes import Button



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (127, 255, 212)

game_state = bool(False)

display_list = pygame.display.get_desktop_sizes() #Obtains resolutions of all the displays
resolution = display_list[0]
screen = pygame.display.set_mode(display_list[0],flags=pygame.FULLSCREEN,depth=0,display=0,vsync=0) #A bit more complex here in that it renders the display to my monitor's resolution, 
pygame.display.set_caption("Title Screen") #Sets the title of the window to "Title Screen"
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial",260,True) #Added the titlefont
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
one_player = Button("ONE PLAYER", ((resolution[0] - 100) // 4, 3 * ((resolution[1] - 100) // 4)), (100, 100), WHITE)
two_player = Button("TWO PLAYER", (((resolution[0] - 100) // 4), 3 * ((resolution[1] - 250) // 4)), (100, 100), WHITE)
choice_buttons.append(one_player)
choice_buttons.append(two_player)

def choice_screen(screen_colour, title_colour, resolution):
    screen.fill(screen_colour)
    title_text = font.render("SUPERFIGHTERS",True , title_colour)
    main_text_width = title_text.get_width()
    main_text_height = title_text.get_height()

    screen.blit(title_text, (resolution[0] // 2 - main_text_width // 2, resolution[1] // 2 - main_text_height // 2))
    for button in choice_buttons:
        button.draw(screen)


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


            for start_button in screen_buttons:
                if event.type == pygame.MOUSEBUTTONDOWN: #If the mouse is clicked
                    if start_button.rect.collidepoint(mouse_loc): #If the mouse is clicked within the button boundaries 
                        if start_button.text == "START": #Self explanatory 
                            screen_selector = "MAIN"
                        elif start_button.text == "EXIT":
                            game_state = False
            for choice_button in choice_buttons:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if choice_button.rect.collidepoint(mouse_loc):
                        if choice_button.text == "ONE PLAYER":
                            screen_selector = "ONE PLAYER"
                            print("ONE PLAYER")
                        elif choice_button.text == "TWO PLAYER":
                            screen_selector = "TWO PLAYER"
                            print("TWO PLAYER")

        if screen_selector == "start":
            screen.fill(BLACK)
            start_screen(BLACK, WHITE, resolution)

        if screen_selector == "MAIN":
            screen.fill(BLUE)
            choice_screen(BLUE, WHITE, resolution)

        


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


