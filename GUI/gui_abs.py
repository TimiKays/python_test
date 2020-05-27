import wx

# 绝对布局
class MyFrame(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,title='新窗口',pos=(600,400),size=(400,300))
        # 创建面板
        panel=wx.Panel(self)
        # 设置字体
        # font=wx.Font(14,wx.DEFAULT,wx.FONTSTYLE_NORMAL,wx.NORMAL)
        # 控件
        self.title=wx.StaticText(panel,label='请输入用户名和密码',pos=(140,20))
        # self.title.SetFont(font )
        self.label_user=wx.StaticText(panel,label='用户名',pos=(50,50))
        self.text_user=wx.TextCtrl(panel,pos=(100,46),size=(235,25),style=wx.TE_LEFT)
        self.label_pwd = wx.StaticText(panel, label='密  码', pos=(50, 100))
        self.text_pwd = wx.TextCtrl(panel, pos=(100, 96), size=(235, 25), style=wx.TE_PASSWORD)
        #按钮
        self.bt_ok=wx.Button(panel,label='确定',pos=(105,150))
        self.bt_cancel = wx.Button(panel, label='取消', pos=(195, 150))


# 创建一个类，继承父类wx.App
class App(wx.App):
    def OnInit(self):
        # 创建窗口
        # frame=wx.Frame(parent=None,title='Hello wxPython')
        frame=MyFrame(parent=None,id=-1)
        frame.Show()
        return True



if __name__ == '__main__':
    # 创建实例
    app=App()

    # # 或者直接使用wx.App，当只有一个窗口时
    # app=wx.App()
    # frame=wx.Frame(None,title='你好呀')
    # frame.Show()

    # 调用主循环方法，将程序的控制权转交给wxPython
    app.MainLoop()