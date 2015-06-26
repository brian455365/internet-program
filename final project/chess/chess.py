from conio import *
import random
from colorama import Fore, Back, Style

__chess__x__ = 1
__chess__y__ = 1

CHESSMAN = { # id symbol level group
	0  : (u'  ', 0, None),
	1  : (u'將', 7, True),
	2  : (u'士', 6, True),
	3  : (u'士', 6, True),
	4  : (u'象', 5, True),
	5  : (u'象', 5, True),
	6  : (u'車', 4, True),
	7  : (u'車', 4, True),
	8  : (u'馬', 3, True),
	9  : (u'馬', 3, True),
	10 : (u'包', 2, True),
	11 : (u'包', 2, True),
	12 : (u'卒', 1, True),
	13 : (u'卒', 1, True),
	14 : (u'卒', 1, True),
	15 : (u'卒', 1, True),
	16 : (u'卒', 1, True),
	17 : (u'帥', 7, False),
	18 : (u'仕', 6, False),
	19 : (u'仕', 6, False),
	20 : (u'相', 5, False),
	21 : (u'相', 5, False),
	22 : (u'轟', 4, False),
	23 : (u'轟', 4, False),
	24 : (u'傌', 3, False),
	25 : (u'傌', 3, False),
	26 : (u'炮', 2, False),
	27 : (u'炮', 2, False),
	28 : (u'兵', 1, False),
	29 : (u'兵', 1, False),
	30 : (u'兵', 1, False),
	31 : (u'兵', 1, False),
	32 : (u'兵', 1, False),
	33 : (u'？', 0, None)
}

# chess status  : chess pos | id | open or not

def chess(x = 1, y = 1) :
	global __chess__x__
	global __chess__y__
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	__chess__x__ = x
	__chess__y__ = y
	y_wall = (0, 2, 4, 6, 8)
	x_wall = (0, 3, 6, 9, 12, 15, 18, 21, 24)
	blank = (1, 4, 7, 10, 13, 16, 19, 22)
	for j in range(9) :
		if j in y_wall :
			inactive(__chess__x__, j + __chess__y__, ' '*25)
			continue
		for i in range(25) :
			if i in blank :
				active(i + __chess__x__ , j + __chess__y__, u'將')
			elif i in x_wall :
				inactive(i + __chess__x__, j + __chess__y__, ' ')
				
def chessSet(x = 1, y = 1, chessman = u'士') :
	global __chess__x__
	global __chess__y__
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	y_pos = (1, 3, 5, 7)
	x_pos = (1, 4, 7, 10, 13, 16, 19, 22)
	active(x_pos[x - 1] + __chess__x__ , y_pos[y - 1] + __chess__y__, chessman)
	
def chessPos(pos) :
	if str(type(pos)) == "<class 'tuple'>" :
		return (pos[1] -  1)*8 + pos[0]
	elif str(type(pos)) == "<class 'int'>" :
		__x__ = pos % 8
		__y__ = int(pos / 8) + 1
		if __x__ == 0 :
			__x__ = 8
			__y__ = __y__ - 1
		return (__x__, __y__)
	elif str(type(pos)) == "<type 'int'>" :
		__x__ = pos % 8
		__y__ = int(pos / 8) + 1
		if __x__ == 0 :
			__x__ = 8
			__y__ = __y__ - 1			
		return (__x__, __y__)
		
def chessTable() :
	__chess__table__ = dict()
	for i in range(1, 33) :
		__chess__table__[i] = [i, False]
	return __chess__table__
	
def initChess() :
	rArray = [i for i in range(1, 33)]
	random.shuffle(rArray)
	initStr = '|'.join([str(e) for e in rArray])
	return initStr
	
