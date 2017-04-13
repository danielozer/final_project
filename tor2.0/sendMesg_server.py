_author__ = "daniel ozer"
import wx


#global verials
class glo_var():
    next_frame=4
    send_mesg_type="regular"
    kill=False
class glo_current_mesg():
    sender_name=None
    conn_id=None
    recv_date=None
    data="shfijsdbfijahfosdhfdsjaoidfsfsjfklsnflkjsflkgkdjnglfsgkjfd \n gkdfngkdjfngkdfjgkfdjgnkdjbkdfjgkjfdgndfkjgbkdfljsgbslkjgbbd"

class MainFrame(wx.Frame):
    def __init__(self,  parent, id, pos, title, size):

        wx.Frame.__init__(self, parent, id, title, pos, size)


class LoginFrame(wx.App):
    def OnInit(self):

        self.frame = MainFrame(None,-1,wx.DefaultPosition,"Login",(400,300))

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


        glo_var.kill=True
        self.frame = MainFrame(None, -1, wx.DefaultPosition, "TOR", (500, 500))

        panel = wx.Panel(self.frame)



        rev = wx.StaticText(panel, -1, "choose your option",(180, 70),
                (110, 20))

        rev.SetForegroundColour('white')
        rev.SetBackgroundColour('red')


        self.send_btn = wx.Button(panel, label='send mesg',size=(200,200),pos=(45,200))
        self.inbox_btn = wx.Button(panel, label='check inbox',size=(200,200),pos=(255,200))


        self.Bind(wx.EVT_BUTTON, self.OnButtonClick_send, self.send_btn)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick_inbox , self.inbox_btn)

        self.frame.SetBackgroundColour((100, 179, 179))

        self.frame.Centre()
        self.frame.Show()


        return True


    def OnButtonClick_inbox(self,event):
        glo_var.kill=False
        self.frame.Close()
        glo_var.send_mesg_type="reply"
        glo_var.next_frame= "box"


    def OnButtonClick_send(self,event):
        glo_var.kill=False
        self.frame.Close()
        glo_var.send_mesg_type="regular"
        glo_var.next_frame= "send"






