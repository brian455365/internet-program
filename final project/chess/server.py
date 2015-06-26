from socket import *
from threading import *
from _thread import *
from time import sleep
from random import randint 
from queue import *
import struct
import uuid
import sys
import ServerInterface

from converter import *

class server :
	def __init__(self, ip = '127.0.0.1', port = 7000, maxQueue = 1000) :
		self.ip = ip # do automatic detect
		self.port = port
		self.user = dict()
		# check, and send messages pool
		self.Q = Queue(maxQueue)
		self.cond = Condition()
		self.mainSocket = socket(AF_INET, SOCK_STREAM)
		self.mainSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		
	def monitor(self, maxConnection = 1000) :
		self.mainSocket.bind((self.ip, self.port))
		self.mainSocket.listen(maxConnection)
		while True :
			newSocket, connAddr = self.mainSocket.accept()
			Thread(target = self.active, args = (newSocket,)).start()
	
	def check(self) :
		while True :
			if not self.Q.empty() :
				data = self.Q.get()
				try :
					self.user[data[0]][1].sendall(str2b(data[1]))
				except OSError :
					pass
				except KeyError :
					pass
	
	def join(self) :
		while True :
			for t in enumerate() :
				if not t.is_alive() :
					try :
						threadName = t.getName()
						t.join(10)
						print('cancel {} thread', threadName)
					except RuntimeError :
						pass
					break
	
	def run(self) :
		mThread = Thread(target = self.monitor)
		cThread = Thread(target = self.check)
		jThread = Thread(target = self.join)
		
		mThread.start()
		cThread.start()
		jThread.start()
		
		print("Server Start OK")
		
		mThread.join()
		cThread.join()
		jThread.join()
			
	def active(self, sock) :
		username = ""
		# match game user name
		peername = ""
		# my turn 
		isMyTurn = False
		
		# 登錄 nickname
		while True :
			try :	
				msg = "type=nickname&name=?"
				sock.sendall(str2b(msg))
				data = sock.recv(4096)
				
				userInfo = b2D(data)
					
				if userInfo["type"] == "nickname" :
					print(userInfo)
					if not userInfo["name"] in list(self.user.keys()) :
						username = userInfo["name"]
						# add new user to server
						self.user[username] = [username, sock, False] # username socket isMatch 
						# send login in game
						self.Q.put((username, "type=loginOK"))
						print(username, " login success !")
						break
						
			except ConnectionResetError :
				sock.close()
				exit()
				
		while True :
			try :
				data = sock.recv(4096)
				if len(data) > 0 :
					D = b2D(data)
					
					if D["type"] == "find" : # 配對對手
						print(self.user)
						if self.user[username][2] :
							self.Q.put((username, "type=peer&user=" + peername))
							self.Q.put((peername, "type=peer&user=" + username))
							pass
						else :
							findPeer = False
							for user in self.user :
								if not self.user[user][2] and user != username :
									peername = user
									print(username + ' peer is ' + peername)
									self.user[username][2] = True # 雙方都需配成 peer
									self.user[peername][2] = True # 雙方都需配成 peer
									self.Q.put((username, "type=peer&user=" + peername))
									self.Q.put((peername, "type=peer&user=" + username))
									initialboard = ServerInterface.Serverinterface()
									self.Q.put((username, "type=initStep&first=0&data=" + initialboard ))	
									self.Q.put((peername, "type=initStep&first=1&data=" + initialboard ))
									findPeer = True
									break
							if not findPeer :
								print('no peer')
								self.Q.put((username, "type=noPeer"))
					# -------------------------------------------------------------------- #
					elif D["type"] == "peer" :  # 設定 match 對手
						peername = D["user"]
					# -------------------------------------------------------------------- #
					elif D["type"] == "nextStep" : # 將下一步的棋步傳給對手
						if isMyTurn :
							#print(D["data"])
							self.Q.put((peername, "type=nextStep&user=" + username + "&data=" + D["data"]))
							isMyTurn = False
						else :
							self.Q.put((username, "type=turnError"))
					# -------------------------------------------------------------------- #
					elif D["type"] == "waitNext" : # 等待我方下下一步棋
						self.Q.put((username, "type=waitNextOK"))
						isMyTurn = True
					# -------------------------------------------------------------------- #
					elif D['type'] == "first": # 設成有先手權
						isMyTurn = True	
					# -------------------------------------------------------------------- #
					elif D["type"] == "gameOver" : # 遊戲中止
						print('game match break')
						try :
							self.user[username][2] = False
						except KeyError :
							pass
						try :
							self.user[peername][2] = False
						except KeyError :
							pass
						peername = ""
						isMyTurn = False
						print(self.user)
					# -------------------------------------------------------------------- #
					elif D["type"] == "logout" :
						sock.sendall(str2b("type=logout"))
						try : # 傳送遊戲中止
							self.Q.put((peername, "type=gameOver"))
						except KeyError :
							pass
						sock.close()
						del self.user[username]
						try :
							self.user[peername][2] = False # 將他遊玩的對手設置成未配對
						except KeyError :
							pass
						break
							
					# self.Q.put( (username, data) )
			except ConnectionResetError :
				try : # 傳送遊戲中止
					self.Q.put((peername, "type=gameOver"))
				except KeyError :
					pass
				sock.close() # 關閉連線
				if not username == '' : # 刪除離線使用者
					del self.user[username]				
				try :
					self.user[peername][2] = False # 將他遊玩的對手設置成未配對
				except KeyError :
					pass
				print(self.user)
				break
		exit()
		
if __name__ == "__main__" :
	s = server()
	s.run()
	
