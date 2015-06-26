import struct

def str2b(str) :
	f = '!' + ''.join(['B' for i in range(len(str))])
	S = [ord(C) for C in str]
	return struct.pack(f, *S)
	
def b2str(bin) :
	f = '!' + ''.join(['B' for i in range(len(bin))])
	S = struct.unpack(f, bin)
	str = [chr(B) for B in S]
	return ''.join(str)
	
def str2D(str) :
	D = dict()
	seg = str.split("&")
	for s in seg :
		s = s.split("=")
		D[s[0]] = s[1]
	return D
	
def b2D(bin) :
	return str2D(b2str(bin))