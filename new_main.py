import os
from settings import *
from new_classes import *
from pathfinding import *
import sys
import pygame
import pytmx
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.init()
pygame.font.init()

# Path fixing for executable creation
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


icon = pygame.image.load(resource_path("images/icon.png"))  # Loads the image "icon.png" into the variable "icon"
icon = pygame.transform.scale(icon, (500, 500))
display_list = pygame.display.get_desktop_sizes()  # Obtains resolutions of all the displays
resolution = display_list[0]
font = pygame.font.SysFont("Arial", 230, True)  # Added the titlefont
small_title = pygame.font.SysFont("Arial", 100, True)
smaller_font = pygame.font.Font(None, 36)

game_state = False



class Game:
    def __init__(self):
        pygame.display.set_caption("Title Screen")  # Sets the title of the window to "Title Screen"
        pygame.display.set_icon(icon)  # Sets the icon of the window to the image "icon.png"
        self.screen = pygame.display.set_mode(display_list[0], flags=pygame.FULLSCREEN, depth=0, display=0, vsync=0)
        self.clock = pygame.time.Clock()
        self.map = None
        self.buttons = []
        self.boxes = []
        self.sliders = []
        self.textboxes = []
        self.sprites = pygame.sprite.Group()
        self.collision = []
        self.instadeath = []
        self.teleports = []
        self.object_id_list = {}
        self.scale_factor = 1
        self.enemy_count = 8
        self.player = None
        self.player2 = None

        # Loads all the data from the .tmx file for the pathfinding to take place --> Creates a graph from the data
        self.nodes, self.edges = load_navmesh("./Maps/world - copy.tmx")
        self.graph = Graph(self.nodes, self.edges)

        # Added a debug switch to change the highlighting of boxes and drawing of polylines
        self.debug_switch = True    
    
    # Creates the start screen with the single start button
    def start_screen(self, screen_colour, title_colour, resolution):
        self.buttons = []
        self.boxes = []
        screen_button = Button("START", ((resolution[0] - 100) // 2 - 100, 3 * ((resolution[1] - 100) // 4)), (100, 100), BLACK, WHITE)
        screen_exit_button = Button("EXIT", (((resolution[0] - 100) // 2) + 100, 3 * ((resolution[1] - 100) // 4)), (100, 100), BLACK, WHITE)
        self.buttons += [screen_button, screen_exit_button]

        self.screen.fill(screen_colour)
        title_text = font.render("SUPERFIGHTERS", True, title_colour)
        t_text_width = title_text.get_width()
        t_text_height = title_text.get_height()

        self.screen.blit(title_text, (resolution[0] // 2 - t_text_width // 2, resolution[1] // 2 - t_text_height // 2))
        for button in self.buttons:
            button.draw(self.screen)

    # Creates a selection screen to allow the player to choose between one player, two player, tutorial, etc....
    def choice_screen(self, screen_colour, title_colour, resolution):
        self.buttons = []
        self.boxes = []
        one_player = Button("ONE PLAYER", ((resolution[0] - 100) // 7, (resolution[1] // 2)), (100, 100), WHITE)
        two_player = Button("TWO PLAYER", ((resolution[0] - 100) // 7, (resolution[1] // 2) + 100), (100, 100), WHITE)
        tutorial = Button("TUTORIAL", ((resolution[0] - 100) // 7, (resolution[1] // 2) + 200), (100, 100), WHITE)
        setup = Button("SETUP", ((resolution[0] - 100) // 7, (resolution[1] // 2) + 300), (100, 100), WHITE)
        self.buttons += [one_player, two_player, tutorial, setup]

        # Changes the screen caption title
        pygame.display.set_caption("Game Modes")
        self.screen.fill(screen_colour)
        title_text = font.render("SUPERFIGHTERS", True, title_colour)
        main_text_width = title_text.get_width()
        main_text_height = title_text.get_height()

        # Renders the text and draws the buttons onto the screen
        self.screen.blit(title_text, (resolution[0] // 2 - main_text_width // 2, (resolution[1] - 400) // 2 - main_text_height // 2))
        for button in self.buttons:
            button.draw(self.screen)

    def one_player_screen_widget_setup(self):
        self.sliders = []
        self.textboxes = []
        slider1 = Slider(
            self.screen,  # The surface to render the slider on
            (resolution[0] - 100) // 2,  # X-coordinate
            3 * ((resolution[1] - 100) // 4) +200,  # Y-coordinate
            100,  # Width
            20,  # Height
            min=1,
            max=8,
            step=1,
            initial=1,
            colour=(255, 255, 255),
            handleColour=(250, 0, 0),
        )
        textbox1 = TextBox(
            self.screen,  # The surface to render the textbox on
            (resolution[0] - 100) // 2,  # x-coordinate
            3 * ((resolution[1] - 100) // 4) + 250,  # y-coordinate
            100,  # width
            100,  # height
            fontSize=50,
            textColour=(0, 0, 0),
            colour=(255, 255, 255),  # This corresponds to backgroundColour
            borderColour=(0, 0, 0)
        )   
        textbox1.disable()
        self.sliders.append(slider1)
        self.textboxes.append(textbox1)


    # Creates a screen for the one player mode
    def oneplayer_screen(self, screen_colour, title_colour, resolution):
        self.buttons = []
        self.boxes = []
        box_width = 500
        box_height = 500
        onep_box = box((box_width, box_height), ((resolution[0] - box_width) // 2, (resolution[1] - box_height) // 2), WHITE)
        onep_box.surface.blit(icon, (0, 0))
        self.boxes.append(onep_box)

        start_game = Button("BEGIN", ((((resolution[0] - 100) // 2), 3 * ((resolution[1]- 100) // 4)+60)), (100, 100), WHITE)
        self.buttons.append(start_game)

        pygame.display.set_caption("One Player Mode")
        self.screen.fill(screen_colour)
        
        # Renders the text and draws the buttons onto the screen
        title_text = small_title.render("SUPERFIGHTERS", True, title_colour)
        main_text_width = title_text.get_width()
        main_text_height = title_text.get_height()
        self.screen.blit(title_text, ((resolution[0] - main_text_width) // 2, (resolution[1] - 800 - main_text_height) // 2))
        for box_item in self.boxes:
            box_item.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)

    def twoplayer_screen(self, screen_colour, title_colour, resolution):
        self.buttons = []
        self.boxes = []
        box_width = 500
        box_height = 500
        twop_box = box((box_width, box_height), ((resolution[0] - box_width) // 2, (resolution[1] - box_height) // 2), WHITE)
        twop_box.surface.blit(icon, (0, 0))
        self.boxes.append(twop_box)

        start_game = Button("BEGIN", ((((resolution[0] - 100) // 2), 3 * ((resolution[1]- 100) // 4)+60)), (100, 100), WHITE)
        self.buttons.append(start_game)

        pygame.display.set_caption("TWO Player Mode")
        self.screen.fill(screen_colour)
        
        title_text = small_title.render("SUPERFIGHTERS", True, title_colour)
        main_text_width = title_text.get_width()
        main_text_height = title_text.get_height()
        self.screen.blit(title_text, ((resolution[0] - main_text_width) // 2, (resolution[1] - 800 - main_text_height) // 2))
        for box_item in self.boxes:
            box_item.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)


    def scalefactor(self, tmx_data, resolution):
        map_width = tmx_data.width * tmx_data.tilewidth
        map_height = tmx_data.height * tmx_data.tileheight
        screen_width, screen_height = resolution
        scale_factor = min(screen_width / map_width, screen_height / map_height)
        return scale_factor

    def load_tmx_map(self, filename):
        return pytmx.load_pygame(resource_path(filename))

    def render_map(self, surface, tmx_data):
        self.scale_factor = self.scalefactor(tmx_data, resolution)
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        scaled_tile = pygame.transform.scale(tile, (int(tmx_data.tilewidth * self.scale_factor), int(tmx_data.tileheight * self.scale_factor)))
                        surface.blit(scaled_tile, (x * tmx_data.tilewidth * self.scale_factor, y * tmx_data.tileheight*self.scale_factor))

    def onep_gameplay_screen_setup(self):
        for slider in self.sliders:
            slider.hide()
        for textbox in self.textboxes:
            textbox.hide()
        self.buttons = []
        self.boxes = []
        pygame.display.set_caption("Gameplay")
        self.map = self.load_tmx_map("Maps/world - copy.tmx")
        self.screen.fill(BACKGROUND)
        self.scale_factor = self.scalefactor(self.map, resolution)

        for obj in self.map.objects:
            if obj.name == 'Player':
                player_img = pygame.image.load(resource_path("images/player.webp")).convert_alpha()
                player_img = pygame.transform.scale(player_img, (30, 30))
                self.player = Player((obj.x * self.scale_factor, obj.y * self.scale_factor), player_img, self.collision, self.instadeath, self)
                self.sprites.add(self.player)


        for x, y, gid in self.map.get_layer_by_name("Main"):
            if gid != 0:
                rect_x = x * self.map.tilewidth * self.scale_factor
                rect_y = y * self.map.tileheight * self.scale_factor
                rect_width = self.map.tilewidth * self.scale_factor
                rect_height = self.map.tileheight * self.scale_factor

                self.collision.append(pygame.FRect(rect_x, rect_y, rect_width, rect_height))
                

        for x, y, gid in self.map.get_layer_by_name("INSTADEATH"):
            if gid != 0:
                rect_x = x * self.map.tilewidth * self.scale_factor
                rect_y = y * self.map.tileheight * self.scale_factor
                rect_width = self.map.tilewidth * self.scale_factor
                rect_height = self.map.tileheight * self.scale_factor

                self.instadeath.append(pygame.FRect(rect_x, rect_y, rect_width, rect_height))
        
        enemy_img = pygame.image.load(resource_path("images/enemy.webp")).convert_alpha()
        enemy_img = pygame.transform.scale(enemy_img, (30, 30))
        
        for obj in self.map.objects:
            self.object_id_list[obj.id] = obj  # Store by ID for lookup
        
            if obj.name == ("Enemy"):
                enemy = Enemy((obj.x * self.scale_factor, obj.y * self.scale_factor), enemy_img, self.collision, self.instadeath, self, self.player)
                self.sprites.add(enemy)

            if obj.name == ("Enemy2") and self.enemy_count >= 2:
                enemy2 = Enemy((obj.x * self.scale_factor, obj.y * self.scale_factor), enemy_img, self.collision, self.instadeath, self, self.player)
                self.sprites.add(enemy2)
            
            if obj.name == ("Enemy3") and self.enemy_count >= 3:
                enemy3 = Enemy((obj.x * self.scale_factor, obj.y * self.scale_factor), enemy_img, self.collision, self.instadeath, self, self.player)
                self.sprites.add(enemy3)
            
            if obj.name == ("Enemy4") and self.enemy_count >= 4:
                enemy4 = Enemy((obj.x * self.scale_factor, obj.y * self.scale_factor), enemy_img, self.collision, self.instadeath, self, self.player)
                self.sprites.add(enemy4)
            
            if obj.name == ("Enemy5") and self.enemy_count >= 5:
                enemy5 = Enemy((obj.x * self.scale_factor, obj.y * self.scale_factor), enemy_img, self.collision, self.instadeath, self, self.player)
                self.sprites.add(enemy5)
            
            if obj.name == ("Enemy6") and self.enemy_count >= 6:
                enemy6 = Enemy((obj.x * self.scale_factor, obj.y * self.scale_factor), enemy_img, self.collision, self.instadeath, self, self.player)
                self.sprites.add(enemy6)
            
            if obj.name == ("Enemy7") and self.enemy_count >= 7:
                enemy7 = Enemy((obj.x * self.scale_factor, obj.y * self.scale_factor), enemy_img, self.collision, self.instadeath, self, self.player)
                self.sprites.add(enemy7)
            
            if obj.name == ("Enemy8") and self.enemy_count >= 8:
                enemy8 = Enemy((obj.x * self.scale_factor, obj.y * self.scale_factor), enemy_img, self.collision, self.instadeath, self, self.player)
                self.sprites.add(enemy8)

            

            if hasattr(obj, 'properties') and 'teleport_target' in obj.properties:
                obj.x *= self.scale_factor
                obj.y *= self.scale_factor
                obj.width *= self.scale_factor
                obj.height *= self.scale_factor
                self.teleports.append(obj)
                print(self.teleports)



    def twop_gameplay_screen_setup(self):
        self.buttons = []
        self.boxes = []
        pygame.display.set_caption("TwoPlayerGameplay")
        self.map = self.load_tmx_map("Maps/world.tmx")
        self.screen.fill(BACKGROUND)
        self.scale_factor = self.scalefactor(self.map, resolution)

        for obj in self.map.objects:
            if obj.name == 'Player':
                player_img = pygame.image.load(resource_path("images/player.webp")).convert_alpha()
                player_img = pygame.transform.scale(player_img, (30, 30))
                self.player = Player((obj.x * self.scale_factor, obj.y * self.scale_factor), player_img, self.collision, self.instadeath, self)
                self.sprites.add(self.player)
        
        for obj in self.map.objects:
            if obj.name == 'Player2':
                player2_img = pygame.image.load(resource_path("images/old_player.webp")).convert_alpha()
                player2_img = pygame.transform.scale(player2_img, (30, 30))
                self.player2 = Player2((obj.x * self.scale_factor, obj.y * self.scale_factor), player2_img, self.collision, self.instadeath, self)
                self.sprites.add(self.player2)


        for x, y, gid in self.map.get_layer_by_name("Main"):
            if gid != 0:
                rect_x = x * self.map.tilewidth * self.scale_factor
                rect_y = y * self.map.tileheight * self.scale_factor
                rect_width = self.map.tilewidth * self.scale_factor
                rect_height = self.map.tileheight * self.scale_factor

                self.collision.append(pygame.Rect(rect_x, rect_y, rect_width, rect_height))
        
        for x, y, gid in self.map.get_layer_by_name("INSTADEATH"):
            if gid != 0:
                rect_x = x * self.map.tilewidth * self.scale_factor
                rect_y = y * self.map.tileheight * self.scale_factor
                rect_width = self.map.tilewidth * self.scale_factor
                rect_height = self.map.tileheight * self.scale_factor 

                self.instadeath.append(pygame.Rect(rect_x, rect_y, rect_width, rect_height))

        # for obj in self.map.objects:
        #     self.object_id_list[obj.id] = obj  # Store by ID for lookup

        #     if hasattr(obj, 'properties') and 'teleport_target' in obj.properties:
        #         obj.x *= self.scale_factor
        #         obj.y *= self.scale_factor
        #         obj.width *= self.scale_factor
        #         obj.height *= self.scale_factor
        #         self.teleports.append(obj)
        #         print(self.teleports)

    def draw_health_bar(self, entity, x, y, width=200, height=20, owner=""):
        # General health bar renderer for any entity
        health_ratio = entity.health / 100
        pygame.draw.rect(self.screen, RED, (x, y, width, height))  # Background
        pygame.draw.rect(self.screen, BLUE, (x, y, width * health_ratio, height))  # Health portion
        pygame.draw.rect(self.screen, BLACK, (x, y, width, height), 2)  # Outline

        if owner:
            name_text = smaller_font.render(owner, True, WHITE)
            self.screen.blit(name_text, (x, y - 30))

    def draw_xp_counter(self, player, x, y, owner=""):
        xp_text = smaller_font.render(f"XP: {player.xp}", True, WHITE)
        self.screen.blit(xp_text, (x, y))

        if owner:
            name_text = smaller_font.render(owner, True, WHITE)
            self.screen.blit(name_text, (x, y - 20))
    

    def gameplay_screen(self):
        self.screen.fill(BACKGROUND)
        self.render_map(self.screen, self.map)

        self.sprites.update()
        self.sprites.draw(self.screen)

        for player in self.sprites:
            if isinstance(player, Player) or isinstance(player, Player2) or isinstance(player, Enemy):
                player.bullets.draw(self.screen)
                player.bullets.update()
                player.bullets.draw(self.screen)
        
        # Draw Player 1 Health Bar and XP
        if self.player:
            self.draw_health_bar(self.player, 20, 60, owner="Player 1")
            self.draw_xp_counter(self.player, 20, 100, owner="Player 1")

        if self.player2:
            self.draw_health_bar(self.player2, 300, 60, owner="Player 2")  # Slightly lower on screen
            self.draw_xp_counter(self.player2, 300, 100, owner="Player 2")

        for sprite in self.sprites:
            if isinstance(sprite, Enemy):
                self.draw_health_bar(sprite, sprite.rect.x, sprite.rect.y - 15, width=30, height=7.5)

        if self.debug_switch:
            self.graph.draw(self.screen)
            for rect in self.collision:
                pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)
            for rect in self.instadeath:
                pygame.draw.rect(self.screen, (0, 0, 255), rect, 2)
            for rect in self.teleports:
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(rect.x, rect.y, rect.width, rect.height), 5)


    def end_screen(self):
        self.screen.fill(BLACK)
        pygame.display.set_caption("Game Over")

        title_text = small_title.render("GAME OVER", True, WHITE)
        self.screen.blit(title_text, ((resolution[0] - title_text.get_width()) // 2, 200))

        # Single player mode 
        if self.player2 is None:
            xp_text = smaller_font.render(f"XP Gained: {self.player.xp}", True, WHITE)
            kills_text = smaller_font.render(f"Bots Defeated: {self.player.kills}", True, WHITE)

            self.screen.blit(xp_text, ((resolution[0] - xp_text.get_width()) // 2, 400))
            self.screen.blit(kills_text, ((resolution[0] - kills_text.get_width()) // 2, 460))

        # Two player mode
        else:
            p1_kills = smaller_font.render(f"Player 1 XP: {self.player.xp}", True, WHITE)
            p2_kills = smaller_font.render(f"Player 2 XP: {self.player2.xp}", True, WHITE)

            self.screen.blit(p1_kills, ((resolution[0] - p1_kills.get_width()) // 2, 400))
            self.screen.blit(p2_kills, ((resolution[0] - p2_kills.get_width()) // 2, 460))

            # Winner Text
            if self.player.xp > self.player2.xp:
                winner_text = smaller_font.render("Player 1 Wins!", True, BLUE)
            elif self.player2.xp > self.player.xp:
                winner_text = smaller_font.render("Player 2 Wins!", True, RED)
            else:
                winner_text = smaller_font.render("DRAW!", True, WHITE)

            self.screen.blit(winner_text, ((resolution[0] - winner_text.get_width()) // 2, 520))

        # Exit + Replay buttons 
        end_button = Button("EXIT", ((resolution[0] - 100) // 2, 600), (100, 100), WHITE, BLACK)
        replay_button = Button("REPLAY", ((resolution[0] - 100) // 2 - 25, 700), (100, 100), WHITE, BLACK)

        end_button.draw(self.screen)
        replay_button.draw(self.screen)
        self.buttons = [end_button, replay_button]




    def run(self):
        screen_selector = "start"
        game_state = True
        while game_state:
            all_events = pygame.event.get()
            for event in all_events:
                if event.type == pygame.QUIT:
                    game_state = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_loc = pygame.mouse.get_pos()

                if screen_selector == "start":
                    for start_button in self.buttons:
                        if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse is clicked
                            if start_button.rect.collidepoint(mouse_loc):  # If the mouse is clicked within the button boundaries 
                                if start_button.text == "START":  # Self explanatory 
                                    screen_selector = "MAIN"
                                elif start_button.text == "EXIT":
                                    game_state = False

                if screen_selector == "MAIN":
                    for choice_button in self.buttons:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if choice_button.rect.collidepoint(mouse_loc):
                                if choice_button.text == "ONE PLAYER":
                                    screen_selector = "ONE PLAYER SETUP"
                                    print("ONE PLAYER SETUP")
                                elif choice_button.text == "TWO PLAYER":
                                    screen_selector = "TWO PLAYER"
                                    print("TWO PLAYER")

                if screen_selector == "ONE PLAYER":
                    for onep_button in self.buttons:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if onep_button.rect.collidepoint(mouse_loc):
                                if onep_button.text == "BEGIN":
                                    screen_selector = "GAMEPLAY"
                                    print("GAMEPLAY")
                
                if screen_selector == "TWO PLAYER":
                    for twop_button in self.buttons:
                        if twop_button.rect.collidepoint(mouse_loc):
                            if twop_button.text == "BEGIN":
                                screen_selector = "2PGAMEPLAY"
                                print("Two Player Mode")
                
                if screen_selector == "END":
                    for end_button in self.buttons:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if end_button.rect.collidepoint(mouse_loc):
                                if end_button.text == "EXIT":
                                    game_state = False
                            if end_button.text == "REPLAY":
                                screen_selector = "MAIN"



            if screen_selector == "start":
                self.start_screen(BLACK, WHITE, resolution)

            if screen_selector == "MAIN":
                self.choice_screen(BLACK, WHITE, resolution)

            if screen_selector == "ONE PLAYER SETUP":
                self.one_player_screen_widget_setup()
                print("ONE PLAYER")
                screen_selector = "ONE PLAYER"
            
            if screen_selector == "ONE PLAYER":
                for slider in self.sliders:
                    slider.listen(all_events)

                self.oneplayer_screen(BLACK, WHITE, resolution) 

                for slider in self.sliders:
                    for textbox in self.textboxes:
                        textbox.setText(str(int(slider.getValue())))
                    self.enemy_count = int(slider.getValue())
                    slider.draw()
                for textbox in self.textboxes:
                    textbox.draw()

            
            if screen_selector == "TWO PLAYER":
                self.twoplayer_screen(BLACK, WHITE, resolution)

            if screen_selector == "GAMEPLAY":
                self.sprites.empty()  # Clear old sprites
                self.onep_gameplay_screen_setup()
                screen_selector = "GAMEPLAY LOOP"

            if screen_selector == "2PGAMEPLAY":
                self.sprites.empty()  # Clear old sprites
                self.twop_gameplay_screen_setup()
                screen_selector = "GAMEPLAY LOOP"

            if screen_selector == "GAMEPLAY LOOP":
                self.gameplay_screen()
                if self.player2:
                    if self.player.lives <= 0 or self.player2.lives <= 0:
                        screen_selector = "END"
                else:
                    enemies_remaining = False
                    for sprite in self.sprites:
                        if isinstance(sprite, Enemy):
                            enemies_remaining = True
                            break  # No need to keep checking once we’ve found one

                    # Check if all enemies are defeated or the player has no lives left

                    if not enemies_remaining or self.player.lives <= 0:
                        screen_selector = "END"

                    
            if screen_selector == "END":
                self.end_screen()


         
            pygame_widgets.update(all_events) # Update the widgets
            pygame.display.update()
            self.clock.tick(FRAMERATE)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    superfighters = Game()
    superfighters.run()






