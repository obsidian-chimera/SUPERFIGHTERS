import pygame
class Button:
    def __init__(self, text, position, size, colour):
        self.text = text
        self.position = position
        self.size = size
        self.colour = colour
        self.font = pygame.font.SysFont("Arial",40,True)
        self.rect = pygame.Rect(self.position,self.size)
        self.text_surface = self.font.render(self.text,True,(0,0,0))
        
