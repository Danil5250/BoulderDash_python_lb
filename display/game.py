import pygame
import keyboard
import sys
from Core.managers.MainManager import MainManager
from display.config.DisplayConfig import DisplayConfig


class Game:
    __slots__ = ["is_running", "main_manager"]
    def __init__(self):
        self.is_running = True
        self.main_manager = MainManager()

    def start_menu(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("BoulderDash - Menu")
        font = pygame.font.SysFont("arial", 24)

        while True:
            screen.fill((30, 30, 30))
            title = font.render("BoulderDash", True, (255, 255, 0))
            start_text = font.render("1 - Start game in random map", True, (255, 255, 255))
            exit_text = font.render("0 - Exit", True, (255, 255, 255))

            screen.blit(title, (120, 50))
            screen.blit(start_text, (100, 150))
            screen.blit(exit_text, (100, 190))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_1:
                        pygame.quit()
                        self.start_game()
                        return

    def start_game(self):
        pygame.init()
        screen = pygame.display.set_mode((DisplayConfig.WIDTH, DisplayConfig.HEIGHT))
        pygame.display.set_caption("BoulderDash - Game")

        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 0))
            self.draw_field(screen)
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()

    def draw_field(self, screen):
        screen.fill((0, 0, 0))

        field_width = self.main_manager.field_width
        field_height = self.main_manager.field_height
        field = self.main_manager.field

        cell_width = screen.get_width() / field_width
        cell_height = screen.get_height() / field_height
        cell_size = min(cell_width, cell_height)

        font = pygame.font.SysFont("consolas", int(cell_size * 0.8))

        for y in range(field_height):
            for x in range(field_width):
                cell = field[y][x]
                color = cell.foreground
                symbol = str(cell.view)

                rect = pygame.Rect(
                    x * cell_size,
                    y * cell_size,
                    cell_size,
                    cell_size
                )

                # рисуем ячейку
                pygame.draw.rect(screen, color, rect)

                # рисуем границу (опционально)
                pygame.draw.rect(screen, (40, 40, 40), rect, 1)

                # текст (символ)
                text_surface = font.render(symbol, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

        pygame.display.flip()
