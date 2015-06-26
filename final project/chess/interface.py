import sys
import random

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

def interface():
	column = 8
	row = 4
	
	#for j in range(row):
	#	for i in range(column):
	#		print("----",end="")
	#	print("-")
	#	print("|   |   |   |   |   |   |   |   |")
	#for i in range(column):
	#	print("----",end="")
	#print("-")
	
	# record : store non-repeated random number from 0 to 31
	record=[]     
	for j in range(32):
		a = random.randint(0,31)
		k = 1
		while True:
			k = 1
			for i in record:
				if i == a:
					a = a + 1
					k=0
					if a == 32:
						a = 0
					break
			#print("k is : " + str(k))
			if k == 1:
				record.append(a)
				break
	
	print(record)
	
	# give chess its initialized position
	k=1
	for i in record:
		y=int(i/8)
		x=int(i%8)
		chess[str(k)][2][0]=x
		chess[str(k)][2][1]=y
		k=k+1
	
	#for i in range(32):
	#	print(chess[str(i+1)])	
		
	# print chess board 
	for j in range(row):
		for i in range(column):
			print("-----",end="")
		print("-")
		
		for k in range(column):
			for i in range(32):
				if chess[str(i+1)][2][0] == k:
					if chess[str(i+1)][2][1] == row-j-1 :
						print("| " + chess[str(i+1)][0] + " ",end="")
						break
		print("|")	
	for i in range(column):
		print("-----",end="")
	print("-")
	
	# key value : "1"~"32"
	# chessMode : store key
	chessMode = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	for i in range(32):
		x=chess[str(i+1)][2][0]
		y=chess[str(i+1)][2][1]
		chessMode[x][y]=str(i+1)       #  chessMode[x][y] = key
	
	#print(chessMode)
	
	while True:
		print("Please choose operation: (1) open chess  (2) move chess")
		opeartion = input()
		if opeartion=="1":
			data =  input("Please input position x,y\n")
			x = int(data[0])
			y = int(data[2])
			if x <8 and y<4 and x>=0 and y>=0:
				if chess[chessMode[x][y]][3] == 0:   #  chessMode[x][y]
					chess[chessMode[x][y]][3] = 1
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
				if source_x <8 and source_y<4 and  source_x>=0 and  source_y>=0:
					if chessMode[source_x][source_y] == "0":	
						print("no chess")
					elif chess[chessMode[source_x][source_y]][3] == 0:
						print("this is dark chess1")
					else:
						break
				else:
					print("out of border")
				
			while True:
				destination = input("destination position x,y\n")
				destination_x = int(destination[0])
				destination_y = int(destination[2])
				if destination_x <8 and destination_y<4 and destination_x>=0 and destination_y>=0:
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
													chess[chessMode[destination_x][destination_y]][2][0]=-1
													chess[chessMode[destination_x][destination_y]][2][1]=-1
													chess[chessMode[destination_x][destination_y]][3] = 3
													chess[chessMode[source_x][source_y]][2][0]=destination_x
													chess[chessMode[source_x][source_y]][2][1]=destination_y
													chessMode[destination_x][destination_y]=chessMode[source_x][source_y]
													chessMode[source_x][source_y]="0"
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
													chess[chessMode[destination_x][destination_y]][2][0]=-1
													chess[chessMode[destination_x][destination_y]][2][1]=-1
													chess[chessMode[destination_x][destination_y]][3] = 3
													chess[chessMode[source_x][source_y]][2][0]=destination_x
													chess[chessMode[source_x][source_y]][2][1]=destination_y
													chessMode[destination_x][destination_y]=chessMode[source_x][source_y]
													chessMode[source_x][source_y]="0"
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
								print(chessMode[destination_x][destination_y])
							# if destination position is not empty
							else:
								print("aaaaaa" + chessMode[destination_x][destination_y])
								# if destination position is bright chess
								
								if chess[chessMode[destination_x][destination_y]][3]==1:
									print(chessMode[destination_x][destination_y])
									source_key = chessMode[source_x][source_y]
									destination_key = chessMode[destination_x][destination_y]
									tempt=0
									# can eat or not
									for i in rule[source_key]:
										# can eat
										if i == int(destination_key):
											tempt=1
											chess[chessMode[destination_x][destination_y]][2][0]=-1
											chess[chessMode[destination_x][destination_y]][2][1]=-1
											chess[chessMode[destination_x][destination_y]][3] = 3
											chess[chessMode[source_x][source_y]][2][0]=destination_x
											chess[chessMode[source_x][source_y]][2][1]=destination_y
											chessMode[destination_x][destination_y]=chessMode[source_x][source_y]
											chessMode[source_x][source_y]="0"
											print(chessMode[destination_x][destination_y])
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
			
if __name__ == "__main__":
	interface()