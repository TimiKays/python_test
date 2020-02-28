import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """外星人的类"""
    def __init__(self,ai_settings,screen):
        """初始化外星人，并设置其起始位置"""
        super().__init__()
        self.screen=screen
        self.ai_settings=ai_settings
        # 加载外星人图像，并获取rect对象
        self.image = pygame.image.load('images\\alien.bmp')
        self.rect=self.image.get_rect()

        # 设置图像位置在左上角附近
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        # 存储精确位置，方便后面计算
        self.x=float(self.rect.x)

    def blitme(self):
        # 根据方块位置绘制图片
        self.screen.blit(self.image,self.rect)

    def update(self):
        # 左/右移动
        self.x+=(self.ai_settings.alien_speed_horizontal*
            self.ai_settings.alien_direction)
        self.rect.x=self.x

    def check_edges(self):
        # 判断是否到边缘
        screen_rect=self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left<=0:
            return True


