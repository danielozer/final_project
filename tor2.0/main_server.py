__author__ = "daniel ozer"

from socket import *
import thread
import cPickle as pickle
import secure
import mng_db
from sys import argv
import sys

"""
print 'The length of command line arguments:', len(argv)
print 'Argv 0 :', argv[0]

if len(argv) >=2:
    print 'Argv 1 :', argv[1]

else:
    print 'Got less than 2 parameters at argv'
    sys.exit(0)
"""
file_name="users_data"
#PATHFILE=argv[1]+ '\\' +file_name

BUFFER=2048




col_name_type1 = "Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, SupperUserFlag INT, UserHash TEXT, PasswordHash TEXT"
tbl_name1 = "srvr_users"
# Id, user-ID-name, supper-user-flag, srvr-password-hashed
init_spass_db = (
    (1, 'yaniv nana', 1, -1, -1),
    (2, 'yossi cohen', 1, -1, -1),
    (3, 'miki epstein', 0, -1, -1),
    (4, 'rami verbin', 0, -1, -1),
    (5, 'ziv tepper', 0, -1, -1))



# INTEGER PRIMARY KEY AUTOINCREMENT
# PRIMARY KEY(Name,ApplName)
col_name_type2 = "Id INTEGER PRIMARY KEY AUTOINCREMENT, User_name TEXT,  TEXT, InSystem BOOL, Password TEXT"
tbl_name2 = "server_accsses"
# Id, user-ID-name, appl-name, user-hashed, password-hashed
init_upass_db = (
    (1, 'yaniv nana', 'nana10', -1, -1),
    (2, 'yossi cohen', 'nrg', -1, -1),
    (3, 'miki epstein', 'ynet', -1, -1),
    (4, 'rami verbin', 'themarker', -1, -1),
    (5, 'rami verbin', 'israel hayom', -1, -1),
    (6, 'yaniv nana', 'ynet', -1, -1),
    (7, 'ziv tepper', 'ebay', -1, -1))









def enum(**enums):
    return type('Enum', (), enums)


def create_db_if_not_exist():
    mng_db.init_db()


def handler(clientsock,addr):

    Mesg_Type = enum(ENTER="enter",request="request"   ,request_next_ip="mesg_next" )

    recvdata_order=enum(MESGTYPE=0,SENDER_NAME=1,MESG=2)

    key=secure.create_key()
    pickle_key=secure.Publik_Key(key)
    #send the client the public key
    clientsock.send(pickle_key)
    print "public key sent "

    #recv the public key of the client
    recv_data=clientsock.recv(BUFFER)
    public_key_client=secure.get_public_key_from_other_side(recv_data)


    end=False

    while(end==False):
        recv_data=secure.DecryptMesg(pickle.loads(clientsock.recv(BUFFER)),key)

        recv_data=break_to_pieces(recv_data)

        mesgtype=recv_data[recvdata_order.MESGTYPE]
        mesg_sender_name=recv_data[recvdata_order.SENDER_NAME]
        if (mesgtype==Mesg_Type.ENTER):
            print

        elif (mesgtype==Mesg_Type.request):
            print
        elif(mesgtype==Mesg_Type.request_next_ip):
            print
        else:
            print "error!!!!!!!"
            #error mesg





def break_to_pieces(mesg):
    mesg=mesg.split("|")
    if (mesg[0]==secure.checksum_md5_text(mesg[3])):
        mesg.remove(mesg[0])
        print mesg

        return mesg
    else:
        return "error!!"





def main():
    """
    input: none
    output: none

    the function start a new thread each time a client try to connect to the server
    """


    HOST="127.0.0.1"
    PORT=9999
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)

    while 1:
        print 'waiting for connection... listening on port', PORT
        clientsock, addr = serversock.accept()
        print '...connected from:', addr
        thread.start_new_thread(handler, (clientsock, addr))

if __name__=='__main__':
    main()
