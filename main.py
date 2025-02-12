import pygame
import sys
pygame.init()  # Simply initialises pygame and all its modules
pygame.font.init()  # Initialise the fonts I want to use
from classes import *  # Imported the classes from the classes.py file
import pytmx

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (127, 255, 212)
BACKGROUND = '#fcdfcd'

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

    def load_tmx_map(self, filename):
        return pytmx.load_pygame(filename)

    def render_map(self, surface, tmx_data, resolution):
        map_width = tmx_data.width * tmx_data.tilewidth
        map_height = tmx_data.height * tmx_data.tileheight
        screen_width, screen_height = resolution
        scale_factor = min(screen_width / map_width, screen_height / map_height)

        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        scaled_tile = pygame.transform.scale(tile, (int(tmx_data.tilewidth * scale_factor), int(tmx_data.tileheight * scale_factor)))
                        surface.blit(scaled_tile, (x * tmx_data.tilewidth * scale_factor, y * tmx_data.tileheight*scale_factor))

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

    def scaling_objects(self, objects, scale):
        for obj in objects:
            obj = {
                'name': obj.name,
                'x': obj.x * scale,
                'y': obj.y * scale,
                'width': obj.width * scale,
                'height': obj.height * scale
                }
                
        map_width = self.map.width * self.map.tilewidth
        map_height = self.map.height * self.map.tileheight
        scale_factor = min(resolution[0] / map_width, resolution[1] / map_height)

    def gameplay_screen_setup(self):
        self.buttons = []
        self.boxes = []
        pygame.display.set_caption("Gameplay")
        self.map = self.load_tmx_map("./Maps/world.tmx")
        self.screen.fill(WHITE)
        self.level_width = self.map.width * 64
        self.level_height = self.map.height * 64

        # for layer in self.map.visible_layers:
        #     if isinstance(layer, pytmx.TiledTileLayer):
        #         for x, y, gid in layer:
        #             tile = self.map.get_tile_image_by_gid(gid)
        #             if tile:
        #                 self.surface.blit(tile, (x * self.map.tilewidth, y * self.map.tileheight))

        # for layer in self.map.visible_layers:
        #     if isinstance(layer, pytmx.TiledTileLayer):
        #         for x, y, gid in layer:
        #             tile = self.map.get_tile_image_by_gid(gid)
        #             if tile:
        #                 sprite = object((x * self.map.tilewidth, y * self.map.tileheight), tile, (self.sprites))
        #                 if layer.name == "Main":
        #                     self.sprites.add(sprite)
        #                     self.collision.add(sprite)
        #                 if layer.name == "Decoration":
        #                     self.sprites.add(sprite)
        #                 if layer.name == "Entities":
        #                     self.sprites.add(sprite)
        #                     self.collision.add(sprite)
        #                     player_img = pygame.image.load("./images/player.webp").convert_alpha()
        #                     player_img = pygame.transform.scale(player_img, (50, 50))
        #                     self.player = Player((x, y), player_img, (self.sprites, self.collision), self.collision)
                            

        # for obj in self.map.objects:
        #     if obj.name == "Player":
        #         player_img = pygame.image.load("./images/player.webp").convert_alpha()
        #         player_img = pygame.transform.scale(player_img, (50, 50))
        #         self.player = Player((obj.x, obj.y), player_img, (self.sprites,), self.collision)
        #         self.sprites.add(self.player)

        for obj in self.map.objects:
            if obj.name == 'Instant Death':
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.instadeath.append(rect)

        # for x,y, image in self.map.get_layer_by_name('Main').tiles():
        #     object((x * 64,y * 64), image, (self.sprites))

        for obj in self.map.objects:
            if obj.name == 'Collisions':
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.collision.append(rect)
        
        # for x, y, image in self.map.get_layer_by_name('Decoration').tiles():
        #     object((x * 64,y * 64), image, (self.sprites))

        for obj in self.map.objects:

            if obj.name == 'Player':
                player_img = pygame.image.load("./images/player.webp").convert_alpha()
                player_img = pygame.transform.scale(player_img, (50, 50))
                Player((obj.x, obj.y), player_img, (self.sprites), self.collision)
        
    def gameplay_screen(self,dt):
        self.screen.fill(BACKGROUND)
        self.render_map(self.screen, self.map, resolution)
        self.sprites.update(dt)
        self.sprites.draw(self.screen)



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
                    
            if screen_selector == "start":
                self.start_screen(BLACK, WHITE, resolution)

            if screen_selector == "MAIN":
                self.choice_screen(BLACK, WHITE, resolution)
            
            if screen_selector == "ONE PLAYER":
                self.oneplayer_screen(BLACK, WHITE, resolution)

            if screen_selector == "GAMEPLAY":
                self.gameplay_screen_setup()
                screen_selector = "GAMEPLAY LOOP"

            if screen_selector == "GAMEPLAY LOOP":
                self.gameplay_screen(self.clock.tick(100) / 1000)


            pygame.display.update()
            self.clock.tick(100)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    superfighters = Game()
    superfighters.run()
