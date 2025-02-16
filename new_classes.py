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

class Player(Object):
    def __init__(self, position, image, collision_rects, instadeath):
        super().__init__(position, image)
        self.starting_position = position
        self.speed = 5
        self.g_constant = 1
        self.velocity_y = 0
        self.on_ground = False
        
        self.collision_rects = collision_rects
        self.instadeath_rects = instadeath
        
        self.lives = 3

        self.direction = 0
        self.bullets = pygame.sprite.Group()
        self.gun = Gun(self, self.bullets, self.collision_rects)

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
                if dy > 0 :  # Moving down
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
            self.direction = -1
        if keys[pygame.K_d]:
            dx = self.speed
            self.direction = 1
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False
        if keys[pygame.K_LCTRL]:
            self.gun.shoot()

        self.move(dx, 0)

    def instadeath(self):
        for rect in self.instadeath_rects:
            if self.rect.colliderect(rect):
                print("You died!")
                self.lives -= 1
                print(f"Lives: {self.lives}")
                if self.lives == 0:
                    print("Game over!")
                    self.kill()
                else:
                    self.rect.topleft = self.starting_position


    def update(self):
        self.instadeath()
        self.input()
        self.gravity()
        self.bullets.update()

class Player2(Object):
    def __init__(self, position, image, collision_rects, instadeath):
        super().__init__(position, image)
        self.starting_position = position
        self.speed = 5
        self.g_constant = 1
        self.velocity_y = 0
        self.on_ground = False
        
        self.collision_rects = collision_rects
        self.instadeath_rects = instadeath
        
        self.lives = 3

        self.direction = 0
        self.bullets = pygame.sprite.Group()
        self.gun = Gun(self, self.bullets, self.collision_rects)

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
                if dy > 0 :  # Moving down
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
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = -1
        if keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = 1
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False
        if keys[pygame.K_RCTRL]:
            self.gun.shoot()

        self.move(dx, 0)

    def instadeath(self):
        for rect in self.instadeath_rects:
            if self.rect.colliderect(rect):
                print("You died!")
                self.lives -= 1
                print(f"Lives: {self.lives}")
                if self.lives == 0:
                    print("Game over!")
                    self.kill()
                else:
                    self.rect.topleft = self.starting_position


    def update(self):
        self.instadeath()
        self.input()
        self.gravity()
        self.bullets.update()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction, speed, collision_rects):
        super().__init__()
        self.image = pygame.Surface((10, 5))  
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.direction = direction 
        self.now = 0
        self.collision_rects = collision_rects

    def update(self):
        self.rect.x += self.speed * self.direction  # Move bullet
        if self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width():
            self.kill()  # Remove bullet when off-screen
        if self.now > 1000:
            self.kill()
            self.now = pygame.time.get_ticks()
        for rect in self.collision_rects:
            if self.rect.colliderect(rect):
                self.kill()



class Gun():
    def __init__(self, host, bullet_group, bullet_speed=10, fire_rate=10, collision_rects=[]):
        self.host = host  # The player holding the gun
        self.bullet_group = bullet_group
        self.bullet_speed = bullet_speed
        self.fire_rate = fire_rate
        self.now = 0
        self.collision_rects = collision_rects

    def shoot(self):
        if pygame.time.get_ticks() - self.now > 1000 // self.fire_rate:
            bullet = Bullet(self.host.rect.center, self.host.direction, self.bullet_speed, self.collision_rects)
            self.bullet_group.add(bullet)
            self.now = pygame.time.get_ticks()
