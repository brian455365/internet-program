import sys, socket, pickle, _thread, time
from getpass import getpass

MAX_BYTES = 65535	

def ReceiveFromServer(sock):
	while True:
		try:
			data = sock.recv(MAX_BYTES)
			message = pickle.loads(data)
			print(message)
			if message[0]=="3":
				break
		except socket.error as e:
			print("this is " + e)

		
def client():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	stringIP = socket.gethostbyname(socket.gethostname())
	sock.connect((stringIP,241))
	
	print("Client socket name", sock.getsockname())
	print("Please input your name.")
	username = input('Name：')
	print("Please input your password.")
	userpassword = getpass()
	check = pickle.dumps([username,userpassword])
	sock.sendall(check)
	
	
	data = sock.recv(MAX_BYTES)
	message = pickle.loads(data)
	print(message[1])
	
	while message[0]==2:
		print("Please input your name.")
		username = input('Name：')
		print("Please input your password.")
		userpassword = getpass()
		check = pickle.dumps([username,userpassword])
		sock.sendall(check)
		data = sock.recv(MAX_BYTES)
		message = pickle.loads(data)
		print(message[1]) 
	
	#Login = [username,userpassword]
	
	_thread.start_new_thread( ReceiveFromServer, (sock,) )
	
	while True:
		time.sleep(1)
		print("Please input a number:")
		print("(1) List all on-line users")
		print("(2) Send broadcast message to all on-line users")
		print("(3) Exit")
		print("(4) Chat with on-line users")
		print("(5) Send message to off-line users")
		mode = input()
		if mode=="1" :
			sock.sendall(pickle.dumps(["1"]))
			#data = sock.recv(MAX_BYTES)
			#message = pickle.loads(data)
			#print(message)
		elif mode=="3":
			sock.sendall(pickle.dumps(["3",username]))
			time.sleep(1)
			#data = sock.recv(MAX_BYTES)
			#message = pickle.loads(data)
			#print(message)
			sock.close()
			break;
		elif mode=="2":
			sentence = input("Please input your message.")
			sock.sendall(pickle.dumps(["2",username,sentence]))
		elif mode=="4":
			name = input("Please input the name you want to chat with:")
			sock.sendall(pickle.dumps(["4",username,name]))     # suppose the other exists
			while True:
				print("Please input your sentence or 'exit' to back to menu.")
				sentence = input()
				sock.sendall(pickle.dumps([username,sentence]))
				if sentence == "exit":
					break
		elif mode=="5":
			print("Please input the name you want to leave messages:")
			name = input()
			print("Please input messages:")
			sentence = input()
			sock.sendall(pickle.dumps(["5",username,name,sentence]))

			
			
			
if __name__ == '__main__':
	client()