from Core.game_objects.base.GameEntity import GameEntity


class Interectable(GameEntity):
    def __init__(self, view, foreground):
        super().__init__(view, foreground)

    def add_score_to_player(self):
        return 0

    def damage_to_player(self):
        return 0

    def add_health_to_player(self):
        return 0