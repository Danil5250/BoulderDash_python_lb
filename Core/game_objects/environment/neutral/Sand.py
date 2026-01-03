from Core.config.environment.neutral.SandConfig import SandConfig
from Core.game_objects.base.Interectable import Interectable


class Sand(Interectable):

    __slots__ = list(Interectable.__slots__) + ["__can_stone_moved_here"]

    def __init__(self, view=SandConfig.SAND_SIGN, forecolor=SandConfig.SAND_COLOR,
                 can_stone_moved_here=SandConfig.CAN_STONE_MOVED_AT_SAND):
        super().__init__(view, forecolor)
        self.__can_stone_moved_here = can_stone_moved_here
    
    def can_stone_move_here(self):
        return self.__can_stone_moved_here
    
    def can_enemy_move_on(self):
        return True