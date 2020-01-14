import sys

import pygame

from settings import Settings
from ship import Ship
from game_stats import GameStats
from background import Background
from button import Button
import game_functions as gf
from pygame.sprite import Group


def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()

    #一些属性设置
    ai_settings = Settings()

    #屏幕显示
    screen = pygame.display.set_mode(
        (ai_settings.screen_width ,ai_settings.screen_height))

    #窗口标题
    pygame.display.set_caption("Alien Invasion")

    #创建背景图    
    background = Background(screen)

    #创建Play按钮
    play_button = Button(ai_settings,screen,"Play")

    #创建一艘飞船
    ship = Ship(ai_settings,screen)

    #创建一个用于存储子弹的编组
    bullets = Group()
    aliens = Group()

    #创建外星人群
    gf.create_fleet(ai_settings,screen,aliens,ship)

    #创建一个外星人
    # alien = Alien(ai_settings,screen)

    #创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)

    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings,stats,screen,ship,bullets,aliens,play_button)

        if stats.game_active :
            gf.update_ship(ship)
            gf.update_bullets(ai_settings,screen,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets)

        gf.update_screen(ai_settings,stats,screen,ship,background,bullets,aliens,play_button)

        # print(len(bullets))

run_game()