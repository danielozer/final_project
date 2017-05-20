"""
---------------------------------------------------------------
Author          :   Daniel Ozer
Date            :   XXXX
Version         :   1.0
Description     :   the front end show and recv data
---------------------------------------------------------------
"""

#imports

import wx
import db_sqlite_client
import thread
import sys, glob

#imports


#global verials
class glo_var():
    premision=True
    next_frame=4
    send_mesg_type="regular"
    kill=False
    return_to_chFrame=False
    mesg_data=0
    stop_loop=True
    db_data=[]

class glo_current_mesg():
    sender_name=None
    conn_id=None
    recv_date=None
    data=None

def get_all_frontend_data():
    database= "E:\music\client_inter_data.db"


    conn=db_sqlite_client.create_connection(database)
    if conn is not None:

        cur=conn.cursor()
        # create projects table
        check=False
        for row in cur.execute('SELECT * FROM data_for_frontend'):

            print "Row " +row[0]
            glo_var.db_data.insert(len(glo_var.db_data),row[0])
            check=True
        if check:

            cur.execute("DELETE FROM data_for_frontend")
            conn.commit()
        conn.close()


def check_for_answer_pass():
    database= "E:\music\client_inter_data.db"


    check=True
    while check :
        get_all_frontend_data()
        for data in glo_var.db_data:

            if "logging answer" in data:
                check=False

                glo_var.db_data.remove(data)


                if "True" in data:

                    return True

                elif "False" in data:

                    return False


def insert_interanl_data(type,data):
        database= "E:\music\client_inter_data.db"

        if type=="logging":
            data="logging~"+data[0]+"~"+data[1]

        elif type=="request":
            data="request~"+data[0]+"~"+data[1]+"~"+data[2]
        elif type=="reply":
            data="reply~"+data[0]+"~"+data[1]

        print "data : "+data
        db_sqlite_client.insert_msg("reg_internal_backend_db",database,data)



def insert_data_to_glo_current_mesg(data):
    print

class MainFrame(wx.Frame):
    def __init__(self,  parent, id, pos, title, size):

        wx.Frame.__init__(self, parent, id, title, pos, size,)


class loginFrame(wx.App):
    def OnInit(self):

        self.frame = MainFrame(None,-1,wx.DefaultPosition,"Login",(400,300))
        self.panel=wx.Panel(self.frame)

        glo_var.kill=True

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
        UserText = pass_user[0]
        PasswordText = pass_user[1]



        if check_for_answer_pass():
            self.frame.Close()
            glo_var.stop_loop=False
            return True

        wrong_user_name = wx.StaticText(self.panel, -1, "WRONG ",pos=(320,55))
        wrong_user_name.SetForegroundColour((255,0,0))

        wrong_pass = wx.StaticText(self.panel, -1, "WRONG ",pos=(320,92))
        wrong_pass.SetForegroundColour((255,0,0))

        return False
    def OnSubmit(self, event):
        glo_var.kill=False

        UserText = self.txt_Username.GetValue()
        PasswordText = self.txt_Password.GetValue()
        print "user_name: "+str(UserText)
        print "password: "+str(PasswordText)
        combo= (str(UserText),str(PasswordText))
        insert_interanl_data("logging",combo)

        self.check_pass(combo)

        glo_var.kill=False

        glo_var.premision=True



        return True




class start_frame(wx.App):
    """Application class."""

    def OnInit(self):

        self.frame = MainFrame(None, -1, wx.DefaultPosition, "TOR", (500, 500))

        panel = wx.Panel(self.frame)
        box = wx.BoxSizer(wx.VERTICAL)

        glo_var.kill=True

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
        glo_var.kill=False
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




def list_of_name(lst_tpls):
    """
    this func recv list of tuples with all the data of the messesages
    recv: list of tuples
    return:list of senderNames
    """

    arr=[]
    i=0
    for tp in lst_tpls:
        arr.insert(i,"sender_name:  "+tp[0]+ "     "+tp[1]+ "  conn_ID:  "+ tp[2],)
        i+=1

    return arr





def put_values(data_when_click,):
    print
    i=0
    for tp in glo_var.mesg_data:
        line="sender_name:  "+tp[0]+ "     "+tp[1]+ "  conn_ID:  "+ tp[2]
        i+=1
        if data_when_click==line:

            glo_current_mesg.sender_name=tp[0]
            glo_current_mesg.recv_date=tp[1]
            glo_current_mesg.conn_id=tp[2]
            glo_current_mesg.data=tp[3]


class inbox_frame(wx.App):
    """Application class."""

    def OnInit(self):
        glo_var.return_to_chFrame=True
        self.frame = MainFrame(None, -1, wx.DefaultPosition, "TOR", (500, 500))
        panel = wx.Panel(self.frame)


        rev = wx.StaticText(panel, -1, "***INBOX***",(200,40),
                (78, 20))

        rev.SetForegroundColour('white')
        rev.SetBackgroundColour('red')

        database= "E:\music\client_db.db"
        mesg_inbox = db_sqlite_client.get_the_list(database)
        glo_var.mesg_data=mesg_inbox
        inbox_firstfarme_show=list_of_name(mesg_inbox)

        self.listBox = wx.ListBox(panel, -1, (50,70), (400, 300),inbox_firstfarme_show,
                wx.LB_SINGLE,)
        self.listBox.SetSelection(0)
        self.open_btn = wx.Button(panel, label='open mesg',pos=(200,375))

        self.Bind(wx.EVT_BUTTON, self.OnButtonClick_open, self.open_btn)

        self.frame.SetBackgroundColour((100, 179, 179))

        self.frame.Centre()
        self.frame.Show()
        return True
    def OnButtonClick_open(self,event):
        glo_var.return_to_chFrame=False
        put_values( self.listBox.GetString(self.listBox.GetSelection()))
        glo_var.next_frame="show_mesg"
        self.frame.Close()


