import pygame.font

class Button():
    def __init__(self,ai_settings,screen,msg):
        """初始化按钮"""
        self.screen=screen
        self.screen_rect=screen.get_rect()
        """更改按钮尺寸和其他属性"""
        self.width,self.height=200,50
        self.button_color=(100,60,100)
        self.text_color=(255,255,255)
        self.font=pygame.font.SysFont(None,48)
        """创建按钮的rect属性并居中"""
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.screen_rect.center
        """按钮的标签只创建一次"""
        self.prep_msg(msg)

    def prep_msg(self,msg):
        """渲染按钮上的文字，并置于按钮中心"""
        # 布尔实参表示是否开启反锯齿功能，然后是字体颜色和背景色
        # 如果没有背景色，将为透明背景
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)
