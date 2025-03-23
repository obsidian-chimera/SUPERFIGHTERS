import pygame
import math
import heapq
from pathfinding import *
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
        self.rect = pygame.FRect(self.position, (self.width, self.height))

        # Constructor method to setup attributes for the button

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
        x = self.rect.x + (self.rect.width - self.surface.get_width()) // 2
        y = self.rect.y + (self.rect.height - self.surface.get_height()) // 2
        screen.blit(self.surface, (x,y))

        # Method to draw the button onto the screen with the text superimposed on top of the button background
class box:
    # Box class that allows for the creation of a box object with attributes below
    def __init__(self, size, position, colour):
        self.size = size
        self.position = position
        self.colour = colour
        # FRect object to store the size and position of the box and allows for the usage of floating point values 
        self.rect = pygame.FRect(self.position, self.size)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.colour)
        text_width, text_height = self.surface.get_size()
        self.width = text_width
        self.height = text_height

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
    
# # Inherits the library class pygame.sprite.Sprite
# class object(pygame.sprite.Sprite):
#     def __init__(self, position, image, classification):
#         super().__init__(classification)
#         self.image = image
#         self.rect = self.image.get_frect(topleft = position)
    
#     def draw(self, screen):
#         screen.blit(self.image, self.rect)

#     # Allows the object to be added to the sprite group and drawn onto the screen and updated without getting a method error
#     def update(self):
#         pass

# Creates a button class that allows for the creation of a button object with attributes below 
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
        self.rect = pygame.FRect(self.position, (self.width, self.height))

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
        x = self.rect.x + (self.rect.width - self.surface.get_width()) // 2 # Centers the text on the button
        y = self.rect.y + (self.rect.height - self.surface.get_height()) // 2
        screen.blit(self.surface, (x, y))

# Similar to the object class but creates a box instead 
class Box:
    def __init__(self, size, position, colour):
        self.size = size
        self.position = position
        self.colour = colour
        self.rect = pygame.FRect(self.position, self.size)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.colour)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

