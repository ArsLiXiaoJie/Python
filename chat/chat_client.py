#!/usr/bin/env python

from socket import *
import threading

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)


tcpClient = socket(AF_INET, SOCK_STREAM)
tcpClient.connect(ADDR)

name = raw_input('> Enter Your Name:')
tcpClient.send( "%s join the server" % name )
back = tcpClient.recv(BUFSIZ)
print back




def recv_func():
	while True:	
		back = tcpClient.recv(BUFSIZ)
		if not back:
			return
		print back

def send_func():
	while True:
		data = raw_input('> ')
		if not data:
			return
		tcpClient.send( data )


f1 = threading.Thread( target = recv_func )
f2 = threading.Thread( target = send_func )

f1.start()
f2.start()

f1.join()
f2.join()

tcpClient.close()
	