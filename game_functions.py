import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings,stats,screen,sb,ship,bullets,aliens,play_button):
    """监控键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,stats,screen,sb,ship,bullets,aliens,play_button,mouse_x,mouse_y)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,stats,ship,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)


def check_keydown_events(event,ai_settings,screen,stats,ship,bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_SPACE and stats.game_active :
        fire_bullet(ai_settings,screen,bullets,ship)
    if event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_up =False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_play_button(ai_settings,stats,screen,sb,ship,bullets,aliens,play_button,mouse_x,mouse_y):
    """在玩家单击Play按钮时开始新游戏"""

    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()

        #隐藏光标
        pygame.mouse.set_visible(False)

        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        #重置记分牌信息
        sb.prep_score()
        sb.prep_highest_score()
        sb.prep_level()
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings,screen,aliens,ship)
        ship.center_ship()

def fire_bullet(ai_settings,screen,bullets,ship):
    """如果没有达到限制，就发射一颗子弹"""
    #创建新子弹并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x/(2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings,alien_height,ship_height):
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y/(2 * alien_height))
    return number_rows


def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    #创建一个外星人，并将其放在当前行
    alien = Alien(ai_settings,screen)    

    #外星人间距为外星人宽度、高度
    alien_width = alien.rect.width
    alien_height = alien.rect.height

    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = alien_height + 2 * alien_height * row_number

    alien.rect.x = alien.x
    alien.rect.y = alien.y

    aliens.add(alien)


def create_fleet(ai_settings,screen,aliens,ship):
    """创建外星人群"""
    #创建一个外星人，并计算每行可容纳多少个外星人
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)   
    number_rows = get_number_rows(ai_settings,alien.rect.height,ship.rect.height)

    #创建第一行外星人 
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)   


def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        """有外星人到达边缘时采取相应措施"""
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break


def change_fleet_direction(ai_settings,aliens):
    """将外星人整体下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """响应子弹和外星人的碰撞"""
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)

    if collisions:
        for aliens in collisions.values():
            stats.game_score +=ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_highest_score(stats,sb)
        

    if len(aliens) == 0:
        #删除现有的所有子弹，并创建一个新的外星人群
        #若整群外星人被消灭，就提高下一个等级
        bullets.empty()
        create_fleet(ai_settings,screen,aliens,ship)   

        #加快游戏节奏
        ai_settings.increase_speed() 

        #提高等级
        stats.game_level +=1
        sb.prep_level()


def check_aliens_bottom(ai_settings,stats,screen,sb,aliens,ship,bullets):
    """检测外星人是否到达屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
            break


def check_highest_score(stats,sb):
    """检查是否诞生了新的最高分"""
    if stats.game_score > stats.highest_score:
        stats.highest_score = stats.game_score
        sb.prep_highest_score()

def ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0 :
        stats.ships_left -= 1

        #更新记分牌
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船放到屏幕底部中央
        create_fleet(ai_settings,screen,aliens,ship)
        ship.center_ship()

        #暂停0.5s
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_ship(ship):
    ship.update()


def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    bullets.update()

    #删除已消失子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)


def update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    #检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        # print('ship hit!!!')
        ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)       

    #检查外星人是否到达屏幕底部
    check_aliens_bottom(ai_settings,stats,screen,sb,aliens,ship,bullets) 


def update_screen(ai_settings,stats,sb,screen,ship,background,bullets,aliens,play_button):
    """更新屏幕上的图像，并切换到新屏幕上"""
    #每次循环都重绘屏幕
    screen.fill(ai_settings.bg_color)
    background.blitme()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    #显示得分
    sb.show_score()

    #如果游戏处于非活跃状态，就显示Play按钮
    if not stats.game_active:
        play_button.draw_button()

    #让最近绘制的屏幕可见
    pygame.display.flip()