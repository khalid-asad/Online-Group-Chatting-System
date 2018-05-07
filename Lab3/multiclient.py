#!/usr/bin/python

import socket
import struct
import thread
import time
import sys
import os

user = "Q2m01x35sa"
default_grp = '239.15.1.1'
default_port = 12345
#MCAST_GRP = '239.15.1.1'
#MCAST_PORT = 12345
def client(MCAST_GRP, MCAST_PORT):
    #MCAST_GRP = '239.15.1.1'
    #MCAST_PORT = 12345

    #create sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    #ask for name
    nick = raw_input("Please choose a nick name: \n")
    user = nick
    sending = True
    joined = nick + " has joined the chat.\n"
    #try sending
    sock.sendto(joined.encode(encoding='utf_8', errors='strict'), (MCAST_GRP, MCAST_PORT))
    while (sending):
        #sendmsg = raw_input('send what message? \n')
        sendmsg = raw_input('')
        if sendmsg == '/exit': #exit
            exiting = nick + " has now left the chat.\n"
            sock.sendto(exiting.encode(encoding='utf_8', errors='strict'), (MCAST_GRP, MCAST_PORT))
            print("leaving chat...\n")
            #thread.exit(server, ("Server", ))
            exit() #exit
            #quit()
            os._exit(1)
            #raise SystemExit
            break
        elif sendmsg.startswith('/nick ') == True: # change nickname
            #get the 2nd word and save that into a message
            nickchange = nick + " is now known as: " + sendmsg.split(sep=None, maxsplit=1)[1]
            #send the message to the Multicast group and port
            sock.sendto(nickchange.encode(encoding='utf_8', errors='strict'), (MCAST_GRP, MCAST_PORT))
            #save the nickname
            nick = sendmsg.split(sep=None, maxsplit=1)[1]
        elif sendmsg.startswith('/send') == True: #send file
            #filename = raw_input('Please enter a filename in the same directory.\n')
            try:
                file_name = sendmsg.split()[1]
                send_flag = 1
            except:
                print "Error: please enter a valid filename"
                send_flag = 0
            while(send_flag):
                print(file_name)
                f=open (file_name, "rb")  #open the file to be send
                l = f.read(10240)
                while (l):
                    sock.sendto(l.encode(encoding='utf_8', errors='strict'), (MCAST_GRP, MCAST_PORT))
                    #send file and read back message
                    l = f.read(10240)
                #close the socket after completion
                sock.close()
                exit()
        elif sendmsg.startswith('/help') == True: #display all types of commands
            print("This program will not give you a prompt message for input.\n")
            print("Simply enter the message you want to send and press enter.\n")
            print("/help for help.\n")
            print("/nick to change your nickname.\n")
            print("/send <filename> to send a file.\n")
            print("/exit to exit program.\n")
        elif sendmsg.startswith('/') == True: #for unrecognized commands
            print("Command not recognized.\n")
        else: #send the message
            parsedmsg = nick + ": " + sendmsg
            #send the message with encoding and strict errors to the multicast group and port
            sock.sendto(parsedmsg.encode(encoding='utf_8', errors='strict'), (MCAST_GRP, MCAST_PORT))
    print("You have left the chat.\n")

def server(MCAST_GRP, MCAST_PORT):
    #MCAST_GRP = '239.15.1.1'
    #MCAST_PORT = 12345

    #set up sockets using REUSEADDR so that we can emulate many machines
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    #add membership to socket
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    message = ""
    
    while True:
        #time.sleep()
        #recieve the message with encoding and strict errors
        message = sock.recv(10240).decode(encoding="utf-8", errors="strict")
        #if message.startswith(user) == False:
        if message.split()[1] == '/send': #check if the 2nd word is /send
            #sc, address = sock.accept()
            f = open(message.split()[2],'wb') #open in binary
            while (True):       
                l = sock.recv(10240)
                while (l):
                    #recieve and write
                    f.write(l)
                    l = sock.recv(10240)
            f.close() #close file
        else:
            print(message)

#main method to change group and port
group_flag = 1
while group_flag:
    start_input = raw_input('Please enter the IP address and port you would like to connect to separated by a space.\nPress enter for default of 239.15.1.1 and 12345\n')
    if start_input.startswith('239.15.'): #get group
        MCAST_GRP = int(start_input.split()[0])
        MCAST_PORT = int(start_input.split()[1])
        print("You entered a group of: " + str(MCAST_GRP) + " and port of: " + str(MCAST_PORT))
        group_flag = 0
    elif start_input == '': #if user presses enter, use default group
        MCAST_GRP = default_grp
        MCAST_PORT = default_port
        print("You entered a group of: " + str(MCAST_GRP) + " and port of: " + str(MCAST_PORT))
        group_flag = 0
    else: #user did not enter a valid IP Address and port
        print("Please enter a valid IP address and port")
#try to create 2 threads, one for server and client function each
try:
    thread.start_new_thread(server, (MCAST_GRP, MCAST_PORT))
    thread.start_new_thread(client, (MCAST_GRP, MCAST_PORT))
except:
   print "Error: unable to start thread"

while 1:
    pass
