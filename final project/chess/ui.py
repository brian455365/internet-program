from conio import *

class uiItem :
	def __init__(self, name, x, y) :
		self.__name = name
		self.x = x
		self.y = y
		self.__U = ""
		self.__D = ""
		self.__R = ""
		self.__L = ""
		self.ETR = lambda string : print(string, end = "")
	def setU(self, _u_name) :
		self.__U = _u_name
	def setD(self, _d_name) :
		self.__D = _d_name
	def setR(self, _r_name) :
		self.__R = _r_name
	def setL(self, _l_name) :
		self.__L = _l_name
	def setF(self, _f_func) :
		self.ETR = _f_func
	def name(self) :
		return self.__name
	def U(self) :
		return self.__U
	def D(self) :
		return self.__D
	def L(self) :
		return self.__L
	def R(self) :
		return self.__R
	def F(self) :
		return self.ETR
	def pos(self) :
		return (self.x, self.y)
		
class uiPage :
	def __init__(self, name) :
		self.name = name
		self.O  = dict()
		self.curItem = ""
	def addItem(self, __item) :
		if not __item.name() in list(self.O.keys()) :
			self.O[__item.name()] = __item
			self.curItem = __item.name()
	def delItem(self, itemName) :
		if itemName in list(self.O.keys()) :
			del self.O[itemName]
	def current(self) :
		return (self.name, self.curItem)
	def drawUI(self) :
		itemName = ""
		pos = (0, 0)
		for itemKey in list(self.O.keys()) :
			itemName = self.O[itemKey].name()
			pos = self.O[itemKey].pos()
			inactive(pos[0], pos[1], itemName)
		itemName = self.O[self.curItem].name()
		pos = self.O[self.curItem].pos()
		active(pos[0], pos[1], itemName)
	def move(self, Op) :
		nextItem = ""
		pos = (0, 0)
		if Op == KEY_UP :
			nextItem = self.O[self.curItem].U()
		elif Op == KEY_DOWN :
			nextItem = self.O[self.curItem].D()
		elif Op == KEY_LEFT :
			nextItem = self.O[self.curItem].L()
		elif Op == KEY_RIGHT :
			nextItem = self.O[self.curItem].R()
		elif Op == Enter :
			pos = self.O[self.curItem].pos()
			inactive(pos[0], pos[1], self.curItem)
			active(pos[0], pos[1], self.curItem)
			return self.O[self.curItem].F() # 按 Enter 會將function 回傳
		if not nextItem  == "" :
			pos = self.O[self.curItem].pos()
			inactive(pos[0], pos[1], self.curItem)
			pos = self.O[nextItem].pos()
			active(pos[0], pos[1], nextItem)
			self.curItem = nextItem
		return None
		
if __name__ == "__main__" :
	initscr()
	clsscr()
	
	# chess(10, 5)
	# chessSet(3, 3)
	item0 = uiItem('A', 1, 1)
	item0.setD('B')
	item0.setR('C')
	item1 = uiItem('B', 1, 2)
	item1.setU('A')
	item2 = uiItem('C', 3, 1)
	item2.setL('A')
	
	page0 = uiPage('example')
	page0.addItem(item0)
	page0.addItem(item1)
	page0.addItem(item2)
	
	page0.drawUI()
	
	while True :
		value = getKey()
		f = page0.move(value)
		if not f  == None :
			f('apple')
		pass
	