import pygame
from settings import *

class Button:
    def __init__(self, text, position, size, colour, text_colour=BLACK):
        self.text = text
        self.position = position
        self.size = size
        self.colour = colour
        self.font = pygame.font.SysFont("Arial",40,True)
        self.surface = self.font.render(self.text,True,text_colour)
        self.text_width, self.text_height = self.surface.get_size()
        self.width = self.text_width + 20
        self.height = self.text_height + 20
        self.rect = pygame.Rect(self.position, (self.width, self.height))

        # Constructor method to setup attributes for the button

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
        x = self.rect.x + (self.rect.width - self.surface.get_width()) // 2
        y = self.rect.y + (self.rect.height - self.surface.get_height()) // 2
        screen.blit(self.surface, (x,y))

        # Method to draw the button onto the screen with the text superimposed on top of the button background
class box:
    def __init__(self, size, position, colour):
        self.size = size
        self.position = position
        self.colour = colour
        self.rect = pygame.Rect(self.position, self.size)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.colour)
        text_width, text_height = self.surface.get_size()
        self.width = text_width
        self.height = text_height

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
    
class object(pygame.sprite.Sprite):
    def __init__(self, position, image, classification):
        super().__init__(classification)
        self.image = image
        self.rect = self.image.get_frect(topleft = position)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt=None):
        pass

class Player(object):
    def __init__(self, position, image, classification, collision):
        super().__init__(position, image, classification)
        self.speed = 400
        self.gravity = 1
        self.shooting = False
        self.direction = pygame.Vector2(0, 1)
        self.collision = collision
        self.ground = False
        self.player_rect = pygame.Rect(position, image.get_size())
        self.movement = pygame.Vector2(0, 0)
        self.position = pygame.Vector2(position)
        self.collided = False

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x = -1
        if keys[pygame.K_d]:    
            self.direction.x = 1
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])   