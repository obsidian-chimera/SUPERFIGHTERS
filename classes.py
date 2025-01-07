import pygame
class Button:
    def __init__(self, text, position, size, colour):
        self.text = text
        self.position = position
        self.size = size
        self.colour = colour
        self.font = pygame.font.SysFont("Arial",40,True)
        self.rect = pygame.Rect(self.position,self.size)
        self.surface = self.font.render(self.text,True,(0,0,0))

        # Constructor method to setup attributes for the button

    def draw(self, screen):
        pygame.draw.rect(screen,self.colour,self.rect)
        screen.blit(self.text_surface,self.rect)

        # Method to draw the button onto the screen with the text superimposed on top of the button background

    

