import pygame

class Background():

    def __init__(self,screen):
        """初始化背景图并设置其初始位置"""
        self.screen = screen

        #加载背景图像并获取其外接矩形
        self.image = pygame.image.load('images/background.jpg')

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def blitme(self):
        self.screen.blit(self.image,self.rect)
        