__author__ = "daniel ozer"

from socket import *
import thread,threading
from Crypto.PublicKey import RSA
from Crypto import Random
import cPickle as pickle
import sys
from sys import argv
import secure



BUFFER=2048
def enum(**enums):
    return type('Enum', (), enums)


def handler(clientsock,addr):

    Mesg_Type = enum(ENTER="enter",request="request"   ,request_next_ip="mesg_next" )

    recvdata_order=enum(MESGTYPE=0,SENER_NAME=1,MESG=2)

    key=secure.create_key()
    public_key=secure.Publik_Key(key)
    #send the client the public key
    clientsock.send(public_key)
    print "public key sent "
    #recv the public key of the client
    recv_data=clientsock.recv(BUFFER)

    public_key_client=secure.DecryptMesg(recv_data,key)
    print public_key_client

    end=False

    while(end==False):
        recv_data=secure.DecryptMesg(clientsock.recv(BUFFER),key)

        recv_data=break_to_pieces(recv_data)

        mesgtype=recv_data[recvdata_order.MESGTYPE]

        if (mesgtype==Mesg_Type.ENTER):
            print

        elif (mesgtype==Mesg_Type.request):
            print
        elif(mesgtype==Mesg_Type.request_next_ip):
            print
        else:
            print "error!!!!!!!"
            #error mesg




    """
    client_public_key=clientsock.recv(BUFFER)
    client_public_key=secure.DecryptMesg(client_public_key,key)

    print "\n\n\n\n\n\n\n\n\n"
    print client_public_key
    print "\n\n\n\n\n\n\n\n\n"
    user_data=secure.DecryptMesg(clientsock.recv(BUFFER),key)
    print "$$$$$$$$"+user_data
    """





def break_to_pieces(mesg):
    mesg=mesg.split("|")
    if (mesg[0]==secure.checksum_md5_text(mesg[3])):
        mesg.remove(mesg[0])

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
