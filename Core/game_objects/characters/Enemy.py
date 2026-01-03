from Core.config.characters.EnemyConfig import EnemyConfig
from Core.game_objects.base.Character import Character
from Core.utils.Enemy.Node import Node
from Core.utils.Enemy.PathFinder import PathFinder


class Enemy(Character):
    def __init__(self, start_x=0, start_y=0, damage = EnemyConfig.DAMAGE_TO_PLAYER, view=EnemyConfig.ENEMY_SIGN, forecolor = EnemyConfig.ENEMY_COLOR,
                 lives=EnemyConfig.LIVES):
        super().__init__(view, forecolor, lives)
        self.position = Node(start_x, start_y)
        self.previous_position = self.position
        self.current_path = []
        self._damage_to_player = damage

    def update(self, map_, player_x, player_y):
        

        
        if not self.current_path or self.should_recompute_path(player_x, player_y):
            self.current_path = PathFinder.find_path(
                map_,
                Node(self.position.x, self.position.y),
                Node(player_x, player_y)
            )

        if self.current_path and len(self.current_path) > 1:
            next_step = self.current_path[1]
            self.previous_position = self.position
            self.position = Node(next_step.x, next_step.y)
            self.current_path.pop(0)
        else:
            # if no path to player, move randomly
            import random
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            valid_moves = []
            
            h = len(map_)
            w = len(map_[0])
            
            for dx, dy in directions:
                nx, ny = self.position.x + dx, self.position.y + dy
                if 0 <= nx < w and 0 <= ny < h and map_[ny][nx]:
                    valid_moves.append((nx, ny))
            
            if valid_moves:
                nx, ny = random.choice(valid_moves)
                self.previous_position = self.position
                self.position = Node(nx, ny)

    def should_recompute_path(self, target_x, target_y):
        last = self.current_path[-1] if self.current_path else None
        return not last or last.x != target_x or last.y != target_y
    
    def damage_to_player(self):
        return self._damage_to_player
    
    def can_enemy_move_on(self):
        return True
    
    def decrease_lives(self, regenerate_enemy):
        self.lives -= 1
        if self.lives <= 0:
            regenerate_enemy()