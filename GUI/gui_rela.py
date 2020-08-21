
import wx
class MyFrame(wx.Frame):
    def __init__(self, parent ,id):
        # 两种写法：
        # super().__init__(parent,id,'用户登录',size=(400,300))
        wx.Frame.__init__(self ,parent ,id ,'用户登录' ,size=(400 ,300))

        # 面板
        panel =wx.Panel(self)
        # 控件
        self.title = wx.StaticText(panel, label='请输入用户名和密码')
        # self.title.SetFont(font )
        self.label_user = wx.StaticText(panel, label='用户名')
        self.text_user = wx.TextCtrl(panel, style=wx.TE_LEFT)
        self.label_pwd = wx.StaticText(panel, label='密  码')
        self.text_pwd = wx.TextCtrl(panel,style=wx.TE_PASSWORD)
        # 按钮
        self.bt_ok = wx.Button(panel, label='确定')
        self.bt_ok.Bind(wx.EVT_BUTTON,self.onClickOk)

        self.bt_cancel = wx.Button(panel, label='取消')
        self.bt_cancel.Bind(wx.EVT_BUTTON, self.onClickCancel)


        # 添加子进行排列
        hsizer_user =wx.BoxSizer(wx.HORIZONTAL)
        hsizer_user.Add(self.label_user ,proportion=0 ,flag=wx.ALL ,border=5)
        hsizer_user.Add(self.text_user, proportion=1, flag=wx.ALL, border=5)
        hsizer_pwd = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_pwd.Add(self.label_pwd, proportion=0, flag=wx.ALL, border=5)
        hsizer_pwd.Add(self.text_pwd, proportion=1, flag=wx.ALL, border=5)
        hsizer_but = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_but.Add(self.bt_ok, proportion=0, flag=wx.ALIGN_CENTER, border=5)
        hsizer_but.Add(self.bt_cancel, proportion=0, flag=wx.ALIGN_CENTER, border=5)
        # 添加父容器
        vsizer_all =wx.BoxSizer(wx.VERTICAL)
        vsizer_all.Add(self.title ,proportion=0 ,flag=wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER ,border=15)
        vsizer_all.Add(hsizer_user, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=45)
        vsizer_all.Add(hsizer_pwd, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=45)
        vsizer_all.Add(hsizer_but, proportion=0, flag=wx.TOP | wx.ALIGN_CENTER, border=15)

        panel.SetSizer(vsizer_all)
    def onClickOk(self,event):
        message=''
        username=self.text_user.GetValue()
        password=self.text_pwd.GetValue()
        if username=='' or password=="":
            message='不能为空'
        elif username=='timi' and password=='123':
            message='登录成功'
        else:
            message='登录失败，用户名或密码错误'
        wx.MessageBox(message)
    def onClickCancel(self,event):
        self.text_user.SetValue('')
        self.text_pwd.SetValue('')

if __name__ == '__main__':
    app =wx.App()
    frame =MyFrame(parent=None ,id=1)
    frame.Show()
    app.MainLoop()
