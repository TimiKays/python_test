import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """一个管理子弹的类"""

    def __init__(self, ai_settings, screen, ship):
        """在飞船所处位置创建一个子弹对象"""
        super().__init__()
        self.screen = screen

        # 先在（0,0）创建一个子弹矩形，然后设置到飞船的顶部居中.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
            ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # 存储用小数表示子弹位置.不用x是因为子弹只要垂直运动
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """在屏幕上移动子弹"""
        # 把子弹移动小数位置，向上走要用减号.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y
        
    def draw_bullet(self):
        """把子弹绘制到屏幕上"""
        pygame.draw.rect(self.screen, self.color, self.rect)