# Inherits the pygame.sprite.Sprite class from the library
class Object(pygame.sprite.Sprite):
    def __init__(self, position, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_frect(topleft=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Creates a player class from inheriting the Object class
class Player(Object):
    def __init__(self, position, image, collision_rects, instadeath, current_game): # Constructor method to setup attributes for the player
        super().__init__(position, image)
        self.starting_position = position
        self.speed = 5
        self.g_constant = 1
        self.velocity_y = 0
        self.on_ground = False
        
        self.collision_rects = collision_rects
        self.instadeath_rects = instadeath
        
        self.lives = 3
        self.health = 100

        self.direction = 1
        self.bullets = pygame.sprite.Group()
        self.gun = Gun(self, self.bullets, collision_rects= self.collision_rects)
        self.game = current_game

        self.last_teleport = 0
        self.teleport_delay = 2000

        self.kills = 0
        self.xp = 0

    def move(self, dx, dy):
        # Move horizontally
        self.rect.x += dx
        # Deals with horizontal collisons 
        for rect in self.collision_rects:
            if self.rect.colliderect(rect):
                if dx > 0:  # Moving right
                    self.rect.right = rect.left
                elif dx < 0:  # Moving left
                    self.rect.left = rect.right

        # Move vertically
        self.rect.y += dy
        # Deals with vertical collisions
        for rect in self.collision_rects:
            if self.rect.colliderect(rect):
                if dy > 0 :  # Moving down
                    self.rect.bottom = rect.top
                    self.on_ground = True
                    self.velocity_y = 0
                elif dy < 0:  # Moving up
                    self.rect.top = rect.bottom
                    self.velocity_y = 0

    # Applies gravity to the player object
    def gravity(self):
        if not self.on_ground:
            self.velocity_y += self.g_constant
            if self.velocity_y > 10:  # Terminal velocity
                self.velocity_y = 10
        self.on_ground = False
        self.move(0, self.velocity_y)

    # Allows for the player to move and jump
    def input(self):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_a]:
            dx = -self.speed
            self.direction = -1
        if keys[pygame.K_d]:
            dx = self.speed
            self.direction = 1
        if keys[pygame.K_w] and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False
        if keys[pygame.K_LCTRL]:
            self.gun.shoot()
        if keys[pygame.K_r]:
            self.lives = LIVES

        self.move(dx, 0)

    # Checks if the player object collides with an instadeath object
    def instadeath(self):
        for rect in self.instadeath_rects:
            if self.rect.colliderect(rect):
                print("You died!")
                self.lives -= 1
                if self.lives <= 0:
                    print("Game over!")
                    self.kill()
                    return
                else:
                    print(f"Lives: {self.lives}")
                    self.rect.topleft = self.starting_position # Returns the player to the pin placed on the map

    # Deals with the player taking damage from the gun
    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            if self.lives == 0:
                print("Game over!")
                self.kill()
            else:
                self.lives -= 1
                print(f"Lives: {self.lives}")
                self.health = 100
                self.rect.topleft = self.starting_position # Returns the player to the pin placed on the map

    def check_teleport(self):
        now = pygame.time.get_ticks()
        if now - self.last_teleport < self.teleport_delay:
            return

        for teleport in self.game.teleports:
            teleport_rect = pygame.FRect(
                teleport.x, 
                teleport.y, 
                teleport.width, 
                teleport.height,
            )

            if self.rect.colliderect(teleport_rect):
                target_id = teleport.properties.get('teleport_target')
                target = self.game.object_id_list.get(target_id)
                if target_id:
                    print(f"Teleporting to object ID {target_id}")
                    self.rect.topleft = (
                        target.x,
                        target.y
                    )
                    self.last_teleport = now
                    return  # Only teleport once per frame

    def update(self):
        self.instadeath()
        self.check_teleport()
        self.input()
        self.gravity()
        self.bullets.update()

# Inherits the player class to create a second player object but overrides the input method to allow for different controls
class Player2(Player):
    def __init__(self, position, image, collision_rects, instadeath, current_game):
        super().__init__(position, image, collision_rects, instadeath, current_game)

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
        if keys[pygame.K_r]:
            self.lives = LIVES

        self.move(dx, 0)

# Bullet class that inherits the pygame.sprite.Sprite class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction, speed, owner, collision_rects):
        super().__init__()
        self.image = pygame.Surface((10, 5))  
        self.image.fill(RED)
        self.rect = self.image.get_frect(center=position)
        self.speed = speed
        self.direction = direction 
        self.now = pygame.time.get_ticks()
        self.collision_rects = collision_rects
        self.owner = owner # The player who shot the bullet

    def update(self):
        self.rect.x += self.speed * self.direction  # Move bullet
        if self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width():
            self.kill()  # Remove bullet when off-screen
        if pygame.time.get_ticks() - self.now > 300:
            self.kill() 
        if self.collision_rects: # Removes bullet when colliding with a rect
            for rect in self.collision_rects:
                if self.rect.colliderect(rect):
                    self.kill()
        
        for entity in pygame.sprite.spritecollide(self, self.owner.game.sprites, False):
            if isinstance(entity, (Player, Player2, Enemy)) and entity != self.owner:  # Ensure bullet only does damage if it belongs to a different player
                entity.damage(20)
                self.owner.xp += DAMAGE_XP
                self.kill()
            if entity.health <= 0:
                self.owner.kills += 1
                self.owner.xp += KILL_XP

# Gun class that allows for the creation of a gun object with attributes below that uses the bullets
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
            bullet = Bullet(self.host.rect.center, self.host.direction, self.bullet_speed, self.host, self.collision_rects)
            self.bullet_group.add(bullet)
            self.now = pygame.time.get_ticks()

# Enemy class that inherits the Object class
class Enemy(Object):
    def __init__(self, position, image, collision_rects, instadeath, game, player):
        super().__init__(position, image)
        self.starting_position = position
        self.speed = 2
        self.g_constant = 1
        self.velocity_y = 0
        self.on_ground = False

        self.collision_rects = collision_rects
        self.instadeath_rects = instadeath

        self.lives = 3
        self.health = 100

        self.direction = 1
        self.bullets = pygame.sprite.Group()
        self.gun = Gun(self, self.bullets, collision_rects=self.collision_rects)
        self.game = game
        self.player = player

        self.jump_needed_collision = False
        self.graph = game.graph
        self.path = []
        self.frame_counter = 0

        self.debug_switch = False

        self.last_teleport = 0
        self.teleport_delay = 1000

        self.fire_cooldown = 250  # milliseconds between shots
        self.last_shot_time = 0
        self.xp = 0




    def distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
   
    def gravity(self):
        if not self.on_ground:
            self.velocity_y += self.g_constant
            self.velocity_y = min(self.velocity_y, 10)
        self.on_ground = False
        self.move(0, self.velocity_y)

    def instadeath(self):
        for rect in self.instadeath_rects:
            if self.rect.colliderect(rect):
                print("You died!")
                self.lives -= 1
                if self.lives <= 0:
                    print("Game over!")
                    self.kill()
                    return
                else:
                    print(f"Lives: {self.lives}")
                    self.rect.topleft = self.starting_position
                    self.path = []

    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            if self.lives == 0:
                print("Game over!")
                self.kill()
            else:
                self.lives -= 1
                print(f"Lives: {self.lives}")
                self.health = 100
                self.rect.topleft = self.starting_position

    def check_teleport(self):
        now = pygame.time.get_ticks()
        if now - self.last_teleport < self.teleport_delay:
            return

        for teleport in self.game.teleports:
            teleport_rect = pygame.FRect(
                teleport.x, 
                teleport.y, 
                teleport.width, 
                teleport.height,
            )

            if self.rect.colliderect(teleport_rect):
                target_id = teleport.properties.get('teleport_target')
                target = self.game.object_id_list.get(target_id)
                if target_id:
                    print(f"Teleporting to object ID {target_id}")
                    self.rect.topleft = (
                        target.x,
                        target.y
                    )
                    self.last_teleport = now
                    return  # Only teleport once per frame
                
    def auto_firing(self):
        now = pygame.time.get_ticks()

        # Simple condition: shoot if in range and cooldown passed
        distance_to_player = math.hypot(
            self.player.rect.centerx - self.rect.centerx,
            self.player.rect.centery - self.rect.centery
        )

        if distance_to_player < 400:  # Only shoot if within 400px
            if now - self.last_shot_time > self.fire_cooldown:
                # Determine direction: left or right
                if self.player.rect.centerx > self.rect.centerx:
                    self.direction = 1
                else:
                    self.direction = -1

                self.gun.shoot()
                self.last_shot_time = now

    def move(self, dx=0, dy=0):
        # Horizontal collisions
        self.rect.x += dx
        if not self.debug_switch:
            for rect in self.collision_rects:
                # self.jump_needed_collision = False
                if self.rect.colliderect(rect):
                    if dx > 0:
                        self.rect.right = rect.left
                        self.jump_needed_collision = True
                    elif dx < 0:
                        self.rect.left = rect.right
                        self.jump_needed_collision = True
        
        # Vertical collisions
        self.rect.y += dy
        if not self.debug_switch:
            for rect in self.collision_rects:
                if self.rect.colliderect(rect):
                    if dy > 0:
                        self.rect.bottom = rect.top
                        self.on_ground = True
                        self.velocity_y = 0
                    elif dy < 0:
                        self.rect.top = rect.bottom
                        self.velocity_y = 0

    def check_jump(self):
        # Check if there's ground directly below
        ground_below = False
        for tile in self.collision_rects:
            if tile.colliderect(self.rect.move(0, 10)):
                ground_below = True
                break

        # Check if moving forward would result in falling off an edge
        edge_ahead = True
        for tile in self.collision_rects:
            if tile.colliderect(self.rect.move(self.direction * 5, 10)):
                edge_ahead = False
                break
        
        return ground_below and edge_ahead


    def jump_motion(self):
        if self.check_jump() or self.jump_needed_collision:
            self.velocity_y = -15  # Apply jump force
            self.move(self.direction * self.speed * 30, 0)
            self.jump_needed_collision = False
        else:
            pass
        
        self.gravity()

    def get_nearest_node(self, position):
        # Find the closest node to a given position.
        closest_node = None
        min_distance = float('inf')
        for node_id, node_pos in self.graph.points.items():
            dist = self.distance(position, node_pos)
            if dist < min_distance:
                min_distance = dist
                closest_node = node_id
        return closest_node

    def find_path_to_player(self):
        # Find a path to the player's position using A*.
        start_node = self.get_nearest_node(self.rect.center)
        goal_node = self.get_nearest_node(self.player.rect.center)

        if start_node is None or goal_node is None:
            print("No valid path! Start or Goal node not found.")
            return

        new_path = self.graph.astar(start_node, goal_node)
        
        if new_path:
            self.path = [self.graph.points[node] for node in new_path]
            print(f"Path found: {self.path}")  # Debug path
        else:
            print("No valid path!")



    def move_along_path(self):
        # Move the enemy along the computed A* path.
        if self.path:
            target_x, target_y = self.path[0]  # Get the next waypoint
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)

            print(f"Moving to {target_x}, {target_y} | Distance: {distance}")

            if dx > 0:
                self.direction = 1
            elif dx < 0:
                self.direction = -1

            if distance > 50:  # Allow more tolerance (increased from 5)
                move_x = (dx / distance) * self.speed
                move_y = (dy / distance) * self.speed
                self.move(move_x, move_y)
            else:
                print(f"Reached waypoint {self.path[0]} - Removing from path")
                self.path.pop(0)  # Remove the waypoint

                # Edge case: If stuck, force pop
                if len(self.path) > 1 and self.distance(self.rect.center, self.path[0]) < 50:
                    print("Stuck at waypoint. Forcing pop")
                    self.path.pop(0)  
        else:
            print("No waypoints left")


    

    def update(self):
        self.frame_counter += 1
        if not self.debug_switch:
            self.instadeath()
            self.gravity()
            self.jump_motion()
        self.check_teleport()
        self.auto_firing()
        self.bullets.update()
        self.move_along_path()
        if not self.path or self.frame_counter > FRAMERATE and self.on_ground:
            print("Recalculating path")
            self.find_path_to_player()  # Recalculate if no path
            self.frame_counter = 0
        







