from Core.input.input_manager import InputManager
from display.config.ui.Button import Button
import pygame
import sys
from Core.managers.MainManager import MainManager
from display.config.DisplayConfig import DisplayConfig


class Game:
    __slots__ = ["is_running", "main_manager", "input_manager"]
    def __init__(self):
        self.is_running = True
        

    def start_menu(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("BoulderDash - Menu")
        font = pygame.font.SysFont("arial", 24)
        
        
        def start_game():
            pygame.quit()
            self.start_game()

        def exit_game():
            pygame.quit()
            sys.exit()

        def load_map_action():
            import tkinter as tk
            from tkinter import filedialog
            
            root = tk.Tk()
            root.withdraw()
            filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            root.destroy()
            
            if filename:
                pygame.quit()
                self.start_game_from_file(filename)

        start_button = Button(100, 140, 200, 40, "Start game", start_game)
        
        def open_editor():
            from display.map_editor import MapEditor
            editor = MapEditor(self)
            editor.run()
            self.start_menu()

        create_map_button = Button(100, 190, 200, 40, "Create Map", open_editor)
        load_map_button = Button(100, 240, 200, 40, "Play in my field", load_map_action)
        exit_button = Button(100, 290, 200, 40, "Exit", exit_game)

        while self.is_running:
            screen.fill((30, 30, 30))
            title = font.render("BoulderDash", True, (255, 255, 0))
            screen.blit(title, (120, 50))

            start_button.draw(screen, font)
            create_map_button.draw(screen, font)
            load_map_button.draw(screen, font)
            exit_button.draw(screen, font)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                start_button.handle_event(event)
                create_map_button.handle_event(event)
                load_map_button.handle_event(event)
                exit_button.handle_event(event)

    def pause_game(self):
        self.main_manager.is_paused = True

    def resume_game(self):
        self.main_manager.is_paused = False

    def start_game_from_file(self, filename):
        from Core.utils.FieldUtils import FieldUtils
        field, width, height = FieldUtils.load_field_from_file(filename)
        
        if field is None:
            print(f"Failed to load map from {filename}")
            return

        self.start_game_with_map(field, width, height)

    def start_game_with_map(self, field, width, height):
        self.main_manager = MainManager(field_width=width, field_height=height, custom_field=field)
        self.input_manager = InputManager()
        pygame.init()
        screen = pygame.display.set_mode((DisplayConfig.WIDTH, DisplayConfig.HEIGHT))
        pygame.display.set_caption("BoulderDash - Custom Game")

        self.run_game_loop(screen)

    def run_game_loop(self, screen):
        pause_button = Button(DisplayConfig.WIDTH - 230,
                              DisplayConfig.HEIGHT - 60,
                              100,
                              40,
                              "Pause",
                              self.pause_game)
        resume_button = Button(DisplayConfig.WIDTH - 110, DisplayConfig.HEIGHT - 60, 100, 40, "Resume", self.resume_game)

        clock = pygame.time.Clock()
        running = True

        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                
                pause_button.handle_event(event)
                resume_button.handle_event(event)

            actions = self.input_manager.get_actions(events)
            for action in actions:
                self.main_manager.apply_action(action)                                  
            
            self.main_manager.update_field_state()
            
            if self.main_manager.is_game_win is not None:
                running = self.show_game_end_screen(screen, self.main_manager.is_game_win)
            else:
                self.draw_field(screen, pause_button, resume_button)
                
            clock.tick(30)
        
        pygame.quit()
        self.start_menu()

    def start_game(self):
        self.main_manager = MainManager()
        self.input_manager = InputManager()
        pygame.init()
        screen = pygame.display.set_mode((DisplayConfig.WIDTH, DisplayConfig.HEIGHT))
        pygame.display.set_caption("BoulderDash - Game")
        
        self.run_game_loop(screen)

    def show_game_end_screen(self, screen, is_win):
        self.draw_field(screen)
        
        overlay = pygame.Surface((DisplayConfig.WIDTH, DisplayConfig.HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        title_font = pygame.font.SysFont("arial", 48, bold=True)
        message_font = pygame.font.SysFont("arial", 24)
        
        if is_win:
            title_text = "VICTORY!"
            title_color = (0, 255, 0)
            message_text = f"You collected all {self.main_manager._diamonds_count} diamonds!"
        else:
            title_text = "GAME OVER"
            title_color = (255, 0, 0)
            message_text = ""
        
        title_surface = title_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(DisplayConfig.WIDTH // 2, DisplayConfig.HEIGHT // 2 - 60))
        screen.blit(title_surface, title_rect)
        
        message_surface = message_font.render(message_text, True, (255, 255, 255))
        message_rect = message_surface.get_rect(center=(DisplayConfig.WIDTH // 2, DisplayConfig.HEIGHT // 2 - 10))
        screen.blit(message_surface, message_rect)
        
        should_return = [False]
        
        return_button = Button(
            DisplayConfig.WIDTH // 2 - 100,
            DisplayConfig.HEIGHT // 2 + 50,
            200,
            50,
            "Return to Menu",
            lambda: should_return.__setitem__(0, True)
        )
        
        button_font = pygame.font.SysFont("arial", 20)
        return_button.draw(screen, button_font)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                return_button.handle_event(event)
                
                if should_return[0]:
                    return False
        
        return False



    def draw_field(self, screen, pause_button=None, resume_button=None):
        screen.fill((20, 20, 20))

        field_width = self.main_manager.field_width
        field_height = self.main_manager.field_height
        field = self.main_manager.field

        avail_width = screen.get_width()
        avail_height = screen.get_height() - DisplayConfig.UI_PANEL_HEIGHT
        cell_size = min(avail_width / field_width, avail_height / field_height)

        offset_x = (avail_width - field_width * cell_size) / 2
        offset_y = (avail_height - field_height * cell_size) / 2

        font = pygame.font.SysFont("consolas", int(cell_size * 0.8))

        for y in range(field_height):
            for x in range(field_width):
                cell = field[y][x]
                color = cell.foreground
                symbol = str(cell.view)

                rect = pygame.Rect(
                    offset_x + x * cell_size,
                    offset_y + y * cell_size,
                    cell_size,
                    cell_size
                )

                pygame.draw.rect(screen, color, rect)

                pygame.draw.rect(screen, (40, 40, 40), rect, 1)

                text_surface = font.render(symbol, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

        panel_rect = pygame.Rect(
            0,
            avail_height,
            screen.get_width(),
            DisplayConfig.UI_PANEL_HEIGHT
        )
        
        pygame.draw.rect(screen, (30, 30, 30), panel_rect)
        pygame.draw.rect(screen, (80, 80, 80), panel_rect, 2)
        
        ui_font = pygame.font.SysFont("arial", 24)
        lives_text = ui_font.render(f"Lives: {self.main_manager.player.lives}", True, (255, 255, 0))
        score_text = ui_font.render(f"Score: {self.main_manager.player.score}", True, (255, 255, 0))
        stones_text = ui_font.render(f"Stones: {self.main_manager.player.current_stone_moves}/{self.main_manager.player.max_stone_moves}", True, (255, 255, 0))
        jumps_text = ui_font.render(f"Jumps: {self.main_manager.player.current_player_jumps}/{self.main_manager.player.max_player_jumps}", True, (255, 255, 0))
        bomb_text = ui_font.render(f"Bombs: {self.main_manager.player.current_count_bombs}", True, (255, 255, 0))
        
        screen.blit(lives_text, (20, avail_height + DisplayConfig.UI_PANEL_HEIGHT // 2 - lives_text.get_height() // 2))
        screen.blit(score_text, (lives_text.get_width() + 50, avail_height + DisplayConfig.UI_PANEL_HEIGHT // 2 - score_text.get_height() // 2))
        screen.blit(stones_text, (lives_text.get_width() + score_text.get_width() + 80, avail_height + DisplayConfig.UI_PANEL_HEIGHT // 2 - stones_text.get_height() // 2))
        screen.blit(jumps_text, (lives_text.get_width() + score_text.get_width() + stones_text.get_width() + 110, avail_height + DisplayConfig.UI_PANEL_HEIGHT // 2 - jumps_text.get_height() // 2))
        screen.blit(bomb_text, (jumps_text.get_width() + lives_text.get_width() + score_text.get_width() + stones_text.get_width() + 140, avail_height + DisplayConfig.UI_PANEL_HEIGHT // 2 - jumps_text.get_height() // 2))

        if pause_button and resume_button:
            button_font = pygame.font.SysFont("arial", 18)
            
            pause_button.draw(screen, button_font)
            resume_button.draw(screen, button_font)

        pygame.display.flip()
