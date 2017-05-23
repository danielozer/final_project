"""
---------------------------------------------------------------
Author          :   Daniel Ozer
Date            :   XXXX
Version         :   1.0
Description     :   the client back-end (the brain)
---------------------------------------------------------------
"""

#imports

import secure
import sendMesg_client
from socket import *
import thread
from threading import Thread
import threading,time
import db_sqlite_client
import cPickle as pickle
import string
import random
#imports

IP="127.0.0.1"
PORT=9999
BUFFER=2048
SENDER_NAME="DONI"


arr_mesg_lock=threading.Lock()

class user_data:


        client_key=""
        client_public_key=""
        server_public_key=""
        loggin=False#true \ false
        mesg_for_send=[] #an array of all the mesg that need  to sent (the mesg is already ready to be send as is.)
        recv_mesg=[]#an array of all the mesg that recieved from the main server
        mesg_for_next_ip=[]




def insert_interanl_data(data):

    database= "E:\music\client_inter_data.db"
    if "logging" in data:

        db_sqlite_client.insert_msg("reg_internal_frontend_db",database,data)

    elif "get_path" in data:
        db_sqlite_client.insert_msg("reg_internal_frontend_db",database,data)

    elif "req_answer" in data :
        print "food"
        db_sqlite_client.insert_msg("reg_internal_backend_db",database,data)

    elif "relpy" in data :
        db_sqlite_client.insert_msg("reg_internal_backend_db",database,data)

    elif "mesg_next" in data :
        db_sqlite_client.insert_msg("reg_internal_backend_db",database,data)

    elif "mesg" in data:
        db_sqlite_client.insert_msg("mesg_db",database,data)
def main(one,tep):



    key=secure.create_key()
    public_key=secure.Public_Key(key)

    user_data.client_key=key
    user_data.client_public_key=public_key

    port=9999
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((IP, port))

    pu_key=sock.recv(BUFFER)
    user_data.server_public_key=secure.get_public_key_from_other_side(pu_key)


    print len(user_data.client_public_key)
    sock.send(user_data.client_public_key)

    print "###############################################################"
    print user_data.server_public_key
    print "###############################################################"
    print user_data.client_public_key

    print "###############################################################"

    print

    p = Thread(target=handler_server_only_from_server, args=(user_data,))
    p.start()
    t = Thread(target=handler_client_with_server, args=(user_data,sock))
    t.start()


    #thread.start_new_thread(handler_client_with_server, (user_data,))
    #thread.start_new_thread(handler_server_only_from_server, (user_data,))
    #port=1901
    #thread.start_new_thread(client_server_other_clients, (user_data,port))


def client_to_other_clients_recv():
    port =8888
    host="127.0.0.1"
    ADDR = (host, port)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    while 1:
        print 'waiting for connection... listening on port', PORT
        clientsock, addr = serversock.accept()
        print '...connected from:', addr

        all_string=""

        recv_data=clientsock.recv(BUFFER)
        if "blocks" in recv_data:

            sp=recv_data.split(" ")
            times=int(sp[0])


            for part in range(0,times):
                recv_data=clientsock.recv(BUFFER)
                all_string=all_string+recv_data

        else:

            all_string=recv_data

        recv_data=clientsock.recv(BUFFER)

        insert_interanl_data("mesg_next~"+all_string+"~"+recv_data)

def client_server_recv(clientsock):
    #c-server-->c-client

    check_for_multi=False
    counter=0
    times=-1
    while 1:
        recv_data=0
        r=clientsock.recv(BUFFER)
        print "r"
        recv_data=secure.DecryptMesg(pickle.loads(r),user_data.client_key)
        if "blocks" in recv_data:

            sp=recv_data.split(" ")
            times=int(sp[0])
            all_string=""
            counter=0
            check_for_multi=True

        elif   check_for_multi:

            all_string=all_string+recv_data

            counter+=1
            if counter==times:
                times=-1
                counter=0
                check_for_multi=False

                recv_data=all_string

        print "recv  : "+recv_data
        if check_for_multi==False:

            insert_interanl_data(recv_data)

        #insert it to database

def client_server_other_clients(user_data,port):
    #c-server-->c-client

    #the main server send the port that need to be used

    port =9899
    host="127.0.0.1"
    ADDR = (host, port)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)


    print 'waiting for connection... listening on port', PORT
    clientsock, addr = serversock.accept()
    print '...connected from:', addr

    while 1:
        recv=clientsock.recv(BUFFER)
        #put the recv in some db

