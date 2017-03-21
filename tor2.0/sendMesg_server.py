_author__ = "daniel ozer"
import wx


<<<<<<< HEAD
#global variable
frame_state="first"

=======
#global verials
class glo_var():
    next_frame=4
>>>>>>> origin/master

class MainFrame(wx.Frame):
    def __init__(self,  parent, id, pos, title, size):

        wx.Frame.__init__(self, parent, id, title, pos, size)

class LoginFrame(wx.App):
    def OnInit(self):

        self.frame = MainFrame(None,-1,wx.DefaultPosition,"Login",(400,400))

        self.panel=wx.Panel(self.frame)
        self.showLoginBox()

        self.frame.SetBackgroundColour((100, 179, 179))
        self.frame.Show()
        self.frame.Centre()
        return True
    def showLoginBox(self): #Create the sizer
        sizer = wx.FlexGridSizer(rows=3, cols=2, hgap=5, vgap=15)

        # Username
        self.txt_Username = wx.TextCtrl(self.panel, 1, size=(150, -1))
        lbl_Username = wx.StaticText(self.panel, -1, "Username:")

        sizer.Add(lbl_Username, 0, wx.LEFT | wx.TOP | wx.RIGHT, 50)
        sizer.Add(self.txt_Username,0, wx.TOP| wx.RIGHT, 50)

        # Password
        self.txt_Password = wx.TextCtrl(self.panel, 1, size=(150, -1), style=wx.TE_PASSWORD)
        lbl_Password = wx.StaticText(self.panel, -1, "Password:")
        sizer.Add(lbl_Password,0, wx.LEFT|wx.RIGHT, 50)
        sizer.Add(self.txt_Password,0, wx.RIGHT, 50)

        # Submit button
        btn_Process = wx.Button(self.panel, -1, "&Login",pos=(150,150))
        self.panel.Bind(wx.EVT_BUTTON, self.OnSubmit, btn_Process)
        #sizer.Add(btn_Process,0, wx.LEFT, 50)

        self.panel.SetSizer(sizer)
    def check_pass(self,pass_user):
        UserText = pass_user[1]
        PasswordText = pass_user[0]

        check=True
        if check:
            return True
        return False
    def OnSubmit(self, event):

        UserText = self.txt_Username.GetValue()
        PasswordText = self.txt_Password.GetValue()
        print "user_name: "+str(UserText)
        print "password: "+str(PasswordText)
        combo= (UserText,PasswordText)
        check=self.check_pass(combo)
        if check:
            self.frame.Close()
            return True

        return False


class start_frame(wx.App):
    """Application class."""

    def OnInit(self):

        self.frame = MainFrame(None, -1, wx.DefaultPosition, "TOR", (500, 500))

        panel = wx.Panel(self.frame)
        box = wx.BoxSizer(wx.VERTICAL)

        lbl1 = wx.StaticText(panel,-1, style = wx.ALIGN_CENTER | wx.ST_ELLIPSIZE_MIDDLE,pos=(17,50))
        lbl1.SetLabel("$$$$$$$$$$ welcome to $$$$$$$$$$\n TOR")
        lbl1.SetForegroundColour((255,0,0))
        lbl1.SetBackgroundColour((0,0,0))
        font = lbl1.GetFont()
        font.SetPointSize(20)
        lbl1.SetFont(font)

        box.Add(lbl1,0,wx.ALIGN_LEFT)
        panel.SetSizer(box)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.start_btn = wx.Button(panel, label='START')
        main_sizer.AddStretchSpacer()
        main_sizer.Add(self.start_btn, 0, wx.CENTER)
        main_sizer.AddStretchSpacer()

        panel.SetSizer(main_sizer)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.start_btn)

        self.frame.SetBackgroundColour((100, 179, 179))

        self.frame.Centre()
        self.frame.Show()

        return True
    def OnButtonClick(self,event):
        self.frame.Close()


class second_frame(wx.App):
    """Application class."""

    def OnInit(self):





        #

        self.frame = MainFrame(None, -1, wx.DefaultPosition, "TOR", (500, 500))

        panel = wx.Panel(self.frame)

<<<<<<< HEAD
        rev = wx.StaticText(panel, -1, "choose your option",(185, 50),
                (105, 20))
=======
        rev = wx.StaticText(panel, -1, "choose your option",(180, 70),
                (110, 20))
>>>>>>> origin/master
        rev.SetForegroundColour('white')
        rev.SetBackgroundColour('red')


        self.send_btn = wx.Button(panel, label='send mesg',size=(200,200),pos=(45,200))
        self.inbox_btn = wx.Button(panel, label='check inbox',size=(200,200),pos=(255,200))

        self.Bind(wx.EVT_BUTTON, self.OnButtonClick_send, self.send_btn)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick_inbox , self.inbox_btn)
        self.frame.SetBackgroundColour((100, 179, 179))

        self.start_btn_box = wx.Button(panel, label='inbox',pos=(300,180))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick_inbox, self.start_btn_box)

        self.start_btn_send=wx.Button(panel, label='send',pos=(100,180))

        self.Bind(wx.EVT_BUTTON, self.OnButtonClick_send, self.start_btn_send)

        self.frame.Centre()
        self.frame.Show()


        return True
<<<<<<< HEAD
    def OnButtonClick_send(self,event):
        global frame_state
        frame_state="send mesg"
=======
    def OnButtonClick_inbox(self,event):
>>>>>>> origin/master
        self.frame.Close()
        glo_var.next_frame= "box"


    def OnButtonClick_send(self,event):
        self.frame.Close()
        glo_var.next_frame= "send"


class mesg_box_frame(wx.App):
    def OnInit(self):



<<<<<<< HEAD
    def OnButtonClick_inbox(self,event):
        global frame_state
        frame_state="inbox"
        self.frame.Close()

class inbox_frame(wx.App):
    """Application class."""

    def OnInit(self):

        return True


def main():
    global frame_state
    login_app=LoginFrame()
    login_app.MainLoop()
=======












def main():
  #  login_app=LoginFrame()
   # login_app.MainLoop()
>>>>>>> origin/master

    start_app=start_frame()

    start_app.MainLoop()

    second_app=second_frame()
    second_app.MainLoop()
<<<<<<< HEAD

    if frame_state=="inbox":
        print "in"
    else:
        print "send"
=======
    if glo_var.next_frame=="box":

    else:


>>>>>>> origin/master
if __name__ == '__main__':
    main()
