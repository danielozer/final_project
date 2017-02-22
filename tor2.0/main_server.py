
__author__ = "daniel ozer"

from socket import *
import thread
import cPickle as pickle
import secure
import mng_db
from sys import argv
import sys
import random

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
col_name_type2 = "Id INTEGER PRIMARY KEY AUTOINCREMENT, User_name TEXT, password TEXT, InSystem BOOL,ID_of_single_conn TEXT"
tbl_name2 = "server_accsses"
# Id, user-ID-name, appl-name, user-hashed, password-hashed
init_upass_db = (
    (1, 'daniel', 'nana10', -1, -1),
    (2, 'yossi cohen', 'nrg', -1, -1),
    (3, 'miki epstein', 'ynet', -1, -1),
    (4, 'rami verbin', 'themarker', -1, -1),
    (5, 'rami verbin', 'israel hayom', -1, -1),
    (6, 'yaniv nana', 'ynet', -1, -1),
    (7, 'ziv tepper', 'ebay', -1, -1))




def change_dic(dic,id):
    """
    this func recv dicintionary exmp{1:IP} and int id ,it return the dic that nees
    input: dic dic_client[int : string (ip)],int id
    output:  dic [int : string (ip)]
    """

    for key in dic:
        if key==id:
            v=dic[key]
            dic[v]=0
        elif key>id:
            v=dic[key]
            dic[v]=dic[v]-1

    return dic

def change_id_(dic,id,value):
    index = {id:value}
    dic.update(index)

    return dic


def create_path_for_mesg(dic_client,rounds):
    """
    this func recv dicintionary exmp{1:IP} and int rounds , it return an array of of the ips that is hte path of the mesg
    input: dic dic_client[int : string (ip)],int rounds
    output: array of string (ips)
    """

    original_dic=dic_client
    reverse=False
    dic_length=len(dic_client)
    array_path=[]
    counter=dic_length
    for n in range(0, rounds):
        random_id=random.randint(0, counter)
        array_path=array_path+[dic_client[random_id]]
        if reverse==True:
            reverse=False
            counter=dic_length



        counter=counter-1

        if counter==0:
            counter =dic_length-1
            reverse=True



    return array_path


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