def put_mesg_for_send():

    database= "E:\music\client_inter_data.db"
    conn=db_sqlite_client.create_connection(database)
    data=[]


    if conn is not None:
        cur=conn.cursor()
        check_for_timming_del=False
        for row in cur.execute('SELECT * FROM data_for_backend'):

            print row
            check_for_timming_del=True
            data.insert(len(data),row)
        if check_for_timming_del:
            cur.execute("delete from data_for_backend ")
            conn.commit()
    conn.close()
    correct_data=[]
    for d in data:


        correct_data.insert(len(correct_data),d[0])

    arr=user_data.mesg_for_next_ip
    user_data.mesg_for_next_ip=[]

    for msg in arr:

            correct_data.insert(len(correct_data),msg)

    return correct_data


def find_var_in_aar_tuples(arr,var):
    for t in arr:
        for i in t:
            if i==var:

                return t
    return "none"
def handler_client_with_server(user_data,sock):

    wait_arr_msg=[]#build from tuples that conatain all the data

    print "handler_client_with_server"
    while 1:
        arr_msg=put_mesg_for_send()
        #need to put lock
        for msg in arr_msg:
            if len(arr_msg)>0:

                arr_mesg_lock.acquire()

                pull_next_mesg=msg


                if "~" in pull_next_mesg:
                    pull_next_mesg =pull_next_mesg.split("~")
                if "logging" in pull_next_mesg[0]:


                    sendMesg_client.send_to_server_password(pull_next_mesg[1]+"~"+pull_next_mesg[2],sock,"enter_sender",user_data.server_public_key)
                elif "request" in pull_next_mesg[0]:

                    uniq_id=''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
                    wait_arr_msg.insert(len(wait_arr_msg),(pull_next_mesg[3],uniq_id))
                    print "wait: "+str(wait_arr_msg)
                    sendMesg_client.send_to_server_sendRequest(pull_next_mesg[1]+'~'+pull_next_mesg[2]+"~"+uniq_id,sock,user_data.server_public_key)

                elif "req_answer" in pull_next_mesg[0]:

                    if "no" in pull_next_mesg[1]:
                        msg_id=pull_next_mesg[4]
                        tup=find_var_in_aar_tuples(wait_arr_msg,msg_id)
                        wait_arr_msg.remove(tup)

                    elif "yes" in pull_next_mesg[1]:
                        nxt_ip=pull_next_mesg[2]
                        pu_key=pull_next_mesg[3]

                        pu_key=secure.get_public_key_from_other_side(str(pu_key))
                        msg_id=pull_next_mesg[4]

                        tup=find_var_in_aar_tuples(wait_arr_msg,msg_id)
                        wait_arr_msg.remove(tup)



                        if len(tup[0])>128:

                            blocks=secure.cut_for_blocks(tup[0])
                            first_msg=str(len(blocks))+" blocks"

                            enc_b=[]
                            for b in blocks:
                                enc_b.insert(len(enc_b),secure.EncryptMesg(b,pu_key))

                            msg=[first_msg]+enc_b
                            sendMesg_client.send_mesg_to_client(nxt_ip,msg,"blocks",msg_id)

                        else:
                            mesg_for_send=secure.EncryptMesg(tup[0],pu_key)
                            sendMesg_client.send_mesg_to_client(nxt_ip,msg,"reg",msg_id)



                elif "reply" in pull_next_mesg[0]:
                    print pull_next_mesg[0]
                    print pull_next_mesg[1]
                    print pull_next_mesg[2]

                    wait_arr_msg.insert(len(wait_arr_msg),(pull_next_mesg[2],pull_next_mesg[1]))
                    sendMesg_client.send_to_server_sendRequest_reply(pull_next_mesg[1],sock,SENDER_NAME,user_data.server_public_key)

                elif "mesg_next" in pull_next_mesg[0]:
                    sendMesg_client.ask_what_next(pull_next_mesg[0],sock,pull_next_mesg[1],pull_next_mesg[2],user_data.server_public_key)

                elif "see_path" in pull_next_mesg[0]:
                    sendMesg_client.send_to_server_sendRequest_reply(pull_next_mesg[1],sock,SENDER_NAME,user_data.server_public_key)


                arr_mesg_lock.release()
                time.sleep(0.1)

def handler_server_only_from_server(user_data):
    #c-server-->s-client
    #act as a server for reciving#need to get the port from the server

    port=9393

    host="127.0.0.1"
    ADDR = (host, port)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)

    while 1:
        print 'waiting for connection... listening on port', port
        clientsock, addr = serversock.accept()
        print '...connected from:', addr
        thread.start_new_thread(client_server_recv, (clientsock,))






if __name__=='__main__':
    main(1,1)