class send_box(wx.App):
    """Application class."""

    def OnInit(self):
        glo_var.return_to_chFrame=True
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
        glo_var.return_to_chFrame=False
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
            insert_interanl_data("request",[ip,str(secu_lvl),mesg])

        else:
            conn=glo_current_mesg.conn_id
            insert_interanl_data("reply",[conn,mesg])

        print mesg

class see_mesg_box(wx.App):
    """Application class."""

    def OnInit(self):

        glo_var.return_to_chFrame=True
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

        self.see_path_btn = wx.Button(panel, label='see_path',pos=(200,600))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick_see_path, self.see_path_btn)


        self.reply_btn = wx.Button(panel, label='REPLY',pos=(350,600))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick_reply, self.reply_btn)

        self.frame.SetBackgroundColour((100, 179, 179))
        self.frame.Centre()
        self.frame.Show()
        return True

    def OnButtonClick_see_path(self,event):
        glo_var.return_to_chFrame=False
        self.frame.Close()
        glo_var.next_frame="see_path"



    def OnButtonClick_reply(self,event):
        glo_var.return_to_chFrame=False
        self.frame.Close()
        glo_var.next_frame="send_reply"

#have to see if its doesnt hurt the security

class see_send_path(wx.App):
    """Application class."""
    def OnInit(self):
        glo_var.next_frame="show_mesg"
        self.frame = MainFrame(None, -1, wx.DefaultPosition, "TOR", size=wx.DisplaySize())
        panel = wx.Panel(self.frame)

        image_computer="computerIcon.png"
        image_right="right.png"
        path_ips=["129m120","192.90.09.00","129m120","192.90.09.00","129m120","192.90.09.00","192.90.09.00","129m120","192.90.09.00","129m120","192.90.09.00"]



        il = wx.ImageList(100,100, True)
        for ip in path_ips:




            bmp_right = wx.Bitmap(image_right, wx.BITMAP_TYPE_PNG)
            bmp_computer = wx.Bitmap(image_computer, wx.BITMAP_TYPE_PNG)
            il_max = il.Add(bmp_computer)
            il_max = il.Add(bmp_right)




        # create the list control
        self.list = wx.ListCtrl(self.frame, -1,
                style=wx.LC_ICON | wx.LC_AUTOARRANGE,size=wx.DisplaySize())

        # assign the image list to it
        self.list.AssignImageList(il, wx.IMAGE_LIST_NORMAL)

        # create some items for the list
        counter=0
        for x in range(2*len(path_ips)):
            img = x % (il_max+1)
            if x%2==0:
                self.list.InsertImageStringItem(x,str(path_ips[counter]), img)
                counter+=1
            else:
                if x!=2*len(path_ips)-1:
                    self.list.InsertImageStringItem(x,"", img)


        ##actully dont do nothing but some how it keeps from the program to break down
        self.nothing_btn = wx.Button(panel, label='',pos=(0,0))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick_nothing , self.nothing_btn)
        ##actully dont do nothing but some how it keeps from the program to break down



        self.frame.Show()

        return True

    def OnButtonClick_nothing(self,event):
        pass
        ##actully dont do nothing but some how it keeps from the program to break down



class error(wx.App):
    """Application class."""
    def OnInit(self):

        self.frame = MainFrame(None, -1, wx.DefaultPosition, "T3R", size=(300,300))
        panel = wx.Panel(self.frame)


        lbl1 = wx.StaticText(panel,-1, style = wx.ALIGN_CENTER | wx.ST_ELLIPSIZE_MIDDLE,pos=(0,75))
        lbl1.SetLabel("error \n something went wrong ")
        lbl1.SetForegroundColour((255,0,0))
        lbl1.SetBackgroundColour((0,0,0))
        font = lbl1.GetFont()
        font.SetPointSize(20)
        lbl1.SetFont(font)


        self.frame.SetBackgroundColour((100, 179, 179))
        self.frame.Centre()
        self.frame.Show()
        return True


def main(one,teo):


        login_app=loginFrame()
        login_app.MainLoop()


        while glo_var.stop_loop==False:

            if glo_var.premision and glo_var.kill==False:

                glo_var.stop_loop=True

                start_app=start_frame()
                start_app.MainLoop()


                counter=0
                while glo_var.kill==False:

                    print str(counter)
                    counter+=1

                    if glo_var.next_frame=="send_reply" and glo_var.return_to_chFrame==False:

                        send_app=send_box()
                        send_app.MainLoop()

                    elif glo_var.next_frame== "show_mesg" and glo_var.return_to_chFrame==False:

                        see_mesg_app=see_mesg_box()
                        see_mesg_app.MainLoop()

                    elif glo_var.next_frame== "see_path" and glo_var.return_to_chFrame==False:

                        path_app=see_send_path()
                        path_app.MainLoop()

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
    main(1,1)