class inbox_frame(wx.App):
    """Application class."""

    def OnInit(self):

        self.frame = MainFrame(None, -1, wx.DefaultPosition, "TOR", (500, 500))
        panel = wx.Panel(self.frame)


        rev = wx.StaticText(panel, -1, "***INBOX***",(200,40),
                (78, 20))

        rev.SetForegroundColour('white')
        rev.SetBackgroundColour('red')


        sampleList = ['zero        sdfsdfjsd j     sdfslf ksdlf                     asdsdasda        asadafsdfsdfdfsdfsdf', 'one  fsdfsdfs    fffddds', 'two', 'three', 'four', 'five',
                      'six', 'seven', 'eight', 'nine', 'ten', 'eleven',
                      'twelve', 'thirteen', 'fourteen','six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'thirteen', 'fourteen','six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'thirteen', 'fourteen','six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'thirteen', 'fourteen','six', 'seven', 'eight', 'nine', 'ten', 'eleven']

        self.listBox = wx.ListBox(panel, -1, (50,70), (400, 300), sampleList,
                wx.LB_SINGLE,)
        self.listBox.SetSelection(0)
        self.open_btn = wx.Button(panel, label='open mesg',pos=(200,375))

        self.Bind(wx.EVT_BUTTON, self.OnButtonClick_open, self.open_btn)

        self.frame.SetBackgroundColour((100, 179, 179))

        self.frame.Centre()
        self.frame.Show()
        return True
    def OnButtonClick_open(self,event):
        print self.listBox.GetString(self.listBox.GetSelection())
        glo_var.next_frame="show_mesg"
        self.frame.Close()


class send_box(wx.App):
    """Application class."""

    def OnInit(self):

        self.frame = MainFrame(None, -1, wx.DefaultPosition, "TOR", (700, 700))
        panel = wx.Panel(self.frame)

        lbl1 = wx.StaticText(panel,-1, style = wx.ALIGN_CENTER | wx.ST_ELLIPSIZE_MIDDLE,pos=(280,50))
        lbl1.SetLabel("SEND BOX")
        lbl1.SetForegroundColour((255,0,0))
        lbl1.SetBackgroundColour((0,0,0))
        font = lbl1.GetFont()
        font.SetPointSize(20)
        lbl1.SetFont(font)


        if glo_var.send_mesg_type=="regular":

            self.ip_ = wx.StaticText(panel, -1, "IP:",pos=(30,130))
            self.ip_text = wx.TextCtrl(panel, pos=(170,130),)

            self.select_txt = wx.StaticText(panel, -1, "selct security level:",pos=(30,190))
            self.select_choice=wx.Choice(panel, -1, (170, 190), choices=["LOW","MEDIUM","HIGH"])


        self.write_mesg = wx.StaticText(panel, -1, "write your mesg here:",pos=(30,250))
        self.mesg = wx.TextCtrl(panel, pos=(170,260),size=(250,300),style=wx.TE_MULTILINE)

        self.sumbit_btn = wx.Button(panel, label='SUMBIT',pos=(290,600))

        self.Bind(wx.EVT_BUTTON, self.OnButtonClick_sumbit, self.sumbit_btn)


        self.frame.SetBackgroundColour((100, 179, 179))
        self.frame.Centre()
        self.frame.Show()
        return True


    def OnButtonClick_sumbit(self,event):
        self.frame.Close()
        mesg=self.mesg.GetValue()
        glo_var.next_frame="regular"
        if glo_var.send_mesg_type=="regular":
            ip=self.ip_text.GetValue()
            choice=self.select_choice.GetString(self.select_choice.GetSelection())

            secu_lvl=4

            if choice=="HIGH":
                secu_lvl=16
            elif choice=="MEDIUM":
                secu_lvl=8


            print ip
            print secu_lvl

        else:
            conn=glo_current_mesg.conn_id


        print mesg

class see_mesg_box(wx.App):
    """Application class."""

    def OnInit(self):

        self.frame = MainFrame(None, -1, wx.DefaultPosition, "TOR", (700, 700))
        panel = wx.Panel(self.frame)

        lbl1 = wx.StaticText(panel,-1, style = wx.ALIGN_CENTER | wx.ST_ELLIPSIZE_MIDDLE,pos=(280,50))
        lbl1.SetLabel("MESSAGE")
        lbl1.SetForegroundColour((255,0,0))
        lbl1.SetBackgroundColour((0,0,0))
        font = lbl1.GetFont()
        font.SetPointSize(20)
        lbl1.SetFont(font)

        self.sender_txt    = wx.StaticText(panel,-1,    "sender name     :    "+str(glo_current_mesg.sender_name),pos=(30,150))
        self.connection_id = wx.StaticText(panel,-1,    "connection id   :    "+str(glo_current_mesg.conn_id),pos=(30,190))
        self.recv_date     = wx.StaticText(panel,-1,    "receive date      :    "+str(glo_current_mesg.recv_date),pos=(30,230))
        self.data          = wx.StaticText(panel,-1,    "data                   :    ",pos=(30,280))

        self.contents = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY, pos=(120,280),size=(450,300))
        self.contents.SetValue(str(glo_current_mesg.data))

        self.reply_btn = wx.Button(panel, label='REPLY',pos=(290,600))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick_reply, self.reply_btn)

        self.frame.SetBackgroundColour((100, 179, 179))
        self.frame.Centre()
        self.frame.Show()
        return True
    def OnButtonClick_reply(self,event):
        self.frame.Close()
        glo_var.next_frame="send_reply"

#have to see if its doesnt hurt the security

class see_send_path(wx.App):
    """Application class."""
    def OnInit(self):

        self.frame = MainFrame(None, -1, wx.DefaultPosition, "TOR", size=wx.DisplaySize())
        panel = wx.Panel(self.frame)
        dir="--->"

        imageFile="computerIcon.png"
        path_ips=[]
        for ip in path_ips:

            image = wx.Image(imageFile, wx.BITMAP_TYPE_PNG)
            temp = image.ConvertToBitmap()
            size = temp.GetWidth(), temp.GetHeight()
            self.bmp = wx.StaticBitmap(parent=self.frame, bitmap=temp,pos=(100,100))

        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True





def main():


    login_app=LoginFrame()
    login_app.MainLoop()
    start_app=start_frame()
    start_app.MainLoop()

    glo_var.kill=False

    while glo_var.kill==False:
        if glo_var.next_frame=="send_reply":
            send_app=send_box()
            send_app.MainLoop()

        elif glo_var.next_frame== "show_mesg" :
            see_mesg_app=see_mesg_box()
            see_mesg_app.MainLoop()
        else:
            second_app=second_frame()
            second_app.MainLoop()
            if glo_var.next_frame == "box" and glo_var.kill==False:
                inbox_app=inbox_frame()
                inbox_app.MainLoop()


            elif glo_var.kill==False:

                send_app=send_box()
                send_app.MainLoop()

if __name__ == '__main__':
    main()