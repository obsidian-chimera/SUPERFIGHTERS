import pygame

class Player:
    def __init__(self, position, collision_rects):
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 0, 255))  # Blue color
        self.rect = self.image.get_rect(topleft=position)
        self.speed = 3
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = False
        self.collision_rects = collision_rects
    
    def move(self, dx, dy):
        new_rect = self.rect.move(dx, dy)
        if not self.check_collision(new_rect, dy):
            self.rect = new_rect
        else:
            if dy > 0:  # If moving down (falling), stop at collision
                self.velocity_y = 0
                self.on_ground = True
            elif dy < 0:  # If moving up (jumping), stop at collision
                self.velocity_y = 0

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity_y += self.gravity
        self.move(0, self.velocity_y)
    
    def check_collision(self, new_rect, dy):
        for rect in self.collision_rects:
            if new_rect.colliderect(rect):
                if dy > 0 and self.rect.bottom <= rect.top:  # Landing on the object
                    self.rect.bottom = rect.top
                    return True
                elif dy < 0 and self.rect.top >= rect.bottom:  # Hitting ceiling
                    return True
                return True
        return False
    
    def update(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP] and self.on_ground:  # Jump
            self.velocity_y = -10
            self.on_ground = False
        
        self.move(dx, dy)
        self.apply_gravity()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
