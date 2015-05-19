import sys, socket, pickle, time
import _thread

MAX_BYTES = 65535

namepassword = [["apple","123"],["banana","1234"],["cat","12345"]]

def CreateListenSocket():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	stringIP = socket.gethostbyname(socket.gethostname())
	sock.bind((stringIP,241))
	sock.listen(10)
	print("Listening socket: ", sock.getsockname())
	return sock

alivename=[]	
offlineMessage=[]
def HandleData(sock,alivesocket):
	global alivename
	global namepassword
	global offlineMessage
	data = sock.recv(MAX_BYTES)
	message = pickle.loads(data)
	count=0
	for i in namepassword:
		if message[0]==i[0] and message[1]==i[1]:
			sock.sendall(pickle.dumps([1,'Login success']))
			alivename.append(i[0])
			alivesocket.append(sock)
			break
		count = count + 1
	while count==len(namepassword):
		sock.sendall(pickle.dumps([2,'Login fail']))
		data = sock.recv(MAX_BYTES)
		message = pickle.loads(data)
		count=0
		for i in namepassword:
			count = count + 1
			if message[0]==i[0] and message[1]==i[1]:
				sock.sendall(pickle.dumps([1,'Login success']))
				alivename.append(i[0])
				alivesocket.append(sock)
				break
	
	while True:
		if len(offlineMessage) != 0 :
			print(offlineMessage)
			count = 0
			for i in alivename:
				#for j in range(1, len(offlineMessage), 3):
				j = 1
				while j < len(offlineMessage):
					if offlineMessage[j] == i:
						alivesocket[count].sendall(pickle.dumps([offlineMessage[j-1],offlineMessage[j+1]]))
						print([offlineMessage[j-1],offlineMessage[j],offlineMessage[j+1]])
						offlineMessage.pop(j-1)
						offlineMessage.pop(j-1)
						offlineMessage.pop(j-1)
						print("Hey")
						print(offlineMessage)
					else:
						j = j + 3
				count = count + 1
			
		data = sock.recv(MAX_BYTES)
		message = pickle.loads(data)
		if message[0] == "1": 
			sock.sendall(pickle.dumps(alivename))
		elif message[0] == "3":
			count = 0
			for i in alivename:
				if message[1] == i:
					alivename.pop(count)
					break
				count = count + 1
			sock.sendall(pickle.dumps(["3","server socket close"]))
			count = 0
			for i in alivesocket:
				if i == sock:
					alivesocket.pop(count)
					break
				count = count + 1
			time.sleep(0.5)
			sock.close()
			break
		elif message[0] == "2":
			for i in alivesocket:
				i.sendall(pickle.dumps(message))
		
		elif message[0] == "4":
			count = 0
			for i in alivename:
				if message[2] == i:
					#print(alivesocket[count])
					alivesocket[count].sendall(pickle.dumps(message))
					break
				count = count + 1
			while True:
				data = sock.recv(MAX_BYTES)
				message = pickle.loads(data)
				if message[1] == "exit":
					break
				alivesocket[count].sendall(pickle.dumps(message))
		
		elif message[0] == "5":
			offlineMessage.append(message[1])   #  sender
			offlineMessage.append(message[2])   #  receiver
			offlineMessage.append(message[3])   #  off-line message
					
			
			

alivesocket=[]	
def server():
	listener = CreateListenSocket()
	global alivesocket
	while True:
		sc, sockname = listener.accept()
		#print("We have accepted a connection from", sockname)
		print("New socket name:  ",sc.getsockname())
		print("Client socket name:  ",sc.getpeername())
		
		_thread.start_new_thread( HandleData, (sc,alivesocket,) )
		
		
				
				
		#data = sc.recv(MAX_BYTES)
		#message = pickle.loads(data)
		#if message=="exit":
		#	print("Client close connection")
		#	sc.close()
		#message, address = sock.recvfrom(MAX_BYTES)
		#print(" Incoming sixteen-octet message:", repr(message))
		#print('The client says:  {}'.format(message))
		#sc.sendall(b'Farewell client')
		#sc.close()
		#print(" Reply sent, socket closed")
		
if __name__ == '__main__':
	server()