from socket import *
from threading import *
from _thread import *
from time import sleep
from random import randint 
from queue import *
import signal
import struct
import uuid
import sys
import getpass

from converter import *

chess={
'1':[u'將','b',[0,0],0],   #[0]:name,[1]:group,[2]:position, [3]:state(open:1 or close:0),useless!!
'2':[u'士','b',[0,0],0],
'3':[u'士','b',[0,0],0],
'4':[u'包','b',[0,0],0],
'5':[u'包','b',[0,0],0],
'6':[u'象','b',[0,0],0],
'7':[u'象','b',[0,0],0],
'8':[u'車','b',[0,0],0],
'9':[u'車','b',[0,0],0],
'10':[u'馬','b',[0,0],0],
'11':[u'馬','b',[0,0],0],
'12':[u'卒','b',[0,0],0],
'13':[u'卒','b',[0,0],0],
'14':[u'卒','b',[0,0],0],
'15':[u'卒','b',[0,0],0],
'16':[u'卒','b',[0,0],0],
'17':[u'帥','r',[0,0],0],
'18':[u'仕','r',[0,0],0],
'19':[u'仕','r',[0,0],0],
'20':[u'炮','r',[0,0],0],
'21':[u'炮','r',[0,0],0],
'22':[u'相','r',[0,0],0],
'23':[u'相','r',[0,0],0],
'24':[u'轟','r',[0,0],0],
'25':[u'轟','r',[0,0],0],
'26':[u'傌','r',[0,0],0],
'27':[u'傌','r',[0,0],0],
'28':[u'兵','r',[0,0],0],
'29':[u'兵','r',[0,0],0],
'30':[u'兵','r',[0,0],0],
'31':[u'兵','r',[0,0],0],
'32':[u'兵','r',[0,0],0]
}

