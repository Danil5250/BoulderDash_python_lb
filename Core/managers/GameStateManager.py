

class GameStateManager:
    
    @staticmethod
    def check_game_end(main_manager):
        if GameStateManager.check_game_over(main_manager.player):
            main_manager.is_game_win = False
        if GameStateManager.check_game_win(main_manager.player.score, main_manager._diamonds_count):
            main_manager.is_game_win = True
    
        
    
    @staticmethod
    def check_game_over(player):
        return player.lives <= 0
    
    @staticmethod
    def check_game_win(collected_diamonds, total_diamonds):
        return collected_diamonds >= total_diamonds