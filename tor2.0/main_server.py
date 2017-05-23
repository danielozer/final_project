"""
---------------------------------------------------------------
Author          :   Daniel Ozer
Date            :   XXXX
Version         :   1.0
Description     :   the server back-end (the brain)
---------------------------------------------------------------
"""

#imports

from socket import *
import thread
from threading import Thread
import cPickle as pickle
import secure
import string
from sys import argv
import sys
import random,time
import db_sqlite_server

#imports

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




class glo_var():
        #msg_arr=[]
        server_key=""
        #client_public_key=""
        server_public_key=""

        #pickle_client_public_key=""
        all_smg_arr_with_data=[]#array of array [client_ip,client_public_key,pickle_client_public_key,msg_arr]


BUFFER=2048

def get_password_from_db():
    conn=db_sqlite_server.create_connection( "E:\music\server_db.db")
    cur=conn.cursor()
    data=[]
    for row in cur.execute('SELECT * FROM passwords '):
            data.insert(len(data),row)
    conn.close()
    print
    return data


def check_passwords(user_name,password):

    data=get_password_from_db()
    for d in data:

        true_user_name=d[1]
        true_password=d[2]

        if (true_password==password and true_user_name==user_name):
            return True

    return False

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







def handler(clientsock,addr):


    Mesg_Type = enum(ENTER="enter",request="request"   ,request_next_ip="mesg_next",path_request="path",reply="reply" )

    recvdata_order=enum(MESGTYPE=0,SENDER_NAME=1,MESG=2)

    key=secure.create_key()
    pickle_key=secure.Public_Key(key)
    #send the client the public key
    clientsock.send(pickle_key)
    print "public key sent "

    #recv the public key of the client
    recv_data=clientsock.recv(BUFFER)
    pickle_client_public_key=recv_data
    client_public_key=secure.get_public_key_from_other_side(recv_data)

    print "###############################################################"
    print client_public_key
    print "###############################################################"

    glo_var.all_smg_arr_with_data.insert(len(glo_var.all_smg_arr_with_data),[addr[0]],client_public_key,pickle_client_public_key,[])

    t = Thread(target=handler_client_only_send, args=(1,))
    t.start()

    end=False

    while(end==False):


        recv_data=secure.DecryptMesg(pickle.loads(clientsock.recv(BUFFER)),key)

        recv_data=break_to_pieces(recv_data)
        mesgtype=recv_data[recvdata_order.MESGTYPE]
        mesg_sender_name=recv_data[recvdata_order.SENDER_NAME]
        if (mesgtype==Mesg_Type.ENTER):
            sp_data=recv_data[2].split("~")

            if (check_passwords(sp_data[0],sp_data[1])):
                conn=db_sqlite_server.create_connection( "E:\music\server_db.db")
                cur=conn.cursor()

                cur.execute("UPDATE passwords SET ip=? WHERE user_name=? AND password=?", (addr[0], sp_data[0],sp_data[1]))
                cur.execute("UPDATE passwords SET pu_key=? WHERE user_name=? AND password=?", (glo_var.pickle_client_public_key, sp_data[0],sp_data[1]))
                conn.commit()
                conn.close()


                glo_var.msg_arr.insert(len(glo_var.msg_arr),"logging answer "+"True")
            else:

                glo_var.msg_arr.insert(len(glo_var.msg_arr),"logging answer "+"False")

        elif (mesgtype==Mesg_Type.request):
            ips={}
            sp_data=recv_data[2].split("~")
            print "sp_data : "+str(sp_data)

            count=0
            target_ip=sp_data[0]
            rounds=sp_data[1]
            uniq_id=sp_data[2]
            check=False
            pu_key_target=""

            for ip_db in get_password_from_db():


                if (ip_db[0] != None and ip_db[0]!=target_ip and ip_db[0]!=addr[0]):
                    count+=1
                    print count
                    ips.update({count:ip_db[0]})
                else:
                    if ip_db[0]==target_ip:
                        check=True
                        pu_key_target=ip_db[3]
            print "ipssss : "+str(ips)

            if check:

                path=create_path_for_mesg(ips,int(rounds))
                path.insert(0,addr[0])
                path.insert(len(path),target_ip)

                print "path " + str(path)

                conn=db_sqlite_server.create_connection( "E:\music\server_db.db")
                cur=conn.cursor()

                nxt_ip=path[1]
                cur.execute("INSERT INTO ips_conn_id  VALUES (?,?,?,?,?)",(addr[0],target_ip,uniq_id,str(path),nxt_ip,))
                conn.commit()
                conn.close()

                print "pu "+pu_key_target

                glo_var.msg_arr.insert(len(glo_var.msg_arr),"req_answer~"+"yes~"+str(nxt_ip)+"~"+str(pu_key_target)+"~"+str(uniq_id))
            else:
                glo_var.msg_arr.insert(len(glo_var.msg_arr),"req_answer~no~xxx~xxx~"+str(uniq_id))

        elif(mesgtype==Mesg_Type.reply):
            id_conn=recv_data[2]
            p=get_path_by_id(id_conn)
            target_ip=p[1]
            path=list(reversed(p[0]))
            nxt_ip=path[1]


            pu_key_target=""

            for ip_db in get_password_from_db():


                if (ip_db[0] != None and ip_db[0]!=target_ip and ip_db[0]!=addr[0]):
                    count+=1
                    print count
                    ips.update({count:ip_db[0]})
                else:
                    if ip_db[0]==target_ip:

                        pu_key_target=ip_db[3]

            conn=db_sqlite_server.create_connection( "E:\music\server_db.db")
            cur=conn.cursor()

            cur.execute("UPDATE ips_conn_id SET path=? AND nxt_ip=? WHERE conn_id=?", (path,nxt_ip ,id_conn))

            conn.close()

            glo_var.msg_arr.insert(len(glo_var.msg_arr),"req_answer~"+"yes~"+str(nxt_ip)+"~"+str(pu_key_target)+"~"+str(uniq_id))

        elif(mesgtype==Mesg_Type.request_next_ip):
            print

        elif (mesgtype==Mesg_Type.path_request):
            id_conn=recv_data[2]
            path=get_path_by_id(id_conn)

            glo_var.msg_arr.insert(len(glo_var.msg_arr),"get_path~"+str(path))


        else:
            print "error!!!!!!!"
            #error mesg

