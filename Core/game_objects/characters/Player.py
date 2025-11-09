from Core.config.characters.PlayerConfig import PlayerConfig
from Core.game_objects.base.Character import Character


class Player(Character):
    __slots__ = list(Character.__slots__) + ["_max_count_bombs", "_max_stone_moves", "_max_player_jumps"]

    def __init__(self, view=PlayerConfig.PLAYER_SIGN, foreground=PlayerConfig.PLAYER_COLOR,
                 lives=PlayerConfig.COUNT_LIVES, max_count_bombs=PlayerConfig.MAX_COUNT_OF_BOMBS,
                 max_stone_moves=PlayerConfig.MAX_PLAYER_STONE_MOVES,
                 max_player_jumps=PlayerConfig.MAX_PLAYER_JUMPS):
        Character.__init__(self, view, foreground, lives)
        self._max_count_bombs = max_count_bombs
        self._max_stone_moves = max_stone_moves
        self._max_player_jumps = max_player_jumps