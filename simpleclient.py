# import sys
import socket
s = socket.socket()
host = socket.gethostname()
port = 8090
s.connect((host, port))
print s.recv(1024)
print "Please enter a valid url"
url = raw_input("URL:")
print url
s.send(url)
s.close()
