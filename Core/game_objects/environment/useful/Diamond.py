from Core.config.environment.useful.DiamondConfig import DiamondConfig
from Core.game_objects.base.Interectable import Interectable

class Diamond(Interectable):
    __slots__ = list(Interectable.__slots__) + ["__score_add_to_player"]

    def __init__(self, view=DiamondConfig.DIAMOND_SIGN, forecolor=DiamondConfig.DIAMOND_COLOR,
                 score_add_to_player=DiamondConfig.COUNT_ADD_SCORE_TO_PLAYER):
        super().__init__(view, forecolor)
        self.__score_add_to_player = score_add_to_player

    def add_score_to_player(self):
        return self.__score_add_to_player
    
    def can_enemy_move_on(self):
        return True

