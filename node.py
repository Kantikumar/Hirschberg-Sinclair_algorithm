#!/usr/bin/python3           # This is client.py file
import socket
import threading 
import time, random

def server(ID, IP, Port, LeftIP, LeftPort, RightIP, RightPort):
	serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serverSock.bind((IP, Port))
	clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	xorPort = LeftPort ^ RightPort
	replyCount = 0
	sendMessage = ""
	sendPort = 0
	while True:
		data = serverSock.recv(1024)
		message = data.split(":")
		if message[1] == "p" and int(message[2]) == ID :
			print "Leader: " + str(ID)
		elif message[1] == "p" and int(message[2]) > ID and int(message[4]) <= 2**int(message[3]) :
			sendMessage = str(Port) + ":p:" + message[2] + ":" + message[3] + ":" + str(int(message[4])+1)
			sendPort = xorPort ^ int(message[0])
			if sendPort == LeftPort :
				sendIP = LeftIP
			else :
				sendIP = RightIP
			clientSock.sendto(sendMessage, (sendIP, sendPort))
		elif message[1] == "p" and int(message[2]) > ID and int(message[4]) > 2**int(message[3]) :
			sendMessage = str(Port) + ":r:" + message[2] + ":" + message[3]
			sendPort = int(message[0])
			if sendPort == LeftPort :
				sendIP = LeftIP
			else :
				sendIP = RightIP
			clientSock.sendto(sendMessage, (sendIP, sendPort))
		elif message[1] == "r" and int(message[2]) != ID :
			sendMessage = str(Port) + ":r:" + message[2] + ":" + message[3]
			sendPort = xorPort ^ int(message[0])
			if sendPort == LeftPort :
				sendIP = LeftIP
			else :
				sendIP = RightIP
			clientSock.sendto(sendMessage, (sendIP, sendPort))
		elif message[1] == "r" and int(message[2]) == ID and replyCount==0 :
			replyCount = replyCount+1
		elif message[1] == "r" and int(message[2]) == ID and replyCount==1 :
			replyCount = 0
			sendMessage = str(Port) + ":p:" + str(ID) + ":" + str(int(message[3])+1) + ":" + "1"
			clientSock.sendto(sendMessage, (RightIP, RightPort))
			clientSock.sendto(sendMessage, (LeftIP, LeftPort))



def client(ID, Port, LeftIP, LeftPort, RightIP, RightPort):
	message = str(Port) + ":p:" + str(ID) + ":" + str(0) + ":" + "1"
	clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	clientSock.sendto(message, (RightIP, RightPort))
	clientSock.sendto(message, (LeftIP, LeftPort))
	# clientSock.sendto("hi from " + str(Port), (RightIP, RightPort))
	# clientSock.sendto("hi from " + str(Port), (LeftIP, LeftPort))




def node_thread(ID, IP, Port, LeftIP, LeftPort, RightIP, RightPort):
	t1 = threading.Thread(target=server, args=(ID, IP, Port, LeftIP, LeftPort, RightIP, RightPort))
	t2 = threading.Thread(target=client, args=(ID, Port, LeftIP, LeftPort, RightIP, RightPort))
	t1.start() 
	# starting thread 2
	time.sleep(3) 
	t2.start()
	t1.join()
	t2.join()



def main():
	number = raw_input("Enter number of nodes:")
	number_nodes = int(number)
	InitIp = "127.0.0."
	InitPort = 5000
	UID = random.sample(range(1, 1000), number_nodes)
	for i in UID:
		print i
	print "Elected leader should be: " , max(UID)
	for i in range(number_nodes):
		IP = InitIp + str(i+1)
		Port = InitPort + i
		ip_ind = i
		port_ind = i-1
		if i-1 < 0:
			ip_ind = number_nodes
			port_ind = number_nodes - 1
		LeftIP = InitIp + str(ip_ind)
		LeftPort = InitPort + port_ind

		ip_ind1 = i
		port_ind1 = i-1
		if i+1 == number_nodes:
			ip_ind1 = -1
			port_ind1 = -2
		RightIP = InitIp + str(ip_ind1+2)
		RightPort = InitPort + port_ind1+2
		print IP + " " + str(Port) + " " + LeftIP + " " +  str(LeftPort) + " "  + RightIP + " "  + str(RightPort)
		threading.Thread(target=node_thread, args=(UID[i], IP, Port, LeftIP, LeftPort, RightIP, RightPort)).start() 




  

'''Class Node: 
	def __init__(self, NodeId, NodeHost, NodePort, clockwiseNeighbor, antiClockwiseNeighbor): 
		self.NodeId=NodeId 
		self.IP=NodeHost 
		self.port=NodePort 
		self.clockwiseNeighbor=clockwiseNeighbor 
		self.antiClockwiseNeighbor=antiClockwiseNeighbor 
  

	def joinRing(self, rightnode): #raise RingException 
		# create a socket object
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# bind to the port
		serversocket.bind((self.IP, self.port))                                  
		# queue up to 5 requests
		serversocket.listen(5)                                           

		while True:
   			# establish a connection
   			clientsocket,addr = serversocket.accept()

   		#create client socket
   		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


	def sendMessageClockwise(self, message): #raise RingException  

	def sendMessageCounterClockwise(self, message) #raise RingException '''


if __name__== "__main__":
  main()