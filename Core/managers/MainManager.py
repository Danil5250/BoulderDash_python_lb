from Core.config.base.GameConfig import GameConfig
from Core.game_objects.environment.harmful.Stone import Stone
from Core.game_objects.environment.neutral.Emptiness import Emptiness
from Core.game_objects.environment.neutral.Sand import Sand
from Core.game_objects.environment.useful.Diamond import Diamond
import random
from Core.utils.Coordinates import Coordinates
from Core.utils.FieldUtils import FieldUtils


class MainManager:
    __slots__ = ['_field', '_field_width', '_field_height', '_diamonds_count']

    def __init__(self, field_width=GameConfig.FIELD_WIDTH, field_height=GameConfig.FIELD_HEIGHT):
        self._field_width = field_width
        self._field_height = field_height
        self._diamonds_count = -1
        self._field = FieldUtils.init_field(self._field_height, self._field_width)

        self.init_field_randomly()

    def init_field_randomly(self):
        self.__generate_environment_in_field(GameConfig.STONE_DENSITY, Stone)
        self._diamonds_count = self.__generate_environment_in_field(GameConfig.STONE_DENSITY, Diamond)
        self.__generate_character(self.player)
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
                        #self.player.coordinates = Coordinates(i, j)

    @property
    def field(self):
        return self._field

    @property
    def field_width(self):
        return self._field_width

    @property
    def field_height(self):
        return self._field_height



