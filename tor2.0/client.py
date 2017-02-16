__author__ ="daniel ozer"
import secure
import sendMesg_client
#import show_page
import socket
import cPickle as pickle
import thread


IP="127.0.0.1"
PORT=9999
BUFFER=2048
SENDER_NAME="DONI"


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


def client_server_recv(clientsock):


def client_server_other_clients(port):
    #the main server send the port that need to be used


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






def handler_client_with_server(user_data):
    #all the client as a client sender
    port=9999
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, port))

    sock.send(user_data.client_public_key)

    while 1:

        ## should be locks
        pull_next_mesg=user_data.mesg_for_send[0]
        user_data.mesg_for_send.remove(pull_next_mesg)
        ##end of the lock




def handler_server_only_from_server(user_data):
    #act as a server for reciving
    port = 8888
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, port))


    pu_key=sock.recv(BUFFER)
    user_data.server_public_key=secure.get_public_key_from_other_side(pu_key)





def control_the_client():
    #all the usage of the user
    #its create all the mesg built already




if __name__=='__main__':
    main()
