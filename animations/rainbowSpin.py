import sys
from sys import argv
import requests
import colorsys
import time

ip = "127.0.0.1"
pixels_count = 10
pixels = [0, 0, 0] * pixels_count

####################################
# Base64 lookup table
base64UrlTable = (
    'A','B','C','D','E','F','G','H','I','J','K','L','M',
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z',
    '0','1','2','3','4','5','6','7','8','9','-','_' )

####################################
# Helper function for encoding base64 color data
def encodeColor(color):
    c = int(color[0]) << 16 | int(color[1]) << 8 | int(color[2]);
    return base64UrlTable[(c >> 18) & 63] + base64UrlTable[(c >> 12) & 63] + base64UrlTable[(c >> 6) & 63] + base64UrlTable[c & 63]

####################################
# Helper function for decoding base64 color data
def decodeColor(data):
    v1 = int( base64UrlTable.index(data[0]) )
    v2 = int( base64UrlTable.index(data[1]) )
    v3 = int( base64UrlTable.index(data[2]) )
    v4 = int( base64UrlTable.index(data[3]) )
    c = v1 << 18 | v2 << 12 | v3 << 6 | v4
    return [ ((c >> 16) & 255), ((c >> 8) & 255), (c & 255) ]

####################################
# Helper function for decoding base64 color data
def getRawPixelsColorData():
    ret = ""
    for i in range( pixels_count ):
        ret += encodeColor(pixels[i])
    return ret

####################################
# Helper function to send raw pixel color to API 
def sendPixelsToAPI():
    req = "http://"
    req += ip
    req += "/setRaw?data="
    req += getRawPixelsColorData()
    requests.get(req)


def getLedCount():
    return int(requests.get("http://"+ip+":80/getLedCount").text)


####################################
# Helper function for decoding base64 color data
def rndColor():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def fillColor(color):
    for i in range(pixels_count):
        pixels[i] = c

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

####################################
# MAIN PROGRAM STARTS HERE
if __name__ == '__main__':
    # print("Sending animation to:", argv[1])
    # ip = argv[1]
    # print("LED strip length:", argv[2])
    # pixels_count = int(argv[2])
    pixels_count = getLedCount()
    pixels = [0, 0, 0] * pixels_count
    
    try:
        hueShift = 0
        while(True):
            
            for i in range(pixels_count):
                c = hsv2rgb( (hueShift + (i/300.0)) %1.0, 1.0, 1.0)
                pixels[i] = c
            
            hueShift = hueShift + 0.005
            if hueShift > 1:
                hueShift = 0

            # print("color = ", c)

            # fillColor(c)
            sendPixelsToAPI()
            time.sleep(0.015) # wait 5ms

    except KeyboardInterrupt:
        pass
    
    print("Animation terminated!")

# x = requests.get('https://w3schools.com')
# print(x.status_code)
# test_color = colorsys.hsv_to_rgb(359,100,100)