class Chess :
	__chess__x__ = 1
	__chess__y__ = 1
	SELECT = 1
	SELECTED = 2
	UNSELECT = 3
	RED = 4
	BLACK = 5
	
	def __init__(self) :
		self.table = dict()
		self.pos = [1, 1]
		self.sel = [-1, -1]
		self.turn = None
		self.step = 1
		self.firstTurn = None
		self.initChess()
		
	def chessColor(self, flag) :
		if flag == self.SELECT :
			setBGColor(Back.RED, Style.BRIGHT)
			setFGColor(Fore.WHITE, Style.DIM)
		elif flag == self.SELECTED :
			setBGColor(Back.GREEN, Style.BRIGHT)
			setFGColor(Fore.WHITE, Style.DIM)
		elif flag == self.UNSELECT :
			setBGColor(Back.YELLOW, Style.BRIGHT)
			setFGColor(Fore.WHITE, Style.BRIGHT)
		elif flag == self.RED :
			setBGColor(Back.BLACK, Style.DIM)
			setFGColor(Fore.RED, Style.BRIGHT)
		elif flag == self.BLACK :
			setBGColor(Back.BLACK, Style.DIM)
			setFGColor(Fore.WHITE, Style.BRIGHT)
			
	def chess(self, x = 1, y = 1) :
		if x <= 0 :
			x = 1
		if y <= 0 :
			y = 1
		self.__chess__x__ = x
		self.__chess__y__ = y
		y_wall = (0, 2, 4, 6, 8)
		x_wall = (0, 3, 6, 9, 12, 15, 18, 21, 24)
		blank = (1, 4, 7, 10, 13, 16, 19, 22)
		for j in range(9) :
			if j in y_wall :
				inactive(self.__chess__x__, j + self.__chess__y__, ' '*25)
				continue
			for i in range(25) :
				if i in blank :
					#active(i + self.__chess__x__ , j + self.__chess__y__, u'  ')
					self.chessColor(self.UNSELECT)
					drawText(i + self.__chess__x__, j + self.__chess__y__, u'  ')
					defaultColor()
				elif i in x_wall :
					inactive(i + self.__chess__x__, j + self.__chess__y__, ' ')
					
	def chessman(self, x = 1, y = 1, symbol = u' ', style = UNSELECT) :
		if x <= 0 :
			x = 1
		if y <= 0 :
			y = 1
		y_pos = (1, 3, 5, 7)
		x_pos = (1, 4, 7, 10, 13, 16, 19, 22)
		#active(x_pos[x - 1] + self.__chess__x__ , y_pos[y - 1] + self.__chess__y__, symbol)
		self.chessColor(style)
		drawText(x_pos[x - 1] + self.__chess__x__, y_pos[y - 1] + self.__chess__y__, symbol)
		defaultColor()
		
	def chessPos(self, pos) :
		if str(type(pos)) == "<class 'tuple'>" :
			return (pos[1] -  1)*8 + pos[0]
		elif str(type(pos)) == "<type 'tuple'>" :
			return (pos[1] -  1)*8 + pos[0]
		elif str(type(pos)) == "<class 'list'>" :
			return (pos[1] -  1)*8 + pos[0]
		elif str(type(pos)) == "<type 'list'>" :
			return (pos[1] -  1)*8 + pos[0]
		elif str(type(pos)) == "<class 'int'>" :
			__x__ = pos % 8
			__y__ = int(pos / 8) + 1
			if __x__ == 0 :
				__x__ = 8
				__y__ = __y__ - 1
			return (__x__, __y__)
		elif str(type(pos)) == "<type 'int'>" :
			__x__ = pos % 8
			__y__ = int(pos / 8) + 1
			if __x__ == 0 :
				__x__ = 8
				__y__ = __y__ - 1			
			return (__x__, __y__)
			
	def initChess(self) :
		self.table = dict()
		self.pos = [1, 1]
		self.sel = [-1, -1]
		self.turn = None
		self.step = 1
		self.firstTurn = None
		for i in range(1, 33) :
			self.table[i] = [i, False]
		rArray = [i for i in range(1, 33)]
		cnt = 1
		random.shuffle(rArray)
		for e in rArray :
			self.table[cnt][0] = e
			cnt = cnt + 1
		initStr = '|'.join([str(e) for e in rArray])
		return initStr
		
	def drawChess(self, x = 1, y = 1) : # 畫棋盤上所有棋子
		self.chess(x, y)
		for k in list(self.table.keys()) :
			pos = self.chessPos(k)
			if self.table[k][1] :
				self.chessman(pos[0], pos[1], CHESSMAN[self.table[k][0]][0])
			else :
				self.chessman(pos[0], pos[1], u'？')
				
	def drawChessman(self, x = 1, y = 1, style = UNSELECT) :
		if self.table[self.chessPos((x, y))][1] :
			self.chessman(x, y, CHESSMAN[self.table[self.chessPos((x, y))][0]][0], style)
		else :
			self.chessman(x, y, u'？', style)
			
	def chessmanInfo (self, x = 1, y = 1) : # 回傳 table 上棋子的訊息
		__chessman_id__  = self.table[self.chessPos((x, y))][0]
		__chess_open__ = self.table[self.chessPos((x, y))][1]
		__chessman_level__  = CHESSMAN[__chessman_id__][1]
		__chessman_group__  = CHESSMAN[__chessman_id__][2]
		return (__chessman_id__, __chessman_level__, __chessman_group__, __chess_open__)
		
	def chessInfo(self) : # 取得棋盤上的資訊
		__chess__info__ = []
		for key in list(self.table.keys()) :
			if self.table[key][1] :
				__chess__info__.append(self.table[key][0])
			else :
				__chess__info__.append(33)
		__chess__info__ = [str(e) for e in __chess__info__]
		return '|'.join(__chess__info__)
		
	def chessTableInfo(self) :
		__chess_table_info__ = []
		for key in list(self.table.keys()) :
			__chess_table_info__.append(self.table[key])
		__chess_table_info__ = [str(e[0]) + "," + str(int(e[1])) for e in __chess_table_info__]
		return '|'.join(__chess_table_info__)
		
	def drawChessTableInfo(self, string) : # 印出棋盤資訊，然後將資訊複製到棋盤的Table
		__chess_table_info__ = string.split('|')
		cnt = 1
		pos = [1, 1]
		for e in __chess_table_info__ :
			e = e.split(',')
			e = [int(e[0]), bool(int(e[1]))]
			self.table[cnt] = e
			pos = self.chessPos(cnt)
			if not e[1] :
				self.chessman(pos[0], pos[1], u'？')
			elif CHESSMAN[e[0]][2] :
				self.chessman(pos[0], pos[1], CHESSMAN[e[0]][0], self.BLACK)
			elif not CHESSMAN[e[0]][2] :
				self.chessman(pos[0], pos[1], CHESSMAN[e[0]][0], self.RED)
			cnt = cnt + 1	
			
	def drawChessInfo(self, string) : # 印出棋盤資訊，然後將資訊複製到棋盤的Table
		__chess__info__ = string.split('|')
		cnt = 1
		pos = [1, 1]
		for e in __chess__info__ :
			if int(e) == 33 :
				self.table[cnt] = [int(e), False]
			else :
				self.table[cnt] = [int(e), True] 
			pos = self.chessPos(cnt)
			if pos[0] == self.sel[0] and pos[1] == self.sel[1] :
				self.chessman(pos[0], pos[1], CHESSMAN[int(e)][0], self.SELECTED)
			else :
				self.chessman(pos[0], pos[1], CHESSMAN[int(e)][0])
			cnt = cnt + 1
			
	def isWin(self) :
		__red__ = []
		__black__ = []
		for key in list(self.table.keys()) :
			if CHESSMAN[self.table[key][0]][2] == None :
				pass
			elif not CHESSMAN[self.table[key][0]][2] :
				__red__.append(self.table[key][0])
			elif CHESSMAN[self.table[key][0]][2] :
				__black__.append(self.table[key][0])
		if len(__red__) == 0 and len(__black__) > 0 :
			return True
		elif len(__black__) == 0 and len(__red__) > 0 :
			return False
		else :
			return None
		return None
	
	def getTurn(self) : # 取得目前的回合權
		return self.turn
		
	def getFirstTurn(self) : # 取得第一次的回合權
		return self.firstTurn
		
	def act(self, sx = -1, sy = -1) : # 回傳棋子能夠吃/移動的目標位置
		target = []
		if sx > 0 and sy > 0 :
			rule1 = [(1, 0), (-1, 0), (0, 1), (0, -1)] # 上 下 左 右
			rule2 = [(-1, -1), (1, -1), (-1, 1), (1, 1)] # 左上 右上 左下 右下
			ntx = 0 # 下一個目標的暫存
			nty = 0 # 下一個目標的暫存
			
			src = self.chessmanInfo(sx, sy)
			tmp = (0, 0, 0)
			
			if src[1] == 7 : # 將 帥
				for v in rule1 :
					ntx = sx + v[0]
					nty = sy + v[1]
					if ntx >= 1 and ntx <= 8 and nty >= 1 and nty <= 4 :
						tmp = self.chessmanInfo(ntx, nty)
						if tmp[1] <= 7 and (not tmp[1] == 1) :
							if tmp[1] > 0 :
								if tmp[2] ^ src[2] and tmp[3]:
									target.append((ntx, nty))
							else :
								target.append((ntx, nty)) # 可以走空白
								
							
			elif src[1] == 6 : # 士 仕
				for v in rule1 :
					ntx = sx + v[0]
					nty = sy + v[1]
					if ntx >= 1 and ntx <= 8 and nty >= 1 and nty <= 4 :
						tmp = self.chessmanInfo(ntx, nty)
						if tmp[1] <= 6 :
							if tmp[1] > 0 :
								if tmp[2] ^ src[2] and tmp[3]:
									target.append((ntx, nty))
							else :
								target.append((ntx, nty)) # 可以走空白
							
			elif src[1] == 5 : # 相 象
				for v in rule1 :
					ntx = sx + v[0]
					nty = sy + v[1]
					if ntx >= 1 and ntx <= 8 and nty >= 1 and nty <= 4 :
						tmp = self.chessmanInfo(ntx, nty)
						if tmp[1] <= 5 :
							if tmp[1] > 0  :
								if tmp[2] ^ src[2] and tmp[3] :
									target.append((ntx, nty))
							else :
								target.append((ntx, nty)) # 可以走空白
							
			elif src[1] == 4 : # 車 轟
				for v in rule1 :
					ntx = sx + v[0]
					nty = sy + v[1]
					if ntx >= 1 and ntx <= 8 and nty >= 1 and nty <= 4 :
						tmp = self.chessmanInfo(ntx, nty)
						if tmp[1] <= 4 :
							if tmp[1] > 0 :
								if tmp[2] ^ src[2] and tmp[3] :
									target.append((ntx, nty))
							else :
								target.append((ntx, nty)) # 可以走空白
							
			elif src[1] == 3 : # 馬 傌
				for v in rule1 :
					ntx = sx + v[0]
					nty = sy + v[1]
					if ntx >= 1 and ntx <= 8 and nty >= 1 and nty <= 4 :
						tmp = self.chessmanInfo(ntx, nty)
						if tmp[1] <= 3 :
							if tmp[1] > 0  :
								if tmp[2] ^ src[2] and tmp[3]:
									target.append((ntx, nty))
							else :
								target.append((ntx, nty)) # 可以走空白
				for v in rule2 : # 斜吃
					ntx = sx + v[0]
					nty = sy + v[1]
					if ntx >= 1 and ntx <= 8 and nty >= 1 and nty <= 4 :
						tmp = self.chessmanInfo(ntx, nty)
						if tmp[1] > 0 : # 不能斜走空白
							if tmp[2] ^ src[2] and tmp[3] :
								target.append((ntx, nty))
							
			elif src[1] == 2 : # 炮 包
				for v in rule1 :
					ntx = sx + v[0]
					nty = sy + v[1]
					if ntx >= 1 and ntx <= 8 and nty >= 1 and nty <= 4 :
						tmp = self.chessmanInfo(ntx, nty)
						if tmp[1] <= 2 :
							if tmp[1] > 0 :
								if tmp[2] ^ src[2] and tmp[3] :
									target.append((ntx, nty))
							else :
								target.append((ntx, nty)) # 可以走空白
				
				cnt = 0
				x_cnt = 0
				y_cnt = 0
				
				# 隔子攻擊確認 x 軸
				x_cnt = sx
				cnt = 0
				while x_cnt <= 8 :
					if not self.chessmanInfo(x_cnt, sy)[0]  == 0 :
						cnt = cnt + 1
						if cnt >= 3 :
							if self.chessmanInfo(x_cnt, sy)[2] ^ src[2] and self.chessmanInfo(x_cnt, sy)[3] :
								target.append((x_cnt, sy))
							break
					x_cnt = x_cnt + 1
				
				# 隔子攻擊確認 x 軸
				x_cnt = sx
				cnt = 0
				while x_cnt >= 1 :
					if not self.chessmanInfo(x_cnt, sy)[0]  == 0 :
						cnt = cnt + 1
						if cnt >= 3  :
							if self.chessmanInfo(x_cnt, sy)[2] ^ src[2] and self.chessmanInfo(x_cnt, sy)[3]:
								target.append((x_cnt, sy))
							break
					x_cnt = x_cnt - 1
				
				# 隔子攻擊確認 y 軸
				y_cnt = sy
				cnt = 0
				while y_cnt <= 4 :
					if not self.chessmanInfo(sx, y_cnt)[0]  == 0 :
						cnt = cnt + 1
						if cnt >= 3 :
							if self.chessmanInfo(sx, y_cnt)[2] ^ src[2] and self.chessmanInfo(sx, y_cnt)[3] :
								target.append((sx, y_cnt))
							break
					y_cnt = y_cnt + 1
				
				# 隔子攻擊確認 y 軸
				y_cnt = sy
				cnt = 0
				while y_cnt >= 1 :
					if not self.chessmanInfo(sx, y_cnt)[0]  == 0 :
						cnt = cnt + 1
						if cnt >= 3 :
							if self.chessmanInfo(sx, y_cnt)[2] ^ src[2] and self.chessmanInfo(sx, y_cnt)[3] :
								target.append((sx, y_cnt))
							break
					y_cnt = y_cnt - 1
						
							
			elif src[1] == 1 : # 卒 兵
				for v in rule1 :
					ntx = sx + v[0]
					nty = sy + v[1]
					if ntx >= 1 and ntx <= 8 and nty >= 1 and nty <= 4 :
						tmp = self.chessmanInfo(ntx, nty)
						if tmp[1] <= 1 or tmp[1] == 7 :
							if tmp[1] > 0 :
								if tmp[2] ^ src[2] and tmp[3] :
									target.append((ntx, nty))
							else :
								target.append((ntx, nty))
			
			# target = [CHESSMAN[self.chessmanInfo(t[0], t[1])[0]][0] for t in target]
		return target
		
	def move(self, Op) :
		sel = False
		newX = self.pos[0]
		newY = self.pos[1]
		
		if Op == KEY_UP :
			newY = self.pos[1] - 1
		elif Op == KEY_DOWN :
			newY = self.pos[1] + 1
		elif Op == KEY_LEFT :
			newX = self.pos[0] - 1
		elif Op == KEY_RIGHT :
			newX = self.pos[0] + 1
		elif Op == Enter :
			sel = True
		
		if newX >= 1 and newX <= 8 : # 新游標位置穩定
			if not self.pos[0] == newX :
				self.drawChessman(self.pos[0], self.pos[1])
				self.pos[0] = newX
			
		if newY >= 1 and newY <= 4 :
			if not self.pos[1] == newY : # 新游標位置穩定
				self.drawChessman(self.pos[0], self.pos[1])
				self.pos[1] = newY
				
		if sel : # 如果有按 ETR
			if not (self.sel[0]  == -1 and self.sel[1] == -1) : 
				# 做吃子或移棋
				if tuple(self.pos) in self.act(self.sel[0], self.sel[1]) : # 移到可以吃的地方 所以成功
					self.table[self.chessPos(self.pos)] = self.table[self.chessPos(self.sel)]
					self.table[self.chessPos(self.sel)] = [0, True]
					self.turn = not self.turn # 交換主導權
					self.step = self.step + 1
				self.drawChessman(self.sel[0], self.sel[1], self.UNSELECT) # 因為已經有選過哩 所以不管怎樣一定要做復原
				self.sel = [-1, -1]
			else :
				self.sel[0] = self.pos[0]
				self.sel[1] = self.pos[1]
				if self.table[self.chessPos(self.sel)][0] == 0 : # 沒有棋子
					self.sel = [-1, -1] # 不能選
				elif not self.table[self.chessPos(self.sel)][1] : # 蓋起來的狀態->掀開
					self.table[self.chessPos(self.sel)][1] = True
					if self.step == 1 :# 初始主導權
						self.turn = not self.chessmanInfo(self.sel[0], self.sel[1])[2]
						self.firstTurn = not self.turn
					else :
						self.turn = not self.turn
					self.step = self.step + 1
					self.drawChessman(self.sel[0], self.sel[1], self.UNSELECT)
					self.sel = [-1, -1]
				elif not self.chessmanInfo(self.sel[0], self.sel[1])[2] == self.turn :
					self.drawChessman(self.sel[0], self.sel[1], self.UNSELECT)
					self.sel = [-1, -1]
		if not (self.pos[0]	== self.sel[0] and self.pos[1] == self.sel[1]) :
			self.drawChessman(self.pos[0], self.pos[1], self.SELECT)
		if not (self.sel[0]  == -1 and self.sel[1] == -1) :
			if self.table[self.chessPos(self.sel)][0] == 0 : # 沒有棋子
				self.drawChessman(self.sel[0], self.sel[1], self.UNSELECT) # 直接取消選選取
				self.sel = [-1, -1] # 直接取消選選取
			else :
				self.drawChessman(self.sel[0], self.sel[1], self.SELECTED) # 進入選擇狀態

	def move2cmd(self, Op) :
		sel = False
		newX = self.pos[0]
		newY = self.pos[1]
		
		if Op == KEY_UP :
			newY = self.pos[1] - 1
		elif Op == KEY_DOWN :
			newY = self.pos[1] + 1
		elif Op == KEY_LEFT :
			newX = self.pos[0] - 1
		elif Op == KEY_RIGHT :
			newX = self.pos[0] + 1
		elif Op == Enter :
			sel = True
		
		if newX >= 1 and newX <= 8 : # 新游標位置穩定
			if not self.pos[0] == newX :
				self.drawChessman(self.pos[0], self.pos[1])
				self.pos[0] = newX
			
		if newY >= 1 and newY <= 4 :
			if not self.pos[1] == newY : # 新游標位置穩定
				self.drawChessman(self.pos[0], self.pos[1])
				self.pos[1] = newY
				
		if sel :
			return (self.pos[0], self.pos[1])

		if not (self.pos[0]	== self.sel[0] and self.pos[1] == self.sel[1]) :
			self.drawChessman(self.pos[0], self.pos[1], self.SELECT)
		if not (self.sel[0]  == -1 and self.sel[1] == -1) :
			if self.table[self.chessPos(self.sel)][0] == 0 : # 沒有棋子
				self.drawChessman(self.sel[0], self.sel[1], self.UNSELECT) # 直接取消選選取
				self.sel = [-1, -1] # 直接取消選選取
			else :
				self.drawChessman(self.sel[0], self.sel[1], self.SELECTED) # 進入選擇狀態
		return None
		
	def setSel(self, x = 1, y = 1) : # 使用 selection 是否成功
		if not (self.sel[0]  == -1 and self.sel[1] == -1) : 
			# 做吃子或移棋
			if tuple(self.pos) in self.act(self.sel[0], self.sel[1]) : # 移到可以吃的地方 所以成功
				self.table[self.chessPos(self.pos)] = self.table[self.chessPos(self.sel)]
				self.table[self.chessPos(self.sel)] = [0, True]
				self.turn = not self.turn # 交換主導權
				self.step = self.step + 1
				self.sel = [-1, -1]
				return True
			# self.drawChessman(self.sel[0], self.sel[1], self.UNSELECT) # 因為已經有選過哩 所以不管怎樣一定要做復原
			self.sel = [-1, -1]
			return False
		else :
			self.sel[0] = x
			self.sel[1] = y
			if self.table[self.chessPos(self.sel)][0] == 0 : # 沒有棋子
				self.sel = [-1, -1] # 不能選
			elif not self.table[self.chessPos(self.sel)][1] : # 蓋起來的狀態->掀開
				self.table[self.chessPos(self.sel)][1] = True
				if self.step == 1 :# 初始主導權
					self.turn = not self.chessmanInfo(self.sel[0], self.sel[1])[2]
					self.firstTurn = not self.turn
				else :
					self.turn = not self.turn
				self.step = self.step + 1
				# self.drawChessman(self.sel[0], self.sel[1], self.UNSELECT)
				self.sel = [-1, -1]
				return True
			elif not self.chessmanInfo(self.sel[0], self.sel[1])[2] == self.turn :
				# self.drawChessman(self.sel[0], self.sel[1], self.UNSELECT)
				self.sel = [-1, -1]
				return False
		return False
	
