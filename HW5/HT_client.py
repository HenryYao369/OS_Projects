from socket import *
import sys
#Host and Port refer to the server's 
#hostname and port number
Host = sys.argv[1]
Port = 44100
addr = (Host, Port)
bufsize = 1024

csocket = socket(AF_INET,SOCK_STREAM)
csocket.connect(addr)

while True:
	data = raw_input('>')
	csocket.send(data)
	data = csocket.recv(bufsize)
	if not data:
		break
	print data
csocket.close()