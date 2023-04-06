###############
# python tcpclient.py 
# usage: python tcpclient.py <IP address> <Port number>
# Will only work with Python2.7
###############

###############
# Computer Network programming 
# HW2: TCP FTP tcpclient.py
# Name: Tanner Patrom
#Student ID: 50406980
# How to compile: python2.7 tcpclient.py <IP address> <Port number>
###############

import socket
import sys
import os

BUFFER_SIZE = 512

menu = """
===Please select from the menu===
1. Check a file (Usage: *1:filename)
2. Download a file (Usage: *2:filename)
0. Exit (Usage: 0)
"""    
# Used to remove *1: or *2:
def pretty(message):
    messageList = list(message)
    for i in range(3):
        messageList.pop(0)
    filename = ''.join(messageList)
    return filename

# Very ugly way of updating filename copies
def fileRename(fileToChange):
    ext = os.path.splitext(fileToChange)
    if ext[0].endswith(')'):
        s = ext[0]
        result = s[s.find('(') + 1: s.find(')')] 
        result = int(result)
        fileToChange = ext[0] + '(' + str(result) + ')' + ext[1]
    else:
        i = 1
        while os.path.exists(fileToChange):
            fileToChange = ext[0] + '(' + str(i) + ')' + ext[1]
            i += 1
    return fileToChange
    

if (len(sys.argv) < 3): 
    print('usage: python udpclient.py <IP address> <Port number>')
    sys.exit()
# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (sys.argv[1], int(sys.argv[2]))
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address) 



try:
    while True:
        print menu 
        userinput = raw_input("Please enter: ")
        message = userinput

        # Send data and receive with appropriate user input
        if '*1' in message:
            filename = pretty(message)
            print 'Requesting file name ' + filename
            sent = sock.send(message)
            data = sock.recv(BUFFER_SIZE)
            print >>sys.stderr, 'Received: %s' % data
            if 'yes' in data:
                print 'Server contains the file ' + filename
            else:
                print 'Server does not contain the file ' + filename
            print '_____________________'
        elif '*2' in message:
            filename = pretty(message)
            print 'Requesting the transfer of ' + filename
            if os.path.exists(filename):
                new_file = fileRename(filename)
            else:
                new_file = filename
            sent = sock.send(message)
            data = sock.recv(BUFFER_SIZE)
            if 'Error' in data:
                print 'File does not exist on server, please try again'
                print '_____________________'
            else:    
                with open(new_file,"w") as fileToWrite:
                    fileToWrite.write(data)
                    while True:
                        data = sock.recv(BUFFER_SIZE)
                        #print >>sys.stderr, 'Received: %s' % data
                        if data == '**EOF**':
                            print 'Received entire file, file saved at ' + new_file
                            print '_____________________'
                            break
                        fileToWrite.write(data)
        else:
            break


finally:
    print >>sys.stderr, 'Closing socket'
    sock.close()


