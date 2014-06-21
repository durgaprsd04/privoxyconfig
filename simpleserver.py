import sys
import socket
from rfc3987 import parse
# import signal
s = socket.socket()
host = ''
port = 8090
s.bind((host, port))
s.listen(5)
c, addr = s.accept()
print "Got connection from ", addr
c.send("Server up and running")
OriginalExceptHook = sys.excepthook


def NewExceptHook(type, value, traceback):
    if type == KeyboardInterrupt:
        print "Closing Socket"
        exit("Ctrl+C Interrupt recieved. Exiting...")
    else:
        OriginalExceptHook(type, value, traceback)
sys.excepthook = NewExceptHook
while True:
    valid = True
    url_recieved = c.recv(1024)
    try:
        parse(url_recieved, rule="IRI")
    except Exception as e:
        valid = False
    if valid:
        print "Do you want to write URL:", url_recieved, "to config file"
        response = raw_input("(yes/no):")
        if response == 'yes':
            fp = open("user.action", 'a')
            fp.write(url_recieved)
            fp.write("\n")
            print "URL written to the file user.action"
            print "Done"
            c.send("The URL is accepted")
            fp.close()
        else:
            print "URL not added"
            print "Message sent to client"
            c.send("The URL is blocked by admin")
    else:
        c.send("The URL is not valid")
        pass
c.close()
