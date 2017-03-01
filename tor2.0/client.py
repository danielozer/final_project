__author__ ="daniel ozer"
import secure
import sendMesg_client
#import show_page
import socket
import cPickle as pickle
import thread
import threading


IP="127.0.0.1"
PORT=9999
BUFFER=2048
SENDER_NAME="DONI"


arr_mesg_lock=threading.Lock()

class All_userdata:
    def __init__(self):

      self.client_key=""
      self.client_public_key=""
      self.server_public_key=""
      self.loggin=False#true \ false
      self.mesg_for_send=[] #an array of all the mesg that need  to sent (the mesg is already ready to be send as is.)
      self.recv_mesg=[]#an array of all the mesg that recieved from the main server


def user_data_string(user_name,password):

  userdata=str(user_name)+str(password)
  return userdata

def user_usage(user_data):

    print
    #show the interface of the password
    #get_password

def main():


def main():

  user_data=All_userdata()

  key=secure.create_key()
  public_key=secure.Publik_Key(key)

  user_data.client_key=key
  user_data.client_public_key=public_key




  #GET FROM THE USER THE PASSWORD AND USERNAME
  while 1:

      password="password"
      sendMesg_client.send_to_server_password(password,sock,user_data.server_public_key,SENDER_NAME)

      #GET AN ANSWER IF THE PASSWORD IS AUTHORIZED
      check=sock.recv(BUFFER)

      while check is True:

          get_data_from_frame()

def client_to_other_clients(client_sock):
    #c-client-->c-server

    #def check for right mesg
    client_sock.send()


def client_server_recv(clientsock):
    #c-server-->c-client
    client_recv=clientsock.recv()
    #insert it to database

def client_server_other_clients(port):
    #c-server-->c-client

    #the main server send the port that need to be used


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


def handler_client_with_server(user_data):

    #c-client-->s-server
    #all the client as a client sender
    port=9999
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, port))

    sock.send(user_data.client_public_key)

    while 1:


        arr_mesg_lock.acquire()

        pull_next_mesg=user_data.mesg_for_send[0]
        user_data.mesg_for_send.remove(pull_next_mesg)
        sock.send(pull_next_mesg)
        arr_mesg_lock.release()

def handler_server_only_from_server(user_data,port):
    #c-server-->s-client
    #act as a server for reciving#need to get the port from the server
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
        thread.start_new_thread(client_server_recv, (clientsock))

   # pu_key=sock.recv(BUFFER)
    #user_data.server_public_key=secure.get_public_key_from_other_side(pu_key)

def control_the_client():
    #all the usage of the user
    #its create all the mesg built already
    print

if __name__=='__main__':
    main()
