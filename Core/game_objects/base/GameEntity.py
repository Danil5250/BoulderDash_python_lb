class GameEntity:
    __slots__ = ("view", "foreground")

    def __init__(self, view, foreground):
        self.view = view
        self.foreground = foreground

    def can_player_move_on(self):
        return True

    def can_stone_move_here(self):
        return False
    
    def can_stone_fall_here(self):
        return False
    
    def can_enemy_move_on(self):
        return False

