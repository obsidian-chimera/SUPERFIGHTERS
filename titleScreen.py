import pygame
import sys
from init import init
from classes import Button

init()

start = Button("start","START GAME",(100,100),(200,200), (0,0,0))
quit = Button("quit","QUIT GAME",(100,150),(200,200), (0,0,0))

game_state = bool(True)
while game_state:
    pass