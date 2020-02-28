import sys
import pygame
from alien import Alien
from time import sleep
from bullet import Bullet

def check_events(ai_settings,screen,ship,bullets_group,stats,play_button,aliens_group,sb):
    """相应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 点击了关闭按钮
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # 按键
            check_keydown_events(event,ai_settings,screen,ship,bullets_group)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 鼠标点击
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,screen,aliens_group,bullets_group,ship,sb)

def check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,screen,aliens_group,bullets_group,ship,sb):
    """点击到了开始按键后"""
    button_clicked= play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        # 当按下开始键且游戏状态为非活跃时
        # 重置设置
        ai_settings.initalize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置统计信息
        stats.reset_stats()
        stats.game_active=True
        # 更新计分板图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空子弹和外星人
        aliens_group.empty()
        bullets_group.empty()
        # 创建新的外星人
        create_fleet(ai_settings,screen,aliens_group,ship)
        # 飞船居中
        ship.center_ship()


def check_keydown_events(event,ai_settings,screen,ship,bullets_group):
    # 按下按键的函数
    if event.key == pygame.K_RIGHT:
        # 按下右键，设置飞船移动的flag
        ship.moving_right=True
    elif event.key == pygame.K_LEFT:
        ship.moving_left=True
    elif event.key == pygame.K_SPACE:
        # 按下空格，创建一颗子弹添加到编组中
        fire_bullet(ai_settings,screen,ship,bullets_group)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    """松开按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right=False
    elif event.key == pygame.K_LEFT:
        ship.moving_left=False

def update_screen(ai_settings,screen,bullets_group,ship,aliens_group,stats,play_button,sb):
    """更新屏幕上的图像，并切换到新屏幕"""
    #每次循环填充背景
    screen.fill(ai_settings.bg_color)
    # 画出子弹。这里为什么要有个.sprites()?
    #   删掉也可以正常运行，查看文档得知两种方式都可以。.
    #   sprites()可能会在后面的版本中有所改进。
    for bullet in bullets_group:
        bullet.draw_bullet()
    # 绘制飞船，根据飞船的flag移动飞船
    ship.blitme()  

    # 绘制外星人，把group里的所有sprites绘制到一个指定的surface上
    # alien.blitme()
    aliens_group.draw(screen)
    # 显示计分板
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    # pygame.display.flip()
    # flip也可以改成update，更新变化的区域
    pygame.display.update()


def update_bullets(bullets_group,aliens_group,ai_settings,screen,ship,stats,sb):
    """更新子弹的位置，并删除已消失的子弹"""
    bullets_group.update()
    # 如果子弹超出屏幕了，就从列表中删掉。
    for bullet in bullets_group.copy():
        if bullet.rect.bottom<=0:
            bullets_group.remove(bullet)
    check_bullet_alien_collisions(bullets_group,aliens_group,ai_settings,screen,ship,stats,sb)


def check_bullet_alien_collisions(bullets_group,aliens_group,ai_settings,screen,ship,stats,sb):
    """检查子弹是否击中外星人"""
    # 检查子弹是否击中外星人。两个true表示要删除碰撞了的子弹和外星人。
    # 如果是激光，第一个为false
    collisions = pygame.sprite.groupcollide(bullets_group,aliens_group,False,True)
    if collisions:
        for aliens in collisions.values():
            # aliens是一个被同个子弹击中的所有外星人的列表
            stats.score+=ai_settings.alien_points*len(aliens)
            # 重新绘制计分板
            sb.prep_score()
        check_high_score(stats,sb)

    # 如果外星人都死了，就再生成一批
    if len(aliens_group) ==0:
        bullets_group.empty()
        # 增加难度的
        ai_settings.increase_speed()
        stats.level+=1
        sb.prep_level()
        create_fleet(ai_settings,screen,aliens_group,ship)

