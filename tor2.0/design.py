__author__ = "daniel ozer"

import wx
from wx.lib import sized_controls


class MainFrame(sized_controls.SizedFrame):

    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        self.SetTitle('MainFrame')
        pane = self.GetContentsPane()

        #pane=wx.Panel(self)
        start_btn=wx.Button(pane, label='START',  )
        start_btn.Position((240, 240))
        self.SetInitialSize((500, 500))
        self.Centre()

class LoginFrame(sized_controls.SizedDialog):

    def __init__(self, *args, **kwargs):
        super(LoginFrame, self).__init__(*args, **kwargs)
        self.parent = args[0]
        self.logged_in = False

        pane = self.GetContentsPane()

        pane_form = sized_controls.SizedPanel(pane)
        pane_form.SetSizerType('form')

        label = wx.StaticText(pane_form, label='User Name')
        label.SetSizerProps(halign='right', valign='center')

        self.user_name_ctrl = wx.TextCtrl(pane_form, size=((200, -1)))

        label = wx.StaticText(pane_form, label='Password')
        label.SetSizerProps(halign='right', valign='center')

        self.password_ctrl = wx.TextCtrl(
            pane_form, size=((200, -1)), style=wx.TE_PASSWORD)

        pane_btns = sized_controls.SizedPanel(pane)
        pane_btns.SetSizerType('horizontal')
        pane_btns.SetSizerProps(halign='right')

        login_btn = wx.Button(pane_btns, label='Login')
        login_btn.SetDefault()
        cancel_btn = wx.Button(pane_btns, label='Cancel')
        self.Fit()
        self.SetTitle('Login')
        self.CenterOnParent()
        self.parent.Disable()

        login_btn.Bind(wx.EVT_BUTTON, self.on_btn_login)
        cancel_btn.Bind(wx.EVT_BUTTON, self.on_btn_cancel)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Centre()


    def on_btn_login(self, event):
        user_name = self.user_name_ctrl.GetValue()
        password = self.password_ctrl.GetValue()
        server_answer=1
        if (server_answer):

            print 'logged in as {} with password {}'.format(user_name, password)
            self.logged_in = True
            self.Close()
        else:
            self.Close()
            print 'wrong passowrd/username'

    def on_btn_cancel(self, event):
        self.Close()

    def on_close(self, event):
        if not self.logged_in:
            self.parent.Close()
        self.parent.Enable()
        event.Skip()


if __name__ == '__main__':
    wxapp = wx.App(False)
    parent_frame = MainFrame(None)
    parent_frame.Show()
    login_frame = LoginFrame(parent_frame)
    login_frame.Show()
    wxapp.MainLoop()