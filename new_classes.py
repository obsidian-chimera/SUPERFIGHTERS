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

    def update(self):
        pass

import pygame
from settings import *

class Button:
    def __init__(self, text, position, size, colour, text_colour=BLACK):
        self.text = text
        self.position = position
        self.size = size
        self.colour = colour
        self.font = pygame.font.SysFont("Arial", 40, True)
        self.surface = self.font.render(self.text, True, text_colour)
        self.text_width, self.text_height = self.surface.get_size()
        self.width = self.text_width + 20
        self.height = self.text_height + 20
        self.rect = pygame.Rect(self.position, (self.width, self.height))

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
        x = self.rect.x + (self.rect.width - self.surface.get_width()) // 2
        y = self.rect.y + (self.rect.height - self.surface.get_height()) // 2
        screen.blit(self.surface, (x, y))

class Box:
    def __init__(self, size, position, colour):
        self.size = size
        self.position = position
        self.colour = colour
        self.rect = pygame.Rect(self.position, self.size)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.colour)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

class Object(pygame.sprite.Sprite):
    def __init__(self, position, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class CollisionTile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0, 100))  # Semi-transparent red for debugging
        self.rect = pygame.Rect(x, y, width, height)

class Player(Object):
    def __init__(self, position, image, collision_rects):
        super().__init__(position, image)
        self.speed = 3
        self.g_constant = 1
        self.velocity_y = 0
        self.on_ground = False
        self.collision_rects = collision_rects

    def move(self, dx, dy):
        # Move horizontally
        self.rect.x += dx
        for rect in self.collision_rects:
            if self.rect.colliderect(rect):
                if dx > 0:  # Moving right
                    self.rect.right = rect.left
                elif dx < 0:  # Moving left
                    self.rect.left = rect.right

        # Move vertically
        self.rect.y += dy
        for rect in self.collision_rects:
            if self.rect.colliderect(rect):
                if dy > 0:  # Moving down
                    self.rect.bottom = rect.top
                    self.on_ground = True
                    self.velocity_y = 0
                elif dy < 0:  # Moving up
                    self.rect.top = rect.bottom
                    self.velocity_y = 0

    def gravity(self):
        if not self.on_ground:
            self.velocity_y += self.g_constant
            if self.velocity_y > 10:  # Terminal velocity
                self.velocity_y = 10
        self.on_ground = False
        self.move(0, self.velocity_y)

    def input(self):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_d]:
            dx = self.speed
        if keys[pygame.K_w] and self.on_ground:
            self.velocity_y = -20
            self.on_ground = False

        self.move(dx, 0)

    def update(self):
        self.input()
        self.gravity()

