import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)



display_list = pygame.display.get_desktop_sizes() #Obtains resolutions of all the displays
resolution = display_list[0]

class Button:
    def __init__(self, text, position, size, colour, text_colour=BLACK):
        self.text = text
        self.position = position
        self.size = size
        self.colour = colour
        self.font = pygame.font.SysFont("Arial",40,True)
        self.rect = pygame.Rect(self.position,self.size)
        self.surface = self.font.render(self.text,True,text_colour)

        # Constructor method to setup attributes for the button

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
        screen.blit(self.surface, (self.position[0] + self.size[0] // 2 - self.surface.get_width() // 2, self.position[1] + self.size[1] // 2 - self.surface.get_height() // 2))

        # Method to draw the button onto the screen with the text superimposed on top of the button background