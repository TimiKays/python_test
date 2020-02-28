import pygame
from pygame.sprite import Sprite 

class Ship(Sprite):
    """用来管理飞船的行为"""
    def __init__(self,screen,ai_settings):
        """初始化飞船并设置其初始位置
        第二个参数指定了飞船要绘制到什么地方"""
        super().__init__()

        self.screen=screen
        self.ai_settings=ai_settings

        # 加载图像，返回一个表示飞船的surface
        self.image=pygame.image.load('images/ship.bmp')
        # 获取surface 的矩形，这样就能像处理矩形一样的处理元素
        self.rect=self.image.get_rect()
        
        # 获取窗口的矩形
        self.screen_rect=screen.get_rect()
        # 设置图像到窗口的底部中央
        self.center_ship()
        self.rect.bottom=self.screen_rect.bottom

        # 为什么要给center赋值这个，因为要存储到一个可以存float的变量里
        # 为什么要把int转成float，方便后面做加减运算
        self.center=float(self.rect.centerx)
        self.moving_right=False
        self.moving_left=False

    def blitme(self):
        """ 根据self.rect指定的位置绘制图像"""
        self.screen.blit(self.image,self.rect)
        

    def update(self):
        """用来更新位置"""
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.center+=self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left>0:
            self.center-=self.ai_settings.ship_speed_factor
        # 根据center更新rect对象，不用转吗
        self.rect.centerx = self.center

    def center_ship(self):
        """让飞船居中"""
        self.rect.centerx=self.screen_rect.centerx



