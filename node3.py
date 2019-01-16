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

def client(Port, RightPort, LeftPort):
	clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	clientSock.sendto("hi from " + str(Port), ("127.0.0.42", RightPort))
	clientSock.sendto("hi from " + str(Port), ("127.0.0.5", LeftPort))



def main():
	# creating thread 
    t1 = threading.Thread(target=server, args=("127.0.0.6", 5060)) 
    t2 = threading.Thread(target=client, args=(5060, 5000, 5050)) 
    # starting thread 1 
    t1.start() 
    # starting thread 2
    time.sleep(5)
    t2.start()
    t1.join()
    t2.join()



  

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