from Core.config.environment.neutral.EmptinessConfig import EmptinessConfig
from Core.game_objects.base.Interectable import Interectable


class Emptiness(Interectable):
    __slots__ = list(Interectable.__slots__) + ["_can_stone_fall_here"]
    
    def __init__(self, view=EmptinessConfig.EMPTINESS_SIGN, forecolor=EmptinessConfig.EMPTINESS_COLOR,
                 can_stone_fall_here=EmptinessConfig.CAN_STONE_FALL_AT_EMPTINESS):
        super().__init__(view, forecolor)
        self._can_stone_fall_here = can_stone_fall_here