from Core.game_objects.base.GameEntity import GameEntity
from Core.config.base.GameConfig import GameConfig
from Core.game_objects.characters.Enemy import Enemy
from Core.game_objects.characters.Player import Player
from Core.game_objects.environment.neutral.Emptiness import Emptiness
from Core.game_objects.environment.neutral.Sand import Sand
from Core.game_objects.environment.harmful.Stone import Stone
from Core.game_objects.environment.useful.Diamond import Diamond
from Core.managers.GameStateManager import GameStateManager

class Bomb(GameEntity):
    
    def __init__(self):
        super().__init__("B", (255, 0, 0))
        self.timer = 150 # 5 seconds * 30 FPS
        self.is_exploded = False

    def can_stone_move_here(self):
        return False

    def can_stone_fall_here(self):
        return False
    
    def can_player_move_on(self):
        return False

    def tick(self):
        if self.timer > 0:
            self.timer -= 1
            return False
        else:
            self.is_exploded = True
            return True

    def explode(self, field, field_width, field_height, bomb_x, bomb_y, main_manager):
        radius = 2
        game_over = False
        
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if abs(dx) + abs(dy) <= radius:
                    ny, nx = bomb_y + dy, bomb_x + dx
                    
                    if 0 <= ny < field_height and 0 <= nx < field_width:
                        entity = field[ny][nx]
                        
                        if isinstance(entity, Diamond):
                            game_over = True
                        elif isinstance(entity, (Stone, Sand, Bomb)): 
                            field[ny][nx] = Emptiness()
                        elif isinstance(entity, Player):
                            entity.decrease_lives()

        if game_over:
             main_manager.is_game_win = False
