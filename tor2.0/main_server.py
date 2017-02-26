
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
col_name_type2 = "Id INTEGER PRIMARY KEY AUTOINCREMENT, User_name TEXT, password TEXT, InSystem TEXT,ID_of_single_conn TEXT"
tbl_name2 = "server_accsses"
# Id, user-ID-name, appl-name, user-hashed, password-hashed
init_upass_db = (
    (1, 'daniel', '1', False, -1),
    (2, 'e', '2', False, -1),
    (3, 'r', '3', False, -1),
    (4, 't', '4', False, -1),
    (5, 'y', '5', False, -1),
    (6, 'u', '6', False, -1),
    (7, 'i', '7', False, -1))



def change_dic(dic,id):
    """
    this func recv dicintionary exmp{1:IP} and int id ,it return the dic without the specif id (index) and the ids is sort by value
    input: dic dic_client[int : string (ip)],int id
    output:  dic [int : string (ip)]
    """

    for key in dic.keys():

        if key == id:
			del dic[key]


        elif key >id:

            dic[key-1] = dic.pop(key)


def put_in_id( dic, value1):

    dic_length = len(dic)
    index = {dic_length+1: value1}
    dic.update(index)


def take_out_id( dic, value1):


    for key, value in dic.iteritems():
        if value == value1:

            lKey=key
            break

    del dic[lKey]

    change_dic(dic,lKey)





def create_path_for_mesg(dic_client1,rounds):
    """
    this func recv dicintionary exmp{1:IP} and int rounds , it return an array of of the ips that is hte path of the mesg
    input: dic dic_client[int : string (ip)],int rounds
    output: array of string (ips)
    """

    dic_client = dic_client1.copy()
    reverse = False
    dic_length = len(dic_client)
    array_path = []
    counter = dic_length
    return_val = 0

    for n in range(0, rounds):

        random_id=random.randint(1, counter)


        array_path=array_path+[dic_client[random_id]]

        last_random_val=dic_client[random_id]

        change_dic(dic_client,random_id)

        counter=counter-1

        if reverse==True:

            reverse=False
            counter=dic_length-1

            put_in_id(dic_client,return_val)


        if counter==0:
            counter =dic_length-1

            reverse=True
            dic_client=dic_client1.copy()
            return_val=last_random_val

            take_out_id(dic_client,last_random_val)

    return array_path





def enum(**enums):
    return type('Enum', (), enums)


def create_db_if_not_exist(fname):
    mng_db.init_db(fname)



db_path = r'E:\music'
db_fname = 'userpass.db'
db_path_fname = db_path + '\\' + db_fname

create_db_if_not_exist(db_path_fname)

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
"""
if __name__=='__main__':
    main()
"""
