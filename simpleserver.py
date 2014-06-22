from rfc3987 import parse
from thread import *
import socket
import sys
OriginalExceptHook = sys.excepthook


def NewExceptHook(type, value, traceback):
    if type == KeyboardInterrupt:
        print "Closing Socket"
        exit("Ctrl+C Interrupt recieved. Exiting...")
    else:
        OriginalExceptHook(type, value, traceback)
sys.excepthook = NewExceptHook


def clientfunc(connection, addr):
    print "Got connection from ", addr
    connection.send("Server up and running")
    while True:
        connection.send("Ready for another url")
        valid = True
        url_recieved = c.recv(1024)
        try:
            parse(url_recieved, rule="IRI")
        except Exception as e:
            valid = False
        if valid:
            url_recieved = url_recieved.split('/')[2]
            print "Do you want to write URL:", url_recieved, "to config file"
            print "for the node", addr
            response = raw_input("(yes/no):")
            if response == 'yes':
                fp = open("user.action", 'a')
                fp.write(url_recieved)
                fp.write("\n")
                print "URL written to the file user.action"
                print "Done"
                connection.send("The URL is accepted")
                fp.close()
            else:
                print "URL not added"
                print "Message sent to client"
                connection.send("The URL is blocked by admin")
        else:
            connection.send("The URL is not valid")
            pass
    connection.close()


s = socket.socket()
host = ''
port = 8090
s.bind((host, port))
s.listen(5)
while True:
    c, addr = s.accept()
    start_new_thread(clientfunc, (c, addr))
s.close()
