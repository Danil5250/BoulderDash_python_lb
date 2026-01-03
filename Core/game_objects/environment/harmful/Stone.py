from Core.config.environment.harmful.StoneConfig import StoneConfig
from Core.game_objects.base.Interectable import Interectable


class Stone(Interectable):
    __slots__ = list(Interectable.__slots__) + ["__can_player_pass", "__damage_to_player", 
                                                "fall_delay", "fall_timer", "is_falling"]
    
    
    def __init__(self, stone_view=StoneConfig.STONE_SIGN, stone_foreground=StoneConfig.STONE_COLOR,
                 can_player_pass=StoneConfig.CAN_PLAYER_PASS, damage_to_player=StoneConfig.STONE_DAMAGE_PLAYER,
                 fall_delay=StoneConfig.FALL_DELAY, fall_timer=StoneConfig.FALL_TIMER, is_falling=StoneConfig.IS_FALLING):
        super().__init__(stone_view, stone_foreground)
        self.__can_player_pass = can_player_pass
        self.__damage_to_player = damage_to_player
        self.fall_delay = fall_delay
        self.fall_timer = fall_timer
        self.is_falling = is_falling
    
    def can_player_move_on(self):
        return self.__can_player_pass
    
    def damage_to_player(self):
        return self.__damage_to_player
