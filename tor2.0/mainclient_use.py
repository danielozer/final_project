"""
---------------------------------------------------------------
Author          :   Daniel Ozer
Date            :   XXXX
Version         :   1.0
Description     :   combing the back-end with the front-end
---------------------------------------------------------------
"""


#imports

import design,client
import thread,time

#imports


"""
run the thread for all the client usage (frontend,backend)
"""
thread.start_new_thread( design.main ,(1,1))


thread.start_new_thread(client.main,(1,1))

while 1:
    pass