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


class Player(object):
    def __init__(self, position, image, classification):
        super().__init__(position, image, classification)
        self.health = 100
        self.speed = 5
        self.jump = 10
        self.gravity = 1
        self.bullets = []
        self.weapon = None
        self.direction = 1
        self.jumping = False
        self.falling = False
        self.shooting = False
        self.dead = False
        self.score = 0
        self.kills = 0
        self.deaths = 0
        self.damage = 10
        self.direction = 1
    
    def move(self, direction):
        self.rect.x += direction * self.speed

    def jump(self):
        self.rect.y -= self.jump
        self.jumping = True
    
    def key_down(self, key):
        if key == pygame.K_w:
            self.jump()
        if key == pygame.K_a:
            self.move(-1)
        if key == pygame.K_d:
            self.move(1)
        if key == pygame.K_SPACE:
            self.jump()

class bot:
    pass

class bullet:
    pass

class weapon:
    pass

