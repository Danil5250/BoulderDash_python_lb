from Core.config.environment.neutral.EmptinessConfig import EmptinessConfig
from Core.game_objects.base.Interectable import Interectable


class Emptiness(Interectable):
    __slots__ = list(Interectable.__slots__) + ["__can_stone_fall_here", "__can_stone_move_here"]
    
    def __init__(self, view=EmptinessConfig.EMPTINESS_SIGN, forecolor=EmptinessConfig.EMPTINESS_COLOR,
                 can_stone_fall_here=EmptinessConfig.CAN_STONE_FALL_AT_EMPTINESS,
                 can_stone_move_here = EmptinessConfig.CAN_STONE_MOVE_AT_EMPTINESS):
        super().__init__(view, forecolor)
        self.__can_stone_fall_here = can_stone_fall_here
        self.__can_stone_move_here = can_stone_move_here
    
    def can_stone_fall_here(self):
        return self.__can_stone_fall_here
    
    def can_stone_move_here(self):
        return self.__can_stone_move_here
    
    def can_enemy_move_on(self):
        return True