import pygame
import game_functions as gf

from pygame.sprite import Group
from settings import Settings
from ship import Ship 
from alien import Alien
from game_stats import GameStats
from button import Button 
from scoreboard import Scoreboard


def run_game():
    #初始化游戏，创建一个屏幕对象
    pygame.init()
    ai_settings=Settings()
    # 返回一个窗口surface,参数是一个元祖
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('外星人入侵')
    # 创建一个按钮
    play_button = Button(ai_settings,screen,"PLAY")
    # 创建一个用于存储游戏信息的实例
    stats=GameStats(ai_settings)
    # 创建一个计分板对象
    sb=Scoreboard(ai_settings,screen,stats)
    # 创建一艘飞船
    ship = Ship(screen,ai_settings)
    # 创建一个group存储子弹
    bullets_group=Group()
    # 创建一个group存储外星人
    aliens_group=Group()
    gf.create_fleet(ai_settings,screen,aliens_group,ship)
    level=1
    #游戏主循环
    while True:
        #监听鼠标键盘事件，更改飞船的是否在移动的flag
        gf.check_events(ai_settings,screen,ship,bullets_group,stats,play_button,aliens_group,sb)

        if stats.game_active:
            ship.update()
            # 绘制子弹
            gf.update_bullets(bullets_group,aliens_group,ai_settings,screen,ship,stats,sb)
            gf.update_aliens(ai_settings, aliens_group,ship,stats,screen,bullets_group,sb)
        
        # 更新屏幕
        gf.update_screen(ai_settings,screen,bullets_group,ship,aliens_group,stats,play_button,sb)
        
run_game()
