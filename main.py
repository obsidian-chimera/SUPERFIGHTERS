import pygame
from gameInitialisation import init
from gameLoopUpdate import game_loop

game_state = bool(False)

if __name__ == "__main__":
    init()
    game_state = bool(True)
    game_loop(game_state)
    
