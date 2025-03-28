import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

display_list = pygame.display.get_desktop_sizes() #Obtains resolutions of all the displays
resolution = display_list[0]

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
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (resolution[0] // 2, resolution[1] // 2)

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 8
        if keys[pygame.K_RIGHT] and self.rect.right < resolution[0]:
            self.rect.x += 8

# Enemy sprite class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(0,resolution[0]), y)

    def update(self, speed=3):
        self.rect.y += speed
        if self.rect.top > resolution[1]:
            self.rect.bottom = 0
            self.rect.left = random.randint(0,resolution[0])
    

