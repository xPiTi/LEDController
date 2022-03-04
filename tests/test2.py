base64UrlTable = (
	'A','B','C','D','E','F','G','H','I','J','K','L','M',
	'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
	'a','b','c','d','e','f','g','h','i','j','k','l','m',
	'n','o','p','q','r','s','t','u','v','w','x','y','z',
	'0','1','2','3','4','5','6','7','8','9','-','_' )

def decodeColor(data):
	v1 = int( base64UrlTable.index(data[0]) )
	v2 = int( base64UrlTable.index(data[1]) )
	v3 = int( base64UrlTable.index(data[2]) )
	v4 = int( base64UrlTable.index(data[3]) )
	c = v1 << 18 | v2 << 12 | v3 << 6 | v4
	return [ ((c >> 16) & 255), ((c >> 8) & 255), (c & 255), 0 ]

def encodeColor(color):
	c = int(color[0]) << 16 | int(color[1]) << 8 | int(color[2]);
	return base64UrlTable[(c >> 18) & 63] + base64UrlTable[(c >> 12) & 63] + base64UrlTable[(c >> 6) & 63] + base64UrlTable[c & 63]

# print(decodeColor("1gj_"))
# print(decodeColor("LMXZ"))
# print(encodeColor([255, 0, 90]))
# print(encodeColor(decodeColor("1234")))

# data = "asdasd ahkd hasjkh j113a"
# print("Length of the data string:", int(len(data)))
# print("Length /4 of the data string:", int(len(data)/4))

l = [0, 128, 64]

s = '#%02x%02x%02x' % (l[0], l[1], l[2])

print(s)