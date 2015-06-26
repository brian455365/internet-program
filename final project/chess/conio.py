from __future__ import print_function
import os
import colorama
from colorama import Fore, Back, Style
import msvcrt
import struct

# 請先安裝colorama => pip install -U colorama

__keyBase__ = b''

# constant value
KEY_ARROW = "KEY_ARROW"
KEY_UP = "KEY_UP"
KEY_DOWN = "KEY_DOWN"
KEY_LEFT = "KEY_LEFT"
KEY_RIGHT = "KEY_RIGHT"

FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

Enter = '\r'
BackSpace = '\x08'
NonASCII = '\xff'

ACTIVE = (Fore.WHITE, Style.NORMAL, Back.YELLOW, Style.BRIGHT) # active 
INACTIVE = (Fore.BLACK, Style.NORMAL, Back.WHITE, Style.NORMAL)

def putch(c) :
	if len(c) <= 5 and ord(c) >= 0 and ord(c) <= 255 :
		msvcrt.putch(struct.pack('!B', ord(c)))
		
def putstr(string) :
	for c in string :
		putch(c)

def getch() :
	return msvcrt.getch()
	
def kbhit() :
	return msvcrt.kbhit()
	

def getKey() : # python windows function call
	global __keyBase__
	kbValue = struct.pack('!B', ord(NonASCII))
	if kbhit() :
		kbValue = getch()
	if kbValue == b'\xe0' :
		__keyBase__ = kbValue
		# print('arrow key base')
		return KEY_ARROW
	else :
		if __keyBase__ == b'\xe0' :
			if kbValue == b'H' : # up
				# print('up')
				__keyBase__ = b''
				return KEY_UP
			elif kbValue == b'P' : # down
				# print('down')
				__keyBase__ = b''
				return KEY_DOWN
			elif kbValue == b'K' : # left
				# print('left')
				__keyBase__ = b''
				return KEY_LEFT
			elif kbValue == b'M' : # right
				# print('right')
				__keyBase__ = b''
				return KEY_RIGHT
			else :
				# print(kbValue)
				__keyBase__ = b''
		elif __keyBase__ == b'\x00' :
			pass
		else :
			# print(kbValue, end = '')
			# print(chr(struct.unpack("!B", kbValue)[0]))
			return chr(struct.unpack("!B", kbValue)[0])

def initscr() :
	colorama.init()
			
def setFGColor(color = Fore.WHITE, style = Style.NORMAL) :
	if color in FORES and style in STYLES:
		print("%s%s" % (color, style), end='')
	else :
		print('Error Foreground color')
		
def setBGColor(color = Back.BLACK, style = Style.NORMAL) :
	if color in BACKS and style in STYLES:
		print("%s%s" % (color, style), end='')
	else :
		print('Error Background color')
		
def defaultColor() :
	setFGColor()
	setBGColor()
		
def gotoxy(x, y) :
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	print('\x1b[%d;%dH' % (y, x), end='')
	
def clsscr() :
	os.system("cls")

def box(x, y, width, height) :
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	gotoxy(x, y)
	print(' '*width*2, end = '')
	for i in range(height) :
		gotoxy(x, y + i)
		print('  ', end = '')
		gotoxy(x + width*2 - 1, y + i)
		print('  ', end = '')
	gotoxy(x, y + height)
	print(' '*(width*2 + 1), end = '')
	
def drawText(x, y, string) :
	gotoxy(x, y)
	print(string, end = '')
	
def active(x = 1, y = 1, string = '') :
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	gotoxy(x, y)
	setFGColor(ACTIVE[0], ACTIVE[1])
	setBGColor(ACTIVE[2], ACTIVE[3])
	print(string, end = '')
	defaultColor()
	
def inactive(x = 1, y = 1, string = '') :
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	gotoxy(x, y)
	setFGColor(INACTIVE[0], INACTIVE[1])
	setBGColor(INACTIVE[2], INACTIVE[3])
	print(string, end = '')
	defaultColor()

