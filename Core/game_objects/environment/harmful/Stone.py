from Core.config.environment.harmful.StoneConfig import StoneConfig
from Core.game_objects.base.Interectable import Interectable


class Stone(Interectable):
    __slots__ = list(Interectable.__slots__) + ["__can_player_pass", "__damage_to_player"]

    def __init__(self, stone_view=StoneConfig.STONE_SIGN, stone_foreground=StoneConfig.STONE_COLOR,
                 can_player_pass=StoneConfig.CAN_PLAYER_PASS, damage_to_player=StoneConfig.STONE_DAMAGE_PLAYER):
        super().__init__(stone_view, stone_foreground)
        self.can_player_pass = can_player_pass
        self.damage_to_player = damage_to_player
