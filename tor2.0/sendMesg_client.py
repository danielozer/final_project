"""
---------------------------------------------------------------
Author          :   Daniel Ozer
Date            :   XXXX
Version         :   1.0
Description     :   all the function the client use for sending messeges for the server or to other client
---------------------------------------------------------------
"""

#imports

import secure
import socket
import cPickle as pickle

#imports




def send_to_server_data(user_data,sock,key,sender_name):
    """
    this func recv the string of data of the user and send it to the server after it encrypt(using secure moudle)
    recv: string of data of the user,socket
    return:non
    """

    sock.send(create_mesg(user_data,"create_new_account",sender_name,key))

def send_to_server_password(str_password,sock,sender_name,key):

    """
    this func recv the string passwords and username  and send it to the server after it encrypt(using secure moudle)
    recv: string of password, socket
    return:non
    """
    sock.send(create_mesg(str_password,"enter",sender_name,key))

def send_to_server_sendRequest(ip,sock,key,):
    """
    this func recv the string mesg  and send it to the server after it encrypt(using secure moudle)
    recv: str mesg, socket
    return:non
    """
    sock.send(create_mesg(ip,"request","req_xxx",key))

def ask_what_next(mesg,sock,sender_name,key):


    sock.send(create_mesg(mesg,"mesg_next",sender_name,key))

def send_mesg_to_client(ip,mesg):

    PORT=8888
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, PORT))
    sock.send(mesg)

def create_mesg(mesg,type,sender_name,key):

    checksum=secure.checksum_md5_text(mesg)
    send_message=checksum+"|"+type+"|"+sender_name+"|"+mesg

    print "send msg  ; "+send_message

    enc_data=pickle.dumps(secure.EncryptMesg(str(send_message),key))
    print enc_data
    return  enc_data
