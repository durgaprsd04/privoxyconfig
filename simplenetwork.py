# import os
import socket
# import signal
s = socket.socket()
host = ''
port = 8090
s.bind((host, port))
s.listen(5)
while True:
    c, addr = s.accept()
    print "Got connection from ", addr
    c.send("Server up and running")
    c.send("Please enter a valid url")
    url_recieved =c.recv(1024)
    print "Writing the URL:", url_recieved, "to config file"
    fp = open("user.action", 'a')
    fp.write(url_recieved)
    fp.close()
    c.close()