def get_path_by_id(conn_id):

    conn=db_sqlite_server.create_connection( "E:\music\server_db.db")
    cur=conn.cursor()

    data=[]
    for row in cur.execute('SELECT * FROM ips_conn_id '):

            if row[2]==conn_id:
                conn.close()
                return (row[3],row[1])

    conn.close()
    return False

def break_to_pieces(mesg):
    mesg=mesg.split("|")
    if (mesg[0]==secure.checksum_md5_text(mesg[3])):
        mesg.remove(mesg[0])
        print mesg

        return mesg
    else:
        return "error!!"

def handler_client_only_recv (ip):
    while 1:
        try:

            port=9393
            ip="127.0.0.1"

            sock = socket(AF_INET,SOCK_STREAM)

            sock.connect((ip, port))

            while 1:
                sock.send("opsaaaaa")

                time.sleep(5)
        except:
            p=1

def handler_client_only_send (ip):
    while 1:
        try:

            port=9393
            ip="127.0.0.1"

            sock = socket(AF_INET,SOCK_STREAM)

            sock.connect((ip, port))
            check_for_timming_del=False
            while 1:
                #lock

                for msg in glo_var.msg_arr:
                    print len(msg)
                    if len(msg)>128:
                        print "IN"
                        blocks=secure.cut_for_blocks(msg)
                        first_msg=str(len(blocks))+" blocks"
                        print first_msg
                        enc_data=pickle.dumps(secure.EncryptMesg(first_msg,glo_var.client_public_key))
                        print "enc : "+str(enc_data)
                        sock.send(enc_data)

                        for b in blocks:
                            print "b : "+b
                            enc_data=pickle.dumps(secure.EncryptMesg(b,glo_var.client_public_key))
                            time.sleep(0.1)
                            sock.send(enc_data)

                    else:

                        enc_data=pickle.dumps(secure.EncryptMesg(msg,glo_var.client_public_key))

                        sock.send(enc_data)
                        print "send"
                    check_for_timming_del=True
                if check_for_timming_del:
                    check_for_timming_del=False
                    glo_var.msg_arr=[]


        except:
            print "errorororo"
            p=1


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
