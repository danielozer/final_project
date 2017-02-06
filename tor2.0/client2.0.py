__author__ ="daniel ozer"
import secure2.0
import sendMesg_client
import show_page
import socket


IP="127.0.0.1"
PORT=9999
BUFFER=2048

class all_userdata(self):
  self.client_key=""
  self.client_public_key=""
  self.server_public_key=""

def user_data_string(user_name,password):
  userdata=str(user_name)+str(password)
  return userdata


def main_client():
  user_data=all_user_data()
  
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((IP, PORT))
                        
  pu_key=sock.recv(BUFFER)
  
  user_data.server_public_key=get_public_key_from_server(pu_key)
  
  
  
