import socket
import time
s = socket.socket()
host = socket.gethostname()
port = 8090
s.connect((host, port))
while True:
    servermsg = s.recv(1024)
    print servermsg
    print "Please enter a valid url"
    url = raw_input("URL:")
    s.send(url)
    recieved_msg = s.recv(1024)
    print recieved_msg
    if recieved_msg == "The URL is not valid":
        print "Sleeping........."
        time.sleep(10)
    else:
        time.sleep(5)
s.close()
