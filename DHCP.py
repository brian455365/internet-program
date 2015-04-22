import argparse, socket, struct, sys

MAX_BYTES = 65535

#server : python DHCP.py 1
#client : python DHCP.py 2

class DHCP_discover:
	def __init__(self):    
		self.stringIP = socket.gethostbyname(socket.gethostname())
		self.binaryIP = socket.inet_aton(self.stringIP)
		
	def buildPacket(self):
		packet = b''
		packet += b'\x01'   
		packet += b'\x01'   
		packet += b'\x06'   
		packet += b'\x00'   
		packet += b'\x00\x00\x02\xcb'    #Transaction ID : 715
		packet += b'\x00\x00'    
		packet += b'\x80\x00'    		 #Bootp flags 
		packet += self.binaryIP			 #ciaddr (Client IP Address)
		packet += b'\x00\x00\x00\x00'    #yiaddr 				 
		packet += b'\x00\x00\x00\x00'	 #siaddr (Server IP Address)				
		packet += b'\x00\x00\x00\x00'    #giaddr (Relay IP Address)						
		packet += b'\x00\x05\x3C\x04'					
		packet += b'\x8D\x59\x00\x00'
		packet += b'\x00\x00\x00\x00'	
		packet += b'\x00\x00\x00\x00'	  
		packet += b'\x00' * 64   		 #Server host name not given
		packet += b'\x00' * 128 		 #Boot file name not given
		packet += b'\x63\x82\x53\x63'	 #Magic cookie

		packet += b'\x35\x01\x01'   #Option: (t=53,l=1) DHCP Message Type = DHCP Discover
		packet += b'\xff'  		    #End Option
		return packet

class DHCP_offer:
	def __init__(self):    
		self.stringIP = socket.gethostbyname(socket.gethostname())
		self.binaryIP = socket.inet_aton(self.stringIP)
		
	def buildPacket(self):
		packet = b''
		packet += b'\x02'  
		packet += b'\x01'   
		packet += b'\x06'   
		packet += b'\x00'   
		packet += b'\x00\x00\x02\xcb'    
		packet += b'\x00\x00'    
		packet += b'\x00\x00'    
		packet += self.binaryIP			 #ciaddr
		packet += b'\xC0\xA8\x01\x64'    #yiaddr  192.168.1.100				
		packet += self.binaryIP			 #siaddr
		packet += b'\x00\x00\x00\x00'    #giaddr		
		packet += b'\x00\x05\x3C\x04'					
		packet += b'\x8D\x59\x00\x00'
		packet += b'\x00\x00\x00\x00'	
		packet += b'\x00\x00\x00\x00'
		packet += b'\x00' * 64   		 
		packet += b'\x00' * 128 		 
		packet += b'\x63\x82\x53\x63'
		packet += b'\x35\x01\x02'   #Option: (t=53,l=1) DHCP Message Type = DHCP Offer
		packet += b'\xff'   		#End Option
		return packet
		
class DHCP_request:
	def __init__(self):    
		self.stringIP = socket.gethostbyname(socket.gethostname())
		self.binaryIP = socket.inet_aton(self.stringIP)
		
	def buildPacket(self):
		packet = b''
		packet += b'\x01'  
		packet += b'\x01'   
		packet += b'\x06'   
		packet += b'\x00'   
		packet += b'\x00\x00\x02\xcc'    
		packet += b'\x00\x00'    
		packet += b'\x80\x00'    
		packet += self.binaryIP			 #ciaddr
		packet += b'\x00\x00\x00\x00'	 #yiaddr  
		packet += self.binaryIP			 #siaddr
		packet += b'\x00\x00\x00\x00'    #giaddr			
		packet += b'\x00\x05\x3C\x04'					
		packet += b'\x8D\x59\x00\x00'
		packet += b'\x00\x00\x00\x00'	
		packet += b'\x00\x00\x00\x00'
		packet += b'\x00' * 64   		 
		packet += b'\x00' * 128 		 
		packet += b'\x63\x82\x53\x63'
		packet += b'\x35\x01\x03'   #Option: (t=53,l=1) DHCP Message Type = DHCP Request
		packet += b'\xff'   		#End Option
		return packet

