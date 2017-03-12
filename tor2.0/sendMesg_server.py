__author__ = "daniel ozer"
import wx

class MainFrame(wx.Frame):
    def __init__(self,  parent, id,
                 pos, title,size):

        wx.Frame.__init__(self, parent, id, title, pos, size)

class App(wx.App):
    """Application class."""

    def OnInit(self):

        self.frame = MainFrame(None,-1,wx.DefaultPosition,"TOR",(500,500))
        self.frame.Show()
        self.frame.Centre()
        panel=wx.Panel(self.frame)
        self.start_btn=wx.Button(panel, label='START',pos=wx.DefaultPosition  )
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.start_btn)
        return True
    def OnButtonClick(self,event):
        self.Close()

class LoginFrame(wx.App):
    def OnInit(self):

        self.frame = MainFrame(None,-1,wx.DefaultPosition,"Login",(400,400))

        panel=wx.Panel(self.frame)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.start_btn=wx.Button(panel, label='START'  )
        main_sizer.AddStretchSpacer()
        main_sizer.Add(self.start_btn, 0, wx.CENTER)
        main_sizer.AddStretchSpacer()

        panel.SetSizer(main_sizer)


        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.start_btn)

        self.frame.Show()
        self.frame.Centre()
        return True
    def OnButtonClick(self,event):
        self.frame.Close()
def main():

    login_app=LoginFrame()

    login_app.MainLoop()
    app=App()
    app.MainLoop()
if __name__ == '__main__':
    main()