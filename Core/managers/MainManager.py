from Core.config.base.GameConfig import GameConfig
from Core.game_objects.characters.Player import Player
from Core.game_objects.characters.Enemy import Enemy
from Core.game_objects.environment.harmful.Stone import Stone
from Core.game_objects.environment.neutral.Emptiness import Emptiness
from Core.game_objects.environment.neutral.Sand import Sand
from Core.game_objects.environment.useful.Diamond import Diamond
from Core.game_objects.environment.harmful.Bomb import Bomb
import random
from Core.managers.GameStateManager import GameStateManager
from Core.managers.EnvironmentManager import EnvironmentManager
from Core.utils.Coordinates import Coordinates
from Core.utils.FieldUtils import FieldUtils
from Core.actions import ActionType

class MainManager:
    __slots__ = ['_field', '_field_width', '_field_height', '_diamonds_count', 'player',
                 'is_paused', 'is_game_win', 'game_tick', 'enemy_generation_success',
                 '_is_custom_map'
                 ]

    def __init__(self, field_width=GameConfig.FIELD_WIDTH, field_height=GameConfig.FIELD_HEIGHT, custom_field=None):
        self._field_width = field_width
        self._field_height = field_height
        self._diamonds_count = -1
        
        self.player = Player()
        self.is_paused = False
        self.is_game_win = None
        self.game_tick = 0
        self.enemy_generation_success = False

        if custom_field:
            self._field = custom_field
            self._is_custom_map = True
            self.init_from_custom_field()
        else:
            self._field = FieldUtils.init_field(self._field_height, self._field_width)
            self._is_custom_map = False
            self.init_field_randomly()
    
    def init_from_custom_field(self):
        # Scan field to set player coordinates and count diamonds
        self._diamonds_count = 0
        player_found = False
        
        for y in range(self._field_height):
            for x in range(self._field_width):
                obj = self._field[y][x]
                if isinstance(obj, Player):
                    if not player_found:
                        self.player = obj
                        self.player.coordinates = Coordinates(x, y)
                        player_found = True
                    else:
                        self._field[y][x] = Emptiness()
                elif isinstance(obj, Diamond):
                    self._diamonds_count += 1
                elif isinstance(obj, Enemy):
                    obj.position.x = x
                    obj.position.y = y
                    obj.previous_position.x = x
                    obj.previous_position.y = y
                    self.enemy_generation_success = True
    
    def init_field_randomly(self):
        self.__generate_environment_in_field(GameConfig.STONE_DENSITY, Stone)
        self._diamonds_count = self.__generate_environment_in_field(GameConfig.STONE_DENSITY, Diamond)
        self.__generate_character(self.player)
        
        # Generate Enemy
        self._try_generate_enemy()
             
        self.__generate_environment_in_field(None, Sand)

    def __generate_environment_in_field(self, object_density, game_object):
        if object_density is not None:
            objects_count = int(self._field_width * self._field_height * object_density)
            count_created_objects = 0

            for _ in range(objects_count):
                x = random.randint(0, self._field_width - 1)
                y = random.randint(0, self._field_height - 1)

                if isinstance(self._field[y][x], Emptiness):
                    self._field[y][x] = game_object()
                    count_created_objects += 1

            return count_created_objects
        else:
            for i in range(self._field_height):
                for j in range(self._field_width):
                    if isinstance(self._field[i][j], Emptiness):
                        self._field[i][j] = game_object()
            return -1

    def __generate_character(self, character):
            for i in range(self._field_height):
                for j in range(self._field_width):
                    if isinstance(self._field[i][j], Emptiness):
                        self._field[i][j] = character
                        self.player.coordinates = Coordinates(j, i)
                        return

    def _try_generate_enemy(self):
        map_ = FieldUtils.field_to_boolean_field(self._field, self._field_height, self._field_width)
        ex, ey = FieldUtils.find_farthest_point(map_, self._field_height, self._field_width, self.player.coordinates.x, self.player.coordinates.y)
        if self._field[ey][ex].can_enemy_move_on():
            if isinstance(self._field[ey][ex], Diamond):
                self._diamonds_count -= 1
            self._field[ey][ex] = Enemy(ex, ey)
            self.enemy_generation_success = True
            
            # Clear neighbors to ensure some movement
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in directions:
                nx, ny = ex + dx, ey + dy
                if 0 <= nx < self._field_width and 0 <= ny < self._field_height:
                    self._field[ny][nx] = Emptiness()
        else:
             self.enemy_generation_success = False

    def apply_action(self, action):
        if self.is_paused:
            return
        
        if action.type == ActionType.MOVE:
            self.player._move_player(action.direction, self._field)
        elif action.type == ActionType.PLACE_BOMB:
            p_coords = self.player.coordinates
            dx, dy = action.direction.value
            nx, ny = p_coords.x + dx, p_coords.y + dy
            
            if 0 <= ny < self._field_height and 0 <= nx < self._field_width:
                if self._field[ny][nx].can_stone_move_here() and self.player.current_count_bombs > 0:
                    self._field[ny][nx] = Bomb()
                    self.player.current_count_bombs -= 1         
    
    def update_field_state(self):
        if self.is_paused:
            return
        
        self.player.update_moves()
        EnvironmentManager.update_stones(self._field, self._field_width, self._field_height, self.player)
        EnvironmentManager.update_bombs(self._field, self._field_width, self._field_height, self)
        if self.game_tick % 30 == 0:
            diamonds_result = EnvironmentManager.update_enemies(self._field, self._field_width, self._field_height, self.player, self._try_generate_enemy)
            if type(diamonds_result) is int:
                self._diamonds_count -= diamonds_result
        GameStateManager.check_game_end(self)

        self.game_tick += 1
        if not self._is_custom_map and not self.enemy_generation_success and self.game_tick % 10 == 0:
            self._try_generate_enemy()
    
    


    @property
    def field(self):
        return self._field

    @property
    def field_width(self):
        return self._field_width

    @property
    def field_height(self):
        return self._field_height



