class Settings():
    """存储《外星人入侵》的所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        #屏幕设置
        self.screen_width = 1280
        self.screen_height = 650
        self.bg_color = (230,230,230)

        #飞船设置
        self.ship_speed_factor = 5
        self.ship_limit = 3

        #子弹设置
        self.bullet_speed_factor = 8
        self.bullet_width = 1280
        self.bullet_height = 10
        self.bullet_color = 255,60,60
        self.bullets_allowed = 3

        #外星人设置
        self.alien_speed_factor = 3
        self.fleet_drop_speed = 10

        #1表示向右，-1表示向左
        self.fleet_direction = 1