def fire_bullet(ai_settings,screen,ship,bullets_group):
    """发射子弹"""
    if len(bullets_group)<ai_settings.bullet_allowed:
        new_bullet=Bullet(ai_settings, screen, ship)
        bullets_group.add(new_bullet)

def create_fleet(ai_settings,screen,aliens_group,ship):
    """创建外星人群"""
    # 为避免重复访问rect属性，获取一个alien宽度并存储到变量(重构create_alien()后不需要了)
    alien=Alien(ai_settings,screen)
    # 计算一行可以容纳多少外星人
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_aliens_y=get_number_aliens_y(ai_settings,alien.rect.width,ship.rect.height)
    # 创建y行x列外星人
    for alien_number_y in range(number_aliens_y):
        for alien_number_x in range(number_aliens_x):
            create_alien(ai_settings,screen,alien_number_x,alien_number_y,aliens_group)

def get_number_aliens_x(ai_settings,alien_width):
    """计算一行可以容纳多少外星人"""
    available_space_x=ai_settings.screen_width-2*alien_width
    number_aliens_x=int(available_space_x/2/alien_width)
    return number_aliens_x

def get_number_aliens_y(ai_settings,alien_height,ship_height):
    """计算可以容纳多少行外星人"""
    available_space_y=ai_settings.screen_height-3*alien_height-ship_height
    number_aliens_y=int(available_space_y/2/alien_height)
    return number_aliens_y

def create_alien(ai_settings,screen,alien_number_x,alien_number_y,aliens_group):
    """创建一个外星人"""
    alien=Alien(ai_settings,screen)
    alien_width=alien.rect.width
    alien_height=alien.rect.height
    # 计算每一个的x坐标，每一个相隔一宽度的距离
    alien.x=alien_width+2*alien_width*alien_number_x
    alien.rect.x=alien.x
    # 计算y坐标
    alien.y=alien_height+2*alien_height*alien_number_y
    alien.rect.y=alien.y
    aliens_group.add(alien)

def update_aliens(ai_settings,aliens_group,ship,stats,screen,bullets_group,sb):
    # 如果在边缘，就往下移动，并更改方向
    check_fleet_edges(ai_settings, aliens_group)
    # 左右移动一个位置
    aliens_group.update()
    # 每次移动后，检测是否撞到飞船。如果是，就停止遍历。如果没有，返回null
    if pygame.sprite.spritecollideany(ship,aliens_group):
        ship_hit(ai_settings,stats,screen,ship,aliens_group,bullets_group,sb)
    # 判断外星人是否到底了
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens_group,bullets_group,sb)

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens_group,bullets_group,sb):
    """判断外星人是否到底了"""
    screen_rect=screen.get_rect()
    for alien in aliens_group:
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings,stats,screen,ship,aliens_group,bullets_group,sb)
            break

def ship_hit(ai_settings,stats,screen,ship,aliens_group,bullets_group,sb):
    """外星人撞到飞船或者飞船触底后"""
    # 飞船生命值减一
    if stats.ships_left>0:
        stats.ships_left-=1
        # 更新记分牌的飞船
        sb.prep_ships()
        # 设置飞船到窗口的底部中央
        ship.center_ship()

        # 清空所有的子弹和外星人
        bullets_group.empty()
        aliens_group.empty()
        create_fleet(ai_settings,screen,aliens_group,ship)

        """反应时间0.5秒"""
        sleep(0.5)
    else:
        # 游戏结束
        stats.game_active=False
        pygame.mouse.set_visible(True)

def check_fleet_edges(ai_settings,aliens_group):
    # 判断外星人是否在边缘
    for alien in aliens_group:
        if alien.check_edges():

            # 如果在边缘，就执行这个方法
            change_fleet_direction(ai_settings,aliens_group)
            break

def change_fleet_direction(ai_settings,aliens_group):
    # 所有外星人往下移动，并把方向*-1改成相反的
    for alien in aliens_group:
        alien.rect.y += ai_settings.alien_speed_vertical
    ai_settings.alien_direction *=-1

def check_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()
