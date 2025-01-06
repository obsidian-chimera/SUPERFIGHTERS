import pygame as pyg
def game_loop(game_state):
    while game_state:
        pyg.display.flip() #This updates the display
        pyg.time.Clock().tick(250) #This is used to cap the frame rate to minimise unnecessary system resource usage