if __name__ == "__main__" :
	initscr()
	clsscr()
	
	#chess(10, 5)
	#chessSet(3, 3)
	
	#print(chessPos((1, 1)))
	#print(chessPos(2))
	#print(chessPos(31))
	#print(chessPos(11))
	#print(chessPos(21))
	
	#print(initChess().split('|'))
	#print(chessTable())
	
	# initA = initChess().split('|')
	
	# chess()
	# xy  = 0
	
	# i = 0
	# for e in initA :
	#	xy = chessPos(int(i))
	#	chessSet(xy[0], xy[1], CHESSMAN[int(e)][0])
	#	i = i + 1
	
	ch = Chess()
	ch.initChess()
	ch.drawChess()
	
	while True :
		value = getKey()
		# ch.move(value)
			
		cmd = ch.move2cmd(value)
		if not cmd  == None :
			gotoxy(1, 10)
			print(cmd)
			ch.setSel(cmd[0], cmd[1])
			ch.drawChessTableInfo(ch.chessTableInfo())
			
		turn = ch.getTurn()
		gotoxy(1, 11)
		if turn == None :
			print('無')
		elif turn :
			print('黑')
		elif not turn :
			print('紅')
		if not ch.isWin()  == None :
			gotoxy(1, 12)
			print(ch.isWin())
			
		pass
	