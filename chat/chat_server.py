#!/usr/bin/env python

import re  
from time import ctime
import select
import socket

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

USER = {}

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.bind(ADDR)
tcpServer.listen(5)

inputs = [tcpServer]

while True:
	print "Start"
	rs, ws, es = select.select( inputs, [], [] )
	for r in rs:
		if r == tcpServer :
			tcpSock, addr = r.accept()
			print tcpSock, addr
			inputs.append(tcpSock)
			USER[tcpSock] = [tcpSock, ""]
		else:
			try:
				data = r.recv(1024)
				matchname = re.match(r'(.+)\sjoin the server',data)  

				if matchname:
					print data
					for x in inputs:
						if x == tcpServer or x == r:
							pass
						else:
							if USER[x][1] == "":
								pass
							else:
								x.send(data)

					username = matchname.group(1)
					USER[r][1] = username
					r.send("Welcome, %s" % username)

				else:
					senddata = "%s said: %s" % (USER[r][1], data)
					for x in inputs:
						if x == tcpServer or x == r:
							pass
						else:
							x.send(senddata)

				disconnected = False

			except socket.error:
				disconnected = True

			if disconnected :
				leftdata = "%s leave! " % USER[r][1]
				print leftdata
				for x in inputs:
					if x == tcpServer or x == r:
						pass
					else:
						x.send(leftdata)

				r.close()
				inputs.remove(r)


tcpServer.close()
