#############
# python tcpserver.py
# usage: python tcpserver.py <Port number>
#############

###############
# Computer Network programming 
# HW2: TCP FTP tcpserver.py
# Name: Tanner Patrom
#Student ID: 50406980
# How to compile: python2.7 tcpserver.py <Port number>
###############

import socket
import sys
import os
import time

BUFFER_SIZE = 512

# Used to remove *1: or *2:
def pretty(message):
    messageList = list(message)
    for i in range(3):
        messageList.pop(0)
    new_message = ''.join(messageList)
    return new_message

if (len(sys.argv) < 2):
    print('usage: python udpserver.py <Port number>')
    sys.exit()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', int(sys.argv[1]))
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(BUFFER_SIZE)
            if not data: break
            print >>sys.stderr, 'received "%s"' % data
            dataFile = pretty(data)

            # Call appropriate method when requested from client
            if '*1' in data:
                print 'Client ' + str(client_address[0]) + ' requesting the file name [' + dataFile + ']'
                if os.path.exists(dataFile):
                    data += ':yes'
                    print 'Server has it and sending ' + data + ' to the client'
                else:
                    data +=':no'
                    print 'Server does not have ' + dataFile + ' and sending ' + data + ' to the client'
                print '_____________________'
                connection.send(data)
            elif '*2' in data:
                if os.path.exists(dataFile):
                    print "Sending request file " + dataFile + ' to ' + str(client_address[0])
                    with open(dataFile,"r") as fileToTransfer:
                        for line in fileToTransfer:
                            connection.send(line)
                    print 'Completed, sending EOF'
                    print '_____________________'
                    time.sleep(0.2) # Only used to force a new tcp segment in order to correctly read eof by client, want to make better
                    connection.send('**EOF**')
                else:
                    print "Error file requested does not exist in this directory"
                    print '_____________________'
                    connection.send('Error file does not exist on server')
                            




    finally:
        # Clean up the connection
        print 'Closing Connection to ' + str(client_address[0])
        connection.close()
