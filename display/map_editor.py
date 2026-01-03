import pygame
import sys
import os
from display.config.DisplayConfig import DisplayConfig
from display.config.ui.Button import Button
from Core.game_objects.environment.harmful.Stone import Stone
from Core.game_objects.environment.useful.Diamond import Diamond
from Core.game_objects.characters.Player import Player
from Core.game_objects.characters.Enemy import Enemy
from Core.game_objects.environment.neutral.Sand import Sand
from Core.game_objects.environment.neutral.Emptiness import Emptiness
from Core.managers.MainManager import MainManager
from Core.utils.FieldUtils import FieldUtils

class MapEditor:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.width = 20
        self.height = 15
        self.field = self._init_empty_field(self.width, self.height)
        self.selected_element = Emptiness
        self.running = True

        
        self.GRID_OFFSET_X = 20
        self.GRID_OFFSET_Y = 20
        self.CELL_SIZE = 30
        self.PANEL_WIDTH = 250
        
        self.elements = [
            ("Stone", Stone, (100, 100, 100)),
            ("Diamond", Diamond, (0, 255, 255)),
            ("Player", Player, (0, 255, 0)),
            ("Enemy", Enemy, (255, 0, 0)),
            ("Sand", Sand, (194, 178, 128)),
            ("Emptiness", Emptiness, (0, 0, 0))
        ]
        
        self.buttons = []
        self._init_ui()

    def _init_empty_field(self, w, h):
        return [[Emptiness() for _ in range(w)] for _ in range(h)]

    def _init_ui(self):
        self.buttons = []
        
        def inc_w():
            self.width += 1
            self.field = self._resize_field()
        def dec_w():
            if self.width > 5:
                self.width -= 1
                self.field = self._resize_field()
        def inc_h():
            self.height += 1
            self.field = self._resize_field()
        def dec_h():
            if self.height > 5:
                self.height -= 1
                self.field = self._resize_field()
                
        def make_select_callback(elem_cls):
            return lambda: self._select_element(elem_cls)

        start_y = 20
        x_pos = DisplayConfig.WIDTH - self.PANEL_WIDTH + 20
        
        self.buttons.append(Button(x_pos, start_y, 30, 30, "-", dec_w))
        self.buttons.append(Button(x_pos + 120, start_y, 30, 30, "+", inc_w))
        
        self.buttons.append(Button(x_pos, start_y + 40, 30, 30, "-", dec_h))
        self.buttons.append(Button(x_pos + 120, start_y + 40, 30, 30, "+", inc_h))
        
        pal_y = start_y + 80
        for name, cls, color in self.elements:
            btn = Button(x_pos, pal_y, 100, 30, name, make_select_callback(cls))
            self.buttons.append(btn)
            pal_y += 40
            
        self.buttons.append(Button(x_pos, pal_y + 5, 120, 30, "Fill Sand", self.fill_sand))
        self.buttons.append(Button(x_pos, pal_y + 50, 120, 30, "Fill Empty", self.clear_field))
        
        self.buttons.append(Button(x_pos, DisplayConfig.HEIGHT - 120, 100, 40, "Play Map", self.play_map))
        self.buttons.append(Button(x_pos+110, DisplayConfig.HEIGHT - 120, 100, 40, "Save Map", self.save_map))
        self.buttons.append(Button(x_pos, DisplayConfig.HEIGHT - 60, 120, 40, "Exit", self.exit_editor))

    def _select_element(self, elem_cls):
        self.selected_element = elem_cls

    def _resize_field(self):
        new_field = [[Emptiness() for _ in range(self.width)] for _ in range(self.height)]
        old_h = len(self.field)
        old_w = len(self.field[0]) if old_h > 0 else 0
        
        for y in range(min(self.height, old_h)):
            for x in range(min(self.width, old_w)):
                new_field[y][x] = self.field[y][x]
        return new_field

    def fill_sand(self):
        for y in range(self.height):
            for x in range(self.width):
                if isinstance(self.field[y][x], Emptiness):
                    self.field[y][x] = Sand()
                    
    def clear_field(self):
        for y in range(self.height):
            for x in range(self.width):
                self.field[y][x] = Emptiness()

    def validate_map(self):
        player_count = 0
        enemy_count = 0
        diamond_count = 0
        
        for y in range(self.height):
            for x in range(self.width):
                obj = self.field[y][x]
                if isinstance(obj, Player):
                    player_count += 1
                elif isinstance(obj, Enemy):
                    enemy_count += 1
                elif isinstance(obj, Diamond):
                    diamond_count += 1
                    
        if player_count != 1:
            return "Error: Map must have exactly one player."
        if enemy_count > 1:
            return "Error: Map must have zero or one enemy."
        if diamond_count < 1:
            return "Error: Map must have at least one diamond."
            
        return None

    def play_map(self):
        error = self.validate_map()
        if error:
            print(error)
            return

        # Start game directly with current field
        self.game_instance.start_game_with_map(self.field, self.width, self.height)
        self.running = False
        
    def save_map(self):
        filename = self.get_next_filename()
        FieldUtils.save_field_to_file(self.field, self.width, self.height, filename)
        print(f"Map saved to {filename}")
    
    def get_next_filename(self):
        base_dir = "maps"
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            
        i = 1
        while True:
            filename = os.path.join(base_dir, f"custom_map_{i}.json")
            if not os.path.exists(filename):
                return filename
            i += 1

    def exit_editor(self):
        self.running = False
        self.game_instance.start_menu()

    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        avail_w = DisplayConfig.WIDTH - self.PANEL_WIDTH - 40
        avail_h = DisplayConfig.HEIGHT - 40
        
        scaled_cell_size = min(avail_w // self.width, avail_h // self.height)
        scaled_cell_size = max(10, min(scaled_cell_size, 40)) # Clamp
        
        self.CELL_SIZE = scaled_cell_size
        
        if mouse_pressed[0]:
            mx, my = mouse_pos
            gx = (mx - self.GRID_OFFSET_X) // self.CELL_SIZE
            gy = (my - self.GRID_OFFSET_Y) // self.CELL_SIZE
            
            if 0 <= gx < self.width and 0 <= gy < self.height:
                if self.selected_element == Player:
                    # Remove other players
                    for Y in range(self.height):
                        for X in range(self.width):
                             if isinstance(self.field[Y][X], Player):
                                 self.field[Y][X] = Emptiness()
                
                if self.selected_element == Enemy:
                    # Remove other enemies
                    for Y in range(self.height):
                        for X in range(self.width):
                             if isinstance(self.field[Y][X], Enemy):
                                 self.field[Y][X] = Emptiness()
                                 
                if self.selected_element == Enemy:
                    self.field[gy][gx] = self.selected_element(gx, gy)
                else:
                    self.field[gy][gx] = self.selected_element()
                
    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((DisplayConfig.WIDTH, DisplayConfig.HEIGHT))
        pygame.display.set_caption("BoulderDash - Map Editor")
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("arial", 18)
        
        while self.running:
            screen.fill((30, 30, 30))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                for btn in self.buttons:
                    btn.handle_event(event)
            
            self.handle_input()
            
            for y in range(self.height):
                for x in range(self.width):
                    rect = pygame.Rect(
                        self.GRID_OFFSET_X + x * self.CELL_SIZE,
                        self.GRID_OFFSET_Y + y * self.CELL_SIZE,
                        self.CELL_SIZE,
                        self.CELL_SIZE
                    )
                    cell = self.field[y][x]
                    
                    pygame.draw.rect(screen, (10, 10, 10), rect)
                    pygame.draw.rect(screen, (50, 50, 50), rect, 1)
                    
                    if not isinstance(cell, Emptiness):
                        color = cell.foreground if hasattr(cell, 'foreground') else (255,255,255)
                        view = cell.view if hasattr(cell, 'view') else "?"
                        
                        pygame.draw.rect(screen, color, rect.inflate(-4, -4))
                        
            ui_x = DisplayConfig.WIDTH - self.PANEL_WIDTH
            pygame.draw.rect(screen, (50, 50, 50), (ui_x, 0, self.PANEL_WIDTH, DisplayConfig.HEIGHT))
            
            screen.blit(font.render(f"Width: {self.width}", True, (255,255,255)), (ui_x + 60, 20))
            screen.blit(font.render(f"Height: {self.height}", True, (255,255,255)), (ui_x + 60, 60))
            
            screen.blit(font.render(f"Selected: {self.selected_element.__name__}", True, (255,255,0)), (ui_x + 20, DisplayConfig.HEIGHT - 150))
            
            err = self.validate_map()
            if err:
                 err_surf = font.render("Invalid Map!", True, (255, 0, 0))
                 screen.blit(err_surf, (ui_x + 20, DisplayConfig.HEIGHT - 170))
            else:
                 ok_surf = font.render("Map Valid", True, (0, 255, 0))
                 screen.blit(ok_surf, (ui_x + 20, DisplayConfig.HEIGHT - 170))

            for btn in self.buttons:
                btn.draw(screen, font)
                
            pygame.display.flip()
            clock.tick(30)
        
