import pygame
import random
import sys
from block_game_classes import Player, Enemy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

game_state = bool(False)

pygame.init() #Simply initialises pygame and all its modules
pygame.font.init() #Initialise the fonts I want to use
display_list = pygame.display.get_desktop_sizes() #Obtains resolutions of all the displays
resolution = display_list[0]
screen = pygame.display.set_mode(display_list[0],flags=pygame.FULLSCREEN,depth=0,display=0,vsync=0) #A bit more complex here in that it renders the display to my monitor's resolution, 
pygame.display.set_caption("Title Screen") #Sets the title of the window to "Title Screen"
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial",40,True) #Added the titlefont
timer_font = pygame.font.Font(None, 36)  
    

# #A few more comments to explain the above:
# #Essentially, the first part sets the resolution of the default display, the second part is a flag that ensures that it is fullscreen, the third enables the correct colours to be used, the fourth enables the default display to be selected, whilst the last one turns off Vsync
# main_menu = pygame_m.Menu("START",1920,1080, theme=pygame_m.themes.THEME_BLUE,) 
# #main_menu.add_button("START","GAME STARTED")
# clock = pygame.time.Clock #Creates an object called clock to track time

# #pygame.set_caption("Menu") #Sets the title of the window to "Game"

player = Player()
player_group = pygame.sprite.Group(player)

enemies = pygame.sprite.Group()
for i in range(5):
    enemy = Enemy(i * 150 + 50, -50)
    enemies.add(enemy)

start_time = pygame.time.get_ticks()
spawn_time = pygame.time.get_ticks()

if __name__ == "__main__":
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player_group.update(keys)
        enemies.update()

        if pygame.sprite.spritecollide(player, enemies, False):
            print("Game Over!")
            running = False


        game_time = (pygame.time.get_ticks() - start_time) // 1000
        level_time = pygame.time.get_ticks() - start_time

        if (level_time - spawn_time) // 1000 > 5:
            enemy = Enemy(random.randint(0,resolution[0]), -50)
            enemies.add(enemy)
            spawn_time = pygame.time.get_ticks()

        timer_text = timer_font.render(f"Time: {game_time}s", True, BLACK)

        screen.fill(WHITE)
        player_group.draw(screen)
        enemies.draw(screen)
        screen.blit(timer_text, (10, 10))
    

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(250)
        

    pygame.quit()
    sys.exit()