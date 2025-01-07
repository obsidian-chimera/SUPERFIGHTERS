import pygame

def game_loop(game_state):
    while game_state:
        pygame.display.flip() #This updates the display
        pygame.time.Clock().tick(250) #This is used to cap the frame rate to minimise unnecessary system resource usage

def game_state_update():
    return 
    #Unsure as to how to implement this as of yet - more research is need