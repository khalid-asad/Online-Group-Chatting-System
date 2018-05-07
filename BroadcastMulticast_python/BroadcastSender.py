#!/usr/bin/python           # This is client connecting to remote/local ip

import socket               # Import socket module
import sys                  # for exit
import time


#------------------------ socket descriptor ----------------------------
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # Create a socket object
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()

try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
except socket.error, msg:
    print 'Failed to set socket option for broadcast. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()

print 'Socket Created'

#------------------------ server IP ----------------------------
remote_ip = "255.255.255.255" # or "<broadcast>"
port = 12345                # Reserve a port for your service.

#------------------------ send data ----------------------------

while True:
    message = "This is a periodic broadcast message."
    try :
        #Set the whole string
        s.sendto(message, (remote_ip, port))
    except socket.error:
        #Send failed
        print 'Send failed'
        sys.exit()
    print 'Message send successfully'
    time.sleep(2)
# should never get here
raw_input('Press <ENTER> to close program')
s.close
