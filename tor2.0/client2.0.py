__author__ ="daniel ozer"
import secure
#import sendMesg_client
#import show_page
import socket


IP="127.0.0.1"
PORT=9999
BUFFER=2048

class All_userdata:
    def __init__(self):
      self.client_key=""
      self.client_public_key=""
      self.server_public_key=""


def user_data_string(user_name,password):
  userdata=str(user_name)+str(password)
  return userdata


def main():
  user_data=All_userdata()
  
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((IP, PORT))
  #recv the public key of the server as a pickle
  pu_key=sock.recv(BUFFER)

  user_data.server_public_key=pu_key
  print user_data.server_public_key
  
  
if __name__=='__main__':
    main()
