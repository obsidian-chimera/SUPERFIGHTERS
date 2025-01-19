import pygame
import random
import sys


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

if __name__ == "__main__":    
    game_state = True
    while game_state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = False


        screen.fill(WHITE)
        title_text = font.render("Title Screen",True , BLACK)
        screen.blit(title_text, (resolution[0] // 2, resolution[1] // 2))



        pygame.display.flip()
        clock.tick(250)

    pygame.quit()
    sys.exit()


