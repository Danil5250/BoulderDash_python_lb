from Core.config.characters.PlayerConfig import PlayerConfig
from Core.game_objects.base.Character import Character
from Core.utils.FieldUtils import FieldUtils


from Core.game_objects.environment.harmful.Stone import Stone
from Core.game_objects.environment.neutral.Emptiness import Emptiness


class Player(Character):
    __slots__ = list(Character.__slots__) + ["max_stone_moves", "max_player_jumps",
                                             "current_count_bombs", "current_stone_moves", "current_player_jumps",
                                             "coordinates", "score", "stone_move_timer", "jump_timer"]

    def __init__(self, view=PlayerConfig.PLAYER_SIGN, foreground=PlayerConfig.PLAYER_COLOR,
                 lives=PlayerConfig.COUNT_LIVES, max_count_bombs=PlayerConfig.MAX_COUNT_OF_BOMBS,
                 max_stone_moves=PlayerConfig.MAX_PLAYER_STONE_MOVES,
                 max_player_jumps=PlayerConfig.MAX_PLAYER_JUMPS):
        Character.__init__(self, view, foreground, lives)
        self.max_stone_moves = max_stone_moves
        self.max_player_jumps = max_player_jumps
        
        self.current_count_bombs = max_count_bombs
        
        self.current_stone_moves = max_stone_moves
        self.current_player_jumps = max_player_jumps
        
        self.stone_move_timer = 0
        self.jump_timer = 0
        
        self.coordinates = None
        self.score = 0
    
    def update_moves(self):
        if self.current_stone_moves < self.max_stone_moves:
            self.stone_move_timer += 1
            if self.stone_move_timer >= PlayerConfig.SECONDS_TO_RESTORE_STONE_MOVES * 30: # 30 FPS (fps = how many frames have changed) 30 approx equals 1 second - (if enough frames have passed to restore stone moves)
                self.current_stone_moves += PlayerConfig.RESTORE_STONE_MOVES_AT_ONCE
                if self.current_stone_moves > self.max_stone_moves:
                    self.current_stone_moves = self.max_stone_moves
                self.stone_move_timer = 0
        
        if self.current_player_jumps < self.max_player_jumps:
            self.jump_timer += 1
            if self.jump_timer >= PlayerConfig.SECONDS_TO_RESTORE_JUMPS * 30: # Assuming 30 FPS
                self.current_player_jumps += PlayerConfig.RESTORE_JUMPS_AT_ONCE
                if self.current_player_jumps > self.max_player_jumps:
                    self.current_player_jumps = self.max_player_jumps
                self.jump_timer = 0

    def _move_player(self, direction, field):
        dx, dy = direction.value
        x = self.coordinates.x
        y = self.coordinates.y
        
        is_jump = abs(dx) == 2 or abs(dy) == 2
        if is_jump:
            if self.current_player_jumps <= 0:
                return
        
        nx, ny = x + dx, y + dy
        
        if FieldUtils.can_move(field, nx, ny):
            if is_jump:
                self.current_player_jumps -= 1
                
            self.increase_score(field[ny][nx].add_score_to_player())
            FieldUtils.move_object(field, y, x, ny, nx)
            self.coordinates.x = nx
            self.coordinates.y = ny
        elif 0 <= ny < len(field) and 0 <= nx < len(field[0]) and isinstance(field[ny][nx], Stone) and not is_jump:
            if self.current_stone_moves > 0:
                nnx, nny = nx + dx, ny + dy
                if 0 <= nny < len(field) and 0 <= nnx < len(field[0]) and field[nny][nnx].can_stone_move_here():
                    self.current_stone_moves -= 1
                    FieldUtils.move_object(field, ny, nx, nny, nnx)
                    FieldUtils.move_object(field, y, x, ny, nx)
                    self.coordinates.x = nx
                    self.coordinates.y = ny
    
    def increase_score(self, count):
        self.score += count

    def can_enemy_move_on(self):
        return True
