# Hirschberg-Sinclair_algorithm

Command to Run: python node.py (Python 2.7)

System Architecture:
The system architecture is based on the master-worker paradigm. The code starts with asking a number of nodes from the user. Main functions act as master threads and generate a number of worker threads (equal to the number of nodes entered). Each worker thread behaves as a node in the existing system. We automatically generated IP, Port number, ID for each node. Each node spawns 2 more threads, one behaves as a client and the other behaves as a server.
Information regarding left and right neighbour is passed to both client and server thread. Client thread is used to initialise the first round, after that, all rounds are handled by server thread.
Server thread receives data from both left and right neighbour and decides based on the received ID.
At last one of them is elected as a leader (with maximum ID).
