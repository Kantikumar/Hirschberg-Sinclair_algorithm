#!/usr/bin/python3
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

	'''The Hirschberg–Sinclair algorithm'''
	while True:
		data = serverSock.recv(1024)
		message = data.split(":")
		if message[1] == "p" and int(message[2]) == ID :
			print "Leader: " + str(ID)
		elif message[1] == "p" and int(message[2]) > ID and int(message[4]) <= 2**int(message[3]) :
			sendMessage = str(Port) + ":p:" + message[2] + ":" + message[3] + ":" + str(int(message[4])+1)
			sendPort = xorPort ^ int(message[0])
			sendIP = LeftIP if sendPort == LeftPort else RightIP
			clientSock.sendto(sendMessage, (sendIP, sendPort))
		elif message[1] == "p" and int(message[2]) > ID and int(message[4]) > 2**int(message[3]) :
			sendMessage = str(Port) + ":r:" + message[2] + ":" + message[3]
			sendPort = int(message[0])
			sendIP = LeftIP if sendPort == LeftPort else RightIP
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


''' client() function starts the phase 0 processing by sending initial probe messages to both the neighbours'''
def client(ID, Port, LeftIP, LeftPort, RightIP, RightPort):
	message = str(Port) + ":p:" + str(ID) + ":" + str(0) + ":" + "1"
	clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	'''Sending message to Right Neighbour'''
	clientSock.sendto(message, (RightIP, RightPort))

	'''Sending message to Left Neighbour'''
	clientSock.sendto(message, (LeftIP, LeftPort))


def node_thread(ID, IP, Port, LeftIP, LeftPort, RightIP, RightPort):
	'''Calling SERVER thread which will keep listening for new messages and process on it'''
	t1 = threading.Thread(target=server, args=(ID, IP, Port, LeftIP, LeftPort, RightIP, RightPort))

	'''Calling CLIENT thread to start the pahse 0'''
	t2 = threading.Thread(target=client, args=(ID, Port, LeftIP, LeftPort, RightIP, RightPort))

	t1.start()
	'''Sleeping for 3 seconds so that all the other thread's Server can start'''
	time.sleep(3)

	t2.start()
	t2.join()
	t1.join()


def main():
	number = raw_input("Enter number of nodes:")
	number_nodes = int(number)
	Sec_suffix = 0
	First_suffix = 1
	InitIp = "127.0"
	InitPort = 5000
	lastIP_first_suffix = number_nodes % 254
	lastIP_sec_suffix = number_nodes / 254
	LastIP = InitIp + "." + str(lastIP_sec_suffix) + "." + str(lastIP_first_suffix)

	'''Generating random unique ID for processes'''
	UID = random.sample(range(1, 10000), number_nodes)
	for i in UID:
		print i
	print "Elected leader should be: " , max(UID)

	'''Assigning Left neighbour and Right neighbour to a node'''
	for i in range(number_nodes):
		if First_suffix%255 == 0 and First_suffix != 0:
			Sec_suffix = Sec_suffix+1
			First_suffix = 1
		IP = InitIp + "." + str(Sec_suffix) + "." + str(First_suffix)  

		Port = InitPort + i
		port_ind = i-1
		if i-1 < 0:
			port_ind = number_nodes - 1
		LeftPort = InitPort + port_ind
		if First_suffix == 1 :
			if Sec_suffix-1 >= 0 :
				LeftIP = InitIp + "." + str(Sec_suffix-1) + ".254"
			else:
				LeftIP = LastIP
		else:
			LeftIP = InitIp + "." + str(Sec_suffix) + "." + str(First_suffix-1)

		ip_ind1 = i
		port_ind1 = i-1
		if i+1 == number_nodes:
			port_ind1 = -2
		RightPort = InitPort + port_ind1+2

		if First_suffix == 254:
			if Sec_suffix < lastIP_sec_suffix:
				RightIP = InitIp +"." + str(Sec_suffix+1) + ".1"
			else:
				RightIP = "127.0.0.1"

		elif IP == LastIP:
			RightIP = "127.0.0.1"

		else:
			RightIP = InitIp + "." + str(Sec_suffix) + "." + str(First_suffix+1)

		First_suffix = First_suffix + 1
		#print IP + " " + str(Port) + " " + LeftIP + " " +  str(LeftPort) + " "  + RightIP + " "  + str(RightPort)

		'''Creating a node as a seperate thread and passing ID, IP, Port, Left neighbour and Right neighbour'''
		threading.Thread(target=node_thread, args=(UID[i], IP, Port, LeftIP, LeftPort, RightIP, RightPort)).start() 


if __name__== "__main__":
  main()