from settings import *
from new_classes import *
import sys
import pygame
import pytmx

pygame.init()
pygame.font.init()

icon = pygame.image.load("./images/icon.png")  # Loads the image "icon.png" into the variable "icon"
icon = pygame.transform.scale(icon, (500, 500))
display_list = pygame.display.get_desktop_sizes()  # Obtains resolutions of all the displays
resolution = display_list[0]
font = pygame.font.SysFont("Arial", 260, True)  # Added the titlefont
small_title = pygame.font.SysFont("Arial", 100, True)
timer_font = pygame.font.Font(None, 36)

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
        self.sprites = pygame.sprite.Group()
        self.collision = []
        self.instadeath = []
        self.scale_factor = 1

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

    def choice_screen(self, screen_colour, title_colour, resolution):
        self.buttons = []
        self.boxes = []
        one_player = Button("ONE PLAYER", ((resolution[0] - 100) // 7, (resolution[1] // 2)), (100, 100), WHITE)
        two_player = Button("TWO PLAYER", ((resolution[0] - 100) // 7, (resolution[1] // 2) + 100), (100, 100), WHITE)
        tutorial = Button("TUTORIAL", ((resolution[0] - 100) // 7, (resolution[1] // 2) + 200), (100, 100), WHITE)
        setup = Button("SETUP", ((resolution[0] - 100) // 7, (resolution[1] // 2) + 300), (100, 100), WHITE)
        self.buttons += [one_player, two_player, tutorial, setup]

        pygame.display.set_caption("Game Modes")
        self.screen.fill(screen_colour)
        title_text = font.render("SUPERFIGHTERS", True, title_colour)
        main_text_width = title_text.get_width()
        main_text_height = title_text.get_height()

        self.screen.blit(title_text, (resolution[0] // 2 - main_text_width // 2, (resolution[1] - 400) // 2 - main_text_height // 2))
        for button in self.buttons:
            button.draw(self.screen)

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
        return pytmx.load_pygame(filename)

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
        self.buttons = []
        self.boxes = []
        pygame.display.set_caption("Gameplay")
        self.map = self.load_tmx_map("./Maps/world.tmx")
        self.screen.fill(BACKGROUND)
        self.scale_factor = self.scalefactor(self.map, resolution)

        for obj in self.map.objects:
            if obj.name == 'Player':
                player_img = pygame.image.load("./images/player.webp").convert_alpha()
                player_img = pygame.transform.scale(player_img, (40, 40))
                self.player = Player((obj.x * self.scale_factor, obj.y * self.scale_factor), player_img, self.collision, self.instadeath, self)
                self.sprites.add(self.player)


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

        for obj in self.map.objects:
            if obj.name == ("Enemy"):
                enemy_img = pygame.image.load("./images/enemy.webp").convert_alpha()
                enemy_img = pygame.transform.scale(enemy_img, (40, 40))
                enemy = Enemy((obj.x * self.scale_factor, obj.y * self.scale_factor), enemy_img, self.collision, self.instadeath, self, self.player)
                self.sprites.add(enemy)


    def twop_gameplay_screen_setup(self):
        self.buttons = []
        self.boxes = []
        pygame.display.set_caption("TwoPlayerGameplay")
        self.map = self.load_tmx_map("./Maps/world.tmx")
        self.screen.fill(BACKGROUND)
        self.scale_factor = self.scalefactor(self.map, resolution)

        for obj in self.map.objects:
            if obj.name == 'Player':
                player_img = pygame.image.load("./images/player.webp").convert_alpha()
                player_img = pygame.transform.scale(player_img, (40, 40))
                self.player = Player((obj.x * self.scale_factor, obj.y * self.scale_factor), player_img, self.collision, self.instadeath, self)
                self.sprites.add(self.player)
        
        for obj in self.map.objects:
            if obj.name == 'Player2':
                player2_img = pygame.image.load("./images/old_player.webp").convert_alpha()
                player2_img = pygame.transform.scale(player2_img, (40, 40))
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


        for rect in self.collision:
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)
        for rect in self.instadeath:
            pygame.draw.rect(self.screen, (0, 0, 255), rect, 2)

    def run(self):
        screen_selector = "start"
        game_state = True
        while game_state:
            for event in pygame.event.get():
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
                                    screen_selector = "ONE PLAYER"
                                    print("ONE PLAYER")
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



            if screen_selector == "start":
                self.start_screen(BLACK, WHITE, resolution)

            if screen_selector == "MAIN":
                self.choice_screen(BLACK, WHITE, resolution)

            if screen_selector == "ONE PLAYER":
                self.oneplayer_screen(BLACK, WHITE, resolution)
            
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


            pygame.display.update()
            self.clock.tick(FRAMERATE)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    superfighters = Game()
    superfighters.run()