rule={
'1':[17,18,19,20,21,22,23,24,25,26,27],
'2':[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32],
'3':[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32],
'4':[17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32],
'5':[17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32],
'6':[20,21,22,23,24,25,26,27,28,29,30,31,32],
'7':[20,21,22,23,24,25,26,27,28,29,30,31,32],
'8':[20,21,24,25,26,27,28,29,30,31,32],
'9':[20,21,24,25,26,27,28,29,30,31,32],
'10':[20,21,26,27,28,29,30,31,32],
'11':[20,21,26,27,28,29,30,31,32],
'12':[28,29,30,31,32,17],
'13':[28,29,30,31,32,17],
'14':[28,29,30,31,32,17],
'15':[28,29,30,31,32,17],
'16':[28,29,30,31,32,17],
'17':[1,2,3,4,5,6,7,8,9,10,11],
'18':[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
'19':[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
'20':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
'21':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
'22':[4,5,6,7,8,9,10,11,12,13,14,15,16],
'23':[4,5,6,7,8,9,10,11,12,13,14,15,16],
'24':[4,5,8,9,10,11,12,13,14,15,16],
'25':[4,5,8,9,10,11,12,13,14,15,16],
'26':[4,5,10,11,12,13,14,15,16],
'27':[4,5,10,11,12,13,14,15,16],
'28':[12,13,14,15,16,1],
'29':[12,13,14,15,16,1],
'30':[12,13,14,15,16,1],
'31':[12,13,14,15,16,1],
'32':[12,13,14,15,16,1]
}

chessMode = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

my_turn = False
my_group = "red"  #  "red" or "black"
judge_group = True

class ChatRoomClient :
	def __init__(self, ip = "127.0.0.1", port = 7000) :
		self.ip = ip
		self.port = port
		self.cond = Condition()
		self.mod = False
		self.exe = True
		self.peer = ""
		self.hint = "Command is -->"
		self.socket = socket(AF_INET, SOCK_STREAM)
		self.socket.connect((self.ip, self.port))
		self.run()
		
	def cmd(self) :
		while self.exe :
			if self.mod :
				command = input()
				command = command.split(" ")
				
				if command[0] == "find" :
					self.socket.sendall(str2b("type=find"))
					
				elif command[0] == "next" :
					global my_turn
					if my_turn == True:
						s = self.docommand()
						my_turn = False
						self.interface()
						self.socket.sendall(str2b("type=nextStep&data=" + s))
					else:
						print("it's not your turn")
					#self.socket.sendall(str2b("type=nextStep&data=" + s))
				elif command[0] == "quit" :
					self.socket.sendall(str2b("type=gameOver"))
				elif command[0] == "logout" :
					self.socket.sendall(str2b("type=logout"))
					break
					
				else :
					if self.peer == "" :
						print("unknow ", command[0])
					else :
						msg = ' '.join(command[0:len(command)])
						self.socket.sendall(str2b("type=talk&to=%s&message=%s" % (self.peer, msg)))
					
	def read(self) :
		while self.exe :
			data = self.socket.recv(4096)
			if len(data) > 0 :	
				D = str2D(b2str(data))
				
				print(D)
				global chess
				global chessMode
				global my_turn
				global judge_group
				global my_group
				
				if D["type"] == "nickname" : # 登錄驗證
					user = input('user :')
					msg = 'type=nickname&name=%s' % (user,)
					self.socket.sendall(str2b(msg))
				# -------------------------------------------------------------------- #
				elif D["type"] == "loginOK" : # 登錄成功
					print("get nickname, start game mode")
					self.mod = True
				# -------------------------------------------------------------------- #
				elif D["type"] == "peer" : # 確認對手
					self.socket.sendall(str2b("type=peer&user=" + D["user"]))
					print("Your peer is " + D["user"])
				# -------------------------------------------------------------------- #
				elif D['type'] == "noPeer" : # 警告沒有對手
					print('no peer QQ')
					pass
				# -------------------------------------------------------------------- #
				elif D['type'] == "initStep" : # 擁有初始棋盤
					print('initial Chess')

					record=[]
					array = D["data"].split(",")
					for i in array:
						record.append(int(i))

					# give chess its initialized position
					k=1
					for i in record:
						y=int(i/8)
						x=int(i%8)
						chess[str(k)][2][0]=x
						chess[str(k)][2][1]=y
						k=k+1
						
					# print chess board 
					self.interface()
					
					# key value : "1"~"32"
					# chessMode : store key
					for i in range(32):
						x=chess[str(i+1)][2][0]
						y=chess[str(i+1)][2][1]
						chessMode[x][y]=str(i+1)       #  chessMode[x][y] = key
					
					if D["first"] == "1" :
						print('my turn')
						my_turn = True
						judge_group = False
						self.socket.sendall(str2b("type=first"))
				# -------------------------------------------------------------------- #
				elif D['type'] == "nextStep" : # 下一步
					# do some next step !
					array = D["data"].split(",")
					if array[0] == "1":
						x = int(array[1])
						y = int(array[2])
						chess[chessMode[x][y]][3] = 1
					elif array[0] == "2":
						source_x = int(array[1])
						source_y = int(array[2])
						destination_x = int(array[3])
						destination_y = int(array[4])
						chess[chessMode[source_x][source_y]][2][0]=destination_x
						chess[chessMode[source_x][source_y]][2][1]=destination_y
						chessMode[destination_x][destination_y]=chessMode[source_x][source_y]
						chessMode[source_x][source_y]="0"
					elif array[0] == "3":
						source_x = int(array[1])
						source_y = int(array[2])
						destination_x = int(array[3])
						destination_y = int(array[4])
						chess[chessMode[destination_x][destination_y]][2][0]=source_x
						chess[chessMode[destination_x][destination_y]][2][1]=source_y
						chess[chessMode[destination_x][destination_y]][3] = 3
						chess[chessMode[source_x][source_y]][2][0]=destination_x
						chess[chessMode[source_x][source_y]][2][1]=destination_y
						chessMode[destination_x][destination_y]=chessMode[source_x][source_y]
						chessMode[source_x][source_y]="0"
					elif array[0] == "4":
						x = int(array[1])
						y = int(array[2])
						chess[chessMode[x][y]][3] = 1
						my_group="b"
						print("my group is " + my_group)		
					elif array[0] == "5":
						x = int(array[1])
						y = int(array[2])
						chess[chessMode[x][y]][3] = 1
						my_group="r"
						print("my group is " + my_group)
						
					self.interface()
					self.socket.sendall(str2b("type=waitNext"))
					pass
				# -------------------------------------------------------------------- #
				elif D['type'] == "waitNextOK" : # 得到下一步許可
					my_turn = True
					print("next step ?")
				# -------------------------------------------------------------------- #
				elif D['type'] == "turnError" : # 回合錯誤警告
					print("it's not your turn")
				# -------------------------------------------------------------------- #
				elif D['type'] == "gameOver" : # 結束遊戲
					self.socket.sendall(str2b("type=gameOver"))
				# -------------------------------------------------------------------- #
				elif D["type"] == "logout" : # 中止遊戲
					print('logout')
					self.exe = False
					break
					
	def run(self) :
		
		rThread = Thread(target = self.read)
		cThread = Thread(target = self.cmd)
		
		rThread.start()
		cThread.start()
		
		print("Client Start OK")
		
		cThread.join()
		rThread.join()
		
	def interface(self):
		column = 8
		row = 4
		# print chess board 
		for j in range(row):
			for i in range(column):
				print("-----",end="")
			print("-")
		
			for k in range(column):
				for i in range(32):
					if chess[str(i+1)][2][0] == k:
						if chess[str(i+1)][2][1] == row-j-1 :
							if chess[str(i+1)][3]==0:
								print("| O "+ " ",end="")
							elif chess[str(i+1)][3]==1:
								print("| " + chess[str(i+1)][0] + " ",end="")
							elif chess[str(i+1)][3]==3:
								print("|    ",end="")
							break
			print("|")	
		for i in range(column):
			print("-----",end="")
		print("-")
	
	
	def docommand(self):
		global chess
		global chessMode
		global rule
		global judge_group
		global my_group
		send_string=""
		# send_string = "1,x,y" -> open chess
		# send_string = "2,x,y,x,y" -> move source chess to destination chess position
		# send_string = "3,x,y,x,y" -> source chess eat destination chess and move to destination chess position
		# send_string = "4,x,y" -> open chess, first group is red
		# send_string = "5,x,y" -> open chess, first group is black
		while True:
			print("Please choose operation: (1) open chess  (2) move chess")
			opeartion = input()
			if opeartion=="1":
				data =  input("Please input position x,y\n")
				x = int(data[0])
				y = int(data[2])
				if x <8 and y<4:
					if chess[chessMode[x][y]][3] == 0:   #  chessMode[x][y]
						chess[chessMode[x][y]][3] = 1
						if judge_group == False:
							my_group = chess[chessMode[x][y]][1]
							if my_group == "r":
								send_string = send_string + "4," + str(x) + "," + str(y)
							elif my_group == "b":
								send_string = send_string + "5," + str(x) + "," + str(y)
							judge_group = True
						else: 
							send_string = send_string + "1," + str(x) + "," + str(y)
						return send_string
					elif chessMode[x][y] == "0":	
						print("no chess")
					else:
						print("wrong operation")
				else:
					print("out of border")
		
			elif opeartion=="2":
				print("Please input position x,y to dest_x,dest_y")
				source_x = 0
				source_y = 0
				while True:
					source =  input("source position x,y\n")
					source_x = int(source[0])
					source_y = int(source[2])
					if source_x <8 and source_y<4:
						if chessMode[source_x][source_y] == "0":	
							print("no chess")
						elif chess[chessMode[source_x][source_y]][3] == 0:
							print("this is dark chess1")
						elif chess[chessMode[source_x][source_y]][1] != my_group:
							print("this is not your group")
						else:
							break
					else:
						print("out of border")
				
				#send_string = send_string + "2," + source_x + "," + source_y + ","
				
				while True:
					destination = input("destination position x,y\n")
					destination_x = int(destination[0])
					destination_y = int(destination[2])
					if destination_x <8 and destination_y<4:
						# this is gunfire
						if chessMode[source_x][source_y] == "4" or chessMode[source_x][source_y] == "5" or chessMode[source_x][source_y] == "20" or chessMode[source_x][source_y] == "21":
							# move one space
							if abs(destination_x-source_x) + abs(destination_y-source_y) == 1:
								# if destination position is empty
								if chessMode[destination_x][destination_y]=="0":
									chess[chessMode[source_x][source_y]][2][0]=destination_x
									chess[chessMode[source_x][source_y]][2][1]=destination_y
									chessMode[destination_x][destination_y]=chessMode[source_x][source_y]
									chessMode[source_x][source_y]="0"
									send_string = send_string + "2," + str(source_x) + "," + str(source_y) + ","
									send_string = send_string + str(destination_x) + "," + str(destination_y)
									return send_string
								# if destination position is not empty
								else:
									print("Can not eat")
							# move more than one space
							else:
								# walk y axis 
								if abs(destination_x-source_x)==0 and abs(destination_y-source_y)>1:
									k = 0
									t = 0
									if destination_y > source_y:
										k = destination_y - source_y -1
										t = source_y
									elif source_y > destination_y:
										k = source_y - destination_y -1
										t = destination_y
								
									judge = 0
									for i in range(k):
										i = i + 1
										if chessMode[source_x][t+i] != "0":
											judge = judge + 1
										
									# in y axis, only one chess exist between source and destination
									if judge == 1:
										# rule
										# if destination position is empty
										if chessMode[destination_x][destination_y]=="0":
											print("Error!! Wrong moves1!")
										# if destination position is not empty
										else:
											# if destination position is bright chess
											if chess[chessMode[destination_x][destination_y]][3]==1:
												source_key = chessMode[source_x][source_y]
												destination_key = chessMode[destination_x][destination_y]
												tempt=0
												# can eat or not
												for i in rule[source_key]:
													# can eat
													if i == int(destination_key):
														tempt=1
														chess[chessMode[destination_x][destination_y]][2][0]=source_x
														chess[chessMode[destination_x][destination_y]][2][1]=source_y
														chess[chessMode[destination_x][destination_y]][3] = 3
														chess[chessMode[source_x][source_y]][2][0]=destination_x
														chess[chessMode[source_x][source_y]][2][1]=destination_y
														chessMode[destination_x][destination_y]=chessMode[source_x][source_y]
														chessMode[source_x][source_y]="0"
														send_string = send_string + "3," + str(source_x) + "," + str(source_y) + ","
														send_string = send_string + str(destination_x) + "," + str(destination_y)
														return send_string
														break
												# can not eat
												if tempt==0:
													print("Can not eat!")
											# if destination position is dark chess
											else:
												print("Destination position is dark chess2!")						
									# in y axis, more than one or no chess exist between source and destination
									else:
										print("Error!! Wrong moves2!")
										
								# walk x axis 
								elif abs(destination_x-source_x)>1 and abs(destination_y-source_y)==0:
									k = 0
									t = 0
									if destination_x > source_x:
										k = destination_x - source_x -1
										t = source_x
									elif source_x > destination_x:
										k = source_x - destination_x -1 
										t = destination_x
									
									judge = 0
									for i in range(k):
										i = i + 1
										if chessMode[t+i][source_y] != "0":
											judge = judge + 1
								
									# in x axis, only one chess exist between source and destination
									if judge == 1:
										# rule
										# if destination position is empty
										if chessMode[destination_x][destination_y]=="0":
											print("Error!! Wrong moves3!")
										# if destination position is not empty
										else:
											# if destination position is bright chess
											if chess[chessMode[destination_x][destination_y]][3]==1:
												source_key = chessMode[source_x][source_y]
												destination_key = chessMode[destination_x][destination_y]
												tempt=0
												# can eat or not
												for i in rule[source_key]:
													# can eat
													if i == int(destination_key):
														tempt=1
														chess[chessMode[destination_x][destination_y]][2][0]=source_x
														chess[chessMode[destination_x][destination_y]][2][1]=source_y
														chess[chessMode[destination_x][destination_y]][3] = 3
														chess[chessMode[source_x][source_y]][2][0]=destination_x
														chess[chessMode[source_x][source_y]][2][1]=destination_y
														chessMode[destination_x][destination_y]=chessMode[source_x][source_y]
														chessMode[source_x][source_y]="0"
														send_string = send_string + "3," + str(source_x) + "," + str(source_y) + ","
														send_string = send_string + str(destination_x) + "," + str(destination_y)
														return send_string
														break
												# can not eat
												if tempt==0:
													print("Can not eat!")
											# if destination position is dark chess
											else:
												print("Destination position is dark chess3!")
									# in x axis, more than one or no chess exist between source and destination
									else:
										print("Error!! Wrong moves4!")	
								else:
									print("Error!! Wrong moves5!")
						# this is not gunfire
						else:
							if abs(destination_x-source_x) + abs(destination_y-source_y) == 1:
								# if destination position is empty
								if chessMode[destination_x][destination_y]=="0":
									chess[chessMode[source_x][source_y]][2][0]=destination_x
									chess[chessMode[source_x][source_y]][2][1]=destination_y
									chessMode[destination_x][destination_y]=chessMode[source_x][source_y]
									chessMode[source_x][source_y]="0"
									send_string = send_string + "2," + str(source_x) + "," + str(source_y) + ","
									send_string = send_string + str(destination_x) + "," + str(destination_y)
									return send_string
								# if destination position is not empty
								else:
									# if destination position is bright chess
									if chess[chessMode[destination_x][destination_y]][3]==1:
										source_key = chessMode[source_x][source_y]
										destination_key = chessMode[destination_x][destination_y]
										tempt=0
										# can eat or not
										for i in rule[source_key]:
											# can eat
											if i == int(destination_key):
												tempt=1
												chess[chessMode[destination_x][destination_y]][2][0]=source_x
												chess[chessMode[destination_x][destination_y]][2][1]=source_y
												chess[chessMode[destination_x][destination_y]][3] = 3
												chess[chessMode[source_x][source_y]][2][0]=destination_x
												chess[chessMode[source_x][source_y]][2][1]=destination_y
												chessMode[destination_x][destination_y]=chessMode[source_x][source_y]
												chessMode[source_x][source_y]="0"
												send_string = send_string + "3," + str(source_x) + "," + str(source_y) + ","
												send_string = send_string + str(destination_x) + "," + str(destination_y)
												return send_string
												break
										# can not eat
										if tempt==0:
											print("Can not eat!")
									# if destination position is dark chess
									else:
										print("Destination position is dark chess4!")
							else:
								print("Error!! Wrong moves6!")
					else:
						print("out of border")
					break
			
if __name__ == "__main__" :
	c = ChatRoomClient()