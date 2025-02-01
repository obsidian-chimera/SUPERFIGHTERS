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
        self.surface = self.font.render(self.text,True,text_colour)
        text_width, text_height = self.surface.get_size()
        new_width = max(self.size[0], text_width + 20)
        new_height = max(self.size[1], text_height + 20)
        self.rect = pygame.Rect(self.position, (new_width, new_height))

        # Constructor method to setup attributes for the button


    def draw(self, screen):
        text_width, text_height = self.surface.get_size()
        new_width = max(self.size[0], text_width + 20)
        new_height = max(self.size[1], text_height + 20)
        pygame.draw.rect(screen, self.colour, self.rect)
        screen.blit(self.surface, (new_width + self.size[0] // 2 - new_width // 2, new_height + self.size[1] // 2 - new_height // 2))

        # Method to draw the button onto the screen with the text superimposed on top of the button background