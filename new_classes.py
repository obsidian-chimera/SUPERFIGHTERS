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

class Player(object):
    def __init__(self, position, image, classification, collision):
        super().__init__(position, image, classification)
        self.speed = 400
        self.gravity = 1
        self.shooting = False
        self.direction = pygame.Vector2(0, 0)
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
        if keys[pygame.K_w]:
            self.direction.y = -1
        if keys[pygame.K_s]:
            self.direction.y = 1
        # self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])   
        # self.direction.y = int(keys[pygame.K_w]) - int(keys[pygame.K_s])
    
    def collision_check(self):
        self.collided = False
        if self.player_rect.left < 0 or self.player_rect.right > resolution[0] or self.player_rect.top < 0 or self.player_rect.bottom > resolution[1]:
            self.collided = True
        for rect in self.collision:
            if self.player_rect.colliderect(rect):
                self.collided = True
                break
        return self.collided
    
    def grounded(self):
        self.ground = False
        if self.collision_check():
            return True
        
    def move(self):
        new_x = self.player_rect.x + (self.direction.x * self.speed)
        new_y = self.player_rect.y + (self.direction.y * self.speed)

        if not self.grounded():
            gravity = self.player_rect.y + self.gravity
            self.player_rect.move(0,gravity) 

        if not self.collision_check():
            self.player_rect.move(new_x,new_y)
        else:
            pass

    def update(self):
        self.input()
        self.move()

