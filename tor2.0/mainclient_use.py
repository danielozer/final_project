import design,client
import thread





thread.start_new_thread( design.main ,(1,1))


thread.start_new_thread(client.main,(1,1))
while 1:
    pass