class DHCP_acknowledgement:
	def __init__(self):    
		self.stringIP = socket.gethostbyname(socket.gethostname())
		self.binaryIP = socket.inet_aton(self.stringIP)
		
	def buildPacket(self):
		packet = b''
		packet += b'\x02'  
		packet += b'\x01'   
		packet += b'\x06'   
		packet += b'\x00'   
		packet += b'\x00\x00\x02\xcc'    
		packet += b'\x00\x00'    
		packet += b'\x00\x00'    
		packet += self.binaryIP			 #ciaddr
		packet += b'\xC0\xA8\x01\x64'	 #yiaddr   192.168.1.100
		packet += self.binaryIP			 #siaddr
		packet += b'\x00\x00\x00\x00'  	 #giaddr	 				
		packet += b'\x00\x05\x3C\x04'					
		packet += b'\x8D\x59\x00\x00'
		packet += b'\x00\x00\x00\x00'	
		packet += b'\x00\x00\x00\x00'
		packet += b'\x00' * 64   		 
		packet += b'\x00' * 128 		 
		packet += b'\x63\x82\x53\x63'
		packet += b'\x35\x01\x05'   #Option: (t=53,l=1) DHCP Message Type = DHCP Ack
		packet += b'\xff'  		    #End Option
		return packet

def PrintMessage(data):
	print("XID : {}".format(struct.unpack('!L', data[4:8])[0]))
	print("CIADDR  : {}.{}.{}.{}".format(data[12],data[13],data[14],data[15]))
	print("YIADDR  : {}.{}.{}.{}".format(data[16],data[17],data[18],data[19]))
	print("SIADDR  : {}.{}.{}.{}".format(data[20],data[21],data[22],data[23]))
	print("GIADDR  : {}.{}.{}.{}".format(data[24],data[25],data[26],data[27]))
	print("GIADDR  : {}.{}.{}.{}".format(data[24],data[25],data[26],data[27]))
	print("Options : {}".format(data[240]))
	print("Options : {}".format(data[241]))
	print("Options : {}".format(data[242]))		
		
ServerType=1			
def server():
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	stringIP = socket.gethostbyname(socket.gethostname())
	sock.bind((stringIP,67))
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	print('Server socket is {}'.format(sock.getsockname()))
	global ServerType
	while True:
		data, address = sock.recvfrom(MAX_BYTES)
		print('The client at {} says :'.format(address))
		PrintMessage(data)
		if ServerType==1:
			offerPacket = DHCP_offer()
			sock.sendto(offerPacket.buildPacket(),('255.255.255.255', 68))
			ServerType = 2
		elif ServerType==2:
			ackPacket = DHCP_acknowledgement()
			sock.sendto(ackPacket.buildPacket(),('255.255.255.255', 68))
			ServerType = 1
			sock.close()
			break

	
def client():
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	stringIP = socket.gethostbyname(socket.gethostname())
	sock.bind((stringIP,68))
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	print('Client socket is {}'.format(sock.getsockname()))
	discoverPacket = DHCP_discover()
	sock.sendto(discoverPacket.buildPacket(),('255.255.255.255', 67))
	sock.settimeout(3)
	try:
		data, address = sock.recvfrom(MAX_BYTES)
		print('The server at {} says :'.format(address))
		PrintMessage(data)
		requestPacket = DHCP_request()
		sock.sendto(requestPacket.buildPacket(),('255.255.255.255', 67))
		sock.settimeout(3)
		try:
			data, address = sock.recvfrom(MAX_BYTES)
			print('The server at {} says :'.format(address))
			PrintMessage(data)
		except socket.timeout as e:
			print(e)
	except socket.timeout as e:
		print(e)
	
	sock.close()	
	
if __name__ == '__main__':
	if sys.argv[1] == '1':
		server()
	elif sys.argv[1] == '2':
		client();
