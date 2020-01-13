import pygame

from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self,ai_settings,screen):
        """初始化外星人并设置其初始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载外星人图像，并设置rect属性
        self.image = pygame.image.load('images/alien.png_no_bg.png')
        self.rect = self.image.get_rect()

        #每个外星人最初都是在屏幕左上角附近
        self.rect.x = self.rect.width       #外星人左边距设置为外星人宽度
        self.rect.y = self.rect.height      #外星人上边距设置为外星人高度

        #存储外星人准确位置
        self.x = float(self.rect.x)
    
    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image,self.rect)

    def check_edges(self):
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """向右移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x


