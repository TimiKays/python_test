class GameStats():
    """跟踪游戏的统计信息"""
    def __init__(self,ai_settings):
        self.ai_settings=ai_settings
        self.reset_stats()
        self.game_active=False
        self.high_score=0
        
    def reset_stats(self):
        """初始化可能变化的统计信息，重新开局会重置"""
        # 飞船的生命
        self.ships_left=self.ai_settings.ship_limit
        self.score=0
        self.level=1
        