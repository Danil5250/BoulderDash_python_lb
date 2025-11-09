from Core.game_objects.base.GameEntity import GameEntity


class Character(GameEntity):
    __slots__ = GameEntity.__slots__ + ["__lives"]

    def __init__(self, view, foreground, lives):
        super().__init__(view, foreground)
        self.__lives = lives

    @property
    def lives(self) -> int:
        return self._lives

    @lives.setter
    def lives(self, value: int):
        if value >= 0:
            self._lives = value

    def decrease_lives(self):
        self.lives -= 1

    def decrease_lives_by(self, d_lives: int):
        self.lives -= d_lives

    def damage_to_player(self) -> int:
        return 0

    def can_player_move_on(self) -> bool:
        return False