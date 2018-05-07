#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import sys


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print 'Socket created'

host = "" # this special form represents INADDR_ANY
# INADDR_ANY
# usually the right thing to do for servers because it saves us from having to find out the host's actual Internet address (a host may have multiple Internet interfaces)
# connections to the specified port will be directed to the corresponding binded socket, regardless of which Internet address they are sent to
port = 12345                # Reserve a port for your service.
try:
    s.bind((host, port))        # Bind to the port
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

while True:
   data, addr = s.recvfrom(1024)
   if data:
       print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data

s.close
