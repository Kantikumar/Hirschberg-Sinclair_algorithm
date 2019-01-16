#!/usr/bin/python3           # This is client.py file
import socket
import threading 
import time

def server(IP, Port):
	serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serverSock.bind((IP, Port))
	while True:
		data, addr = serverSock.recvfrom(1024)
		print "Message: ", data



def client(Port, LeftIP, LeftPort, RightIP, RightPort):
	clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	clientSock.sendto("hi from " + str(Port), (RightIP, RightPort))
	clientSock.sendto("hi from " + str(Port), (LeftIP, LeftPort))




def node_thread(IP, Port, LeftIP, LeftPort, RightIP, RightPort):
	t1 = threading.Thread(target=server, args=(IP, Port)) #right left
	t2 = threading.Thread(target=client, args=(Port, LeftIP, LeftPort, RightIP, RightPort)) #right left



def main():
	number = raw_input("Enter number of nodes:")
	number_nodes = int(number)
	InitIp = "127.0.0."
	InitPort = 5000

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

		if i+1 == number_nodes:
			ip_ind = -1
			port_ind = -2
		RightIP = InitIp + str(ip_ind+2)
		RightPort = InitPort + port_ind+2
		print IP + " " + str(Port) + " " + LeftIP + " " +  str(LeftPort) + " "  + RightIP + " "  + str(RightPort)
		#threading.Thread(target=node_thread, args=(IP, Port, LeftIP, LeftPort, RightIP, RightPort)).start() 




  

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
