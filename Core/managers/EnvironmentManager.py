from Core.game_objects.characters.Player import Player
from Core.game_objects.environment.harmful.Stone import Stone
from Core.game_objects.environment.harmful.Bomb import Bomb
from Core.game_objects.environment.neutral.Emptiness import Emptiness

from Core.game_objects.characters.Enemy import Enemy
from Core.game_objects.environment.useful.Diamond import Diamond
from Core.utils.FieldUtils import FieldUtils

class EnvironmentManager:
    
    @staticmethod
    def update_stones(field, field_width, field_height, player):
        for y in range(field_height - 2, -1, -1):
            for x in range(field_width):
                entity = field[y][x]

                if isinstance(entity, Stone):
                    is_falling = EnvironmentManager.process_stone_falling(field, player, y, x, entity)
                    if not is_falling:
                        EnvironmentManager.reset_stone(entity)

    @staticmethod
    def process_stone_falling(field, player, y, x, entity):
        
        if field[y + 1][x].can_stone_fall_here():
            if not entity.is_falling:
                entity.is_falling = True
                entity.fall_timer = entity.fall_delay
                return True
            
            entity.fall_timer -= 1

            if entity.fall_timer <= 0:                                
                if player.coordinates.x == x and player.coordinates.y == (y + 2):
                    player.decrease_lives()
                else:
                    field[y + 1][x] = entity
                field[y][x] = Emptiness()
                # make stone fall slower than it falls immidiately
                return False
            
            return True
        
        return False
    
    @staticmethod
    def update_bombs(field, field_width, field_height, main_manager):
        for y in range(field_height):
            for x in range(field_width):
                entity = field[y][x]
                if isinstance(entity, Bomb):
                    if entity.tick():
                        entity.explode(field, field_width, field_height, x, y, main_manager)
    
    @staticmethod
    def reset_stone(stone):
        stone.is_falling = False
        stone.fall_timer = 0

    @staticmethod
    def update_enemies(field, field_width, field_height, player, regenerate_enemy):
        
        map_ = FieldUtils.field_to_boolean_field(field, field_height, field_width)
        
        diamonds_destroyed = 0
        
        # Identify enemies first to avoid double updating if they move down/right
        enemy = None
        for y in range(field_height):
            for x in range(field_width):
                if isinstance(field[y][x], Enemy):
                    enemy = field[y][x]
            
        # Find enemy on field (to be safe and get current coords)
        cx, cy = -1, -1
        for y in range(field_height):
            for x in range(field_width):
                if field[y][x] == enemy:
                    cx, cy = x, y
                    break # Перериває внутрішній цикл
            #if cx != -1: break
            else:
                continue # Виконується ТІЛЬКИ якщо внутрішній цикл НЕ було перервано (ворога не знайдено в цьому рядку)
            break # Перериває зовнішній цикл, якщо ворога знайдено
        
        if cx == -1: return # Enemy not found on field
        
        enemy.update(map_, player.coordinates.x, player.coordinates.y)
        
        # check where it wants to go
        nx, ny = enemy.position.x, enemy.position.y
        
        if nx != cx or ny != cy:
            # Attempt move
            if 0 <= ny < field_height and 0 <= nx < field_width:
                 # Check if target is walkable (since A* said it's walkable)
                 if field[ny][nx].can_enemy_move_on():
                    if isinstance(field[ny][nx], Player):
                        player.decrease_lives()
                        enemy.decrease_lives(regenerate_enemy)
                        if enemy.lives <= 0:
                             field[cy][cx] = Emptiness()
                    else:
                        if isinstance(field[ny][nx], Diamond):
                            diamonds_destroyed += 1
                        field[ny][nx] = enemy
                        field[cy][cx] = Emptiness()
                 else:
                     # Revert internal position
                     enemy.position.x = cx
                     enemy.position.y = cy
        return diamonds_destroyed
