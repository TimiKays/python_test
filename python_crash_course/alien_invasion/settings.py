class Settings():
    """存储所有设置的类"""
    def __init__(self):
        """初始化游戏设置"""

        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        # 飞船设置
        self.ship_limit=3
        # 子弹设置
        self.bullet_width=300
        self.bullet_height=15
        self.bullet_color=60,60,60
        self.bullet_allowed=10
        # 外星人设置
        self.alien_speed_vertical=10
            
        # 游戏升级节奏
        self.speedup_scale=1.2
        self.score_scale=1.5
        self.initalize_dynamic_settings()

    def initalize_dynamic_settings(self):
        # 重置游戏运行中会变化的值
        self.ship_speed_factor=1.5
        self.bullet_speed_factor=3
        self.alien_speed_horizontal=1
        self.alien_direction=1  # 1表示向右，-1表示向左
        self.alien_points=50

    def increase_speed(self):
        # 提高游戏难度的方法，在消灭一波外星人后手动调用
        self.ship_speed_factor*=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.alien_speed_horizontal*=self.speedup_scale
        self.alien_points=int(self.alien_points*self.score_scale)
        print(self.alien_points)
