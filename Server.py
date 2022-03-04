#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<IP> <port>]
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import logging

import random
import board
import neopixel
import time

import sys
import signal
import subprocess


# animProcess = subprocess.Popen([
#                 "python3", 
#                 "./animations/NONE.py", 
#                 "127.0.0.1",
#                 "300"
#                 ], stdout=subprocess.PIPE)


####################################
LED_COUNT         = 60           # Number of LED pixels.
LED_PIN           = board.D18     # GPIO pin
LED_ORDER         = neopixel.GRBW #GRB  # order of LED colours. May also be RGB, GRBW, or RGBW
LED_BRIGHTNESS    = 1.0           # max brightenss of the led strip
LEFT_ALCOVE_LEN   = 20           # length of left alcove LED strip
CENTER_ALCOVE_LEN = 20           # length of center alcove LED strip
RIGHT_ALCOVE_LEN  = 20           # length of right alcove LED strip

# print(type(LED_ORDER))
# print(LED_ORDER)

pixels  = neopixel.NeoPixel( LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False, pixel_order=LED_ORDER)

# /animProcess = subprocess.Popen([ "python3", "./animations/NONE.py" ], stdout=subprocess.PIPE)
animProcess = subprocess.Popen(["pwd"])

base64UrlTable = (
    'A','B','C','D','E','F','G','H','I','J','K','L','M',
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z',
    '0','1','2','3','4','5','6','7','8','9','-','_' )


####################################
# For debugining, sets LED Strip to a random color
def rndColor():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


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
# Helper function for encoding base64 color data
def encodeColor(color):
    c = int(color[0]) << 16 | int(color[1]) << 8 | int(color[2]);
    return base64UrlTable[(c >> 18) & 63] + base64UrlTable[(c >> 12) & 63] + base64UrlTable[(c >> 6) & 63] + base64UrlTable[c & 63]


####################################
# Function for retriving data from GET response
def getValue(variables, key, default = 0):
    for x in variables:
        parts = x.split('=')
        if parts[0] == key:
            return parts[1]
    return default

####################################
# Function for retriving data from GET response
def endAnimation():
    global animProcess
    if animProcess.poll() is None:
        # print("Old animation is running, killing process before starting new!")
        animProcess.kill()


####################################
class LedAlcove:
    def __init__(self, startIndex, endIndex):
        self._startIndex = startIndex
        self._endIndex = endIndex
        self._color = [0, 0, 0, 0]


    def setColor(self, c):
        self._color = c
        for i in range(self._startIndex, self._endIndex):
            pixels[i] = self._color;

    def getColor(self):
        return self._color


####################################
class LedStrip:
    def __init__(self, left_alcove_len, center_alcove_len, right_alcove_len):
        pixels.fill((0, 0, 0, 0))
        pixels.show()

        self._left_alcove   = LedAlcove(0, left_alcove_len)
        self._center_alcove = LedAlcove(left_alcove_len, left_alcove_len + center_alcove_len)
        self._right_alcove  = LedAlcove(left_alcove_len + center_alcove_len, left_alcove_len + center_alcove_len + right_alcove_len)

    def setColor(self, c):
        endAnimation()
        self._left_alcove.setColor(c)
        self._center_alcove.setColor(c)
        self._right_alcove.setColor(c)
        pixels.show()

    def setLeft(self, c):
        endAnimation()
        self._left_alcove.setColor(c)
        pixels.show()

    def setCenter(self, c):
        endAnimation()
        self._center_alcove.setColor(c)
        pixels.show()

    def setRight(self, c):
        endAnimation()
        self._right_alcove.setColor(c)
        pixels.show()

    def getColor(self):
        return "{\"left_alcove\":" + str(pixels[0]) + ",\"right_alcove\":" + str(pixels[left_alcove_len+center_alcove_len]) + "}" 

    def getRawData(self):
        ret = ""
        for i in range( LED_COUNT ):
            ret += encodeColor(pixels[i])
        return ret

    def getDivPixelData(self):
        ret = ""
        for i in range(LED_COUNT):
            ret += "<div class=\"px\", style=\"background-color: "
            ret += str('#%02x%02x%02x' % (pixels[i][0], pixels[i][1], pixels[i][2]) )
            ret += "\"/>"
            ret += str(i)
            ret += "</div>"
        return ret

    def getColorArrayStr(self):
        return str(pixels)


strip = LedStrip(LEFT_ALCOVE_LEN, CENTER_ALCOVE_LEN, RIGHT_ALCOVE_LEN)

####################################
class S(BaseHTTPRequestHandler):
    def handleQuery(self, bits):
        path = bits.path
        query = bits.query.replace(' ', '')
        query = query.replace('&amp;', '&')
        variables = query.split('&')
        #logging.info("Path: %s, variables: %s", path, variables)

        if path == '/setColor':
            endAnimation()

            _r = int(getValue(variables, 'r', 0))
            _g = int(getValue(variables, 'g', 0))
            _b = int(getValue(variables, 'b', 0))
            _w = int(getValue(variables, 'w', 0))

            strip.setColor([_r, _g, _b, _w])
            #logging.info("LED Strip set to: " + str([_r, _g, _b]))

            self._set_response()
            self.wfile.write("Success!".encode('utf-8'))

        elif path == '/setLeft':
            _r = int(getValue(variables, 'r', 0))
            _g = int(getValue(variables, 'g', 0))
            _b = int(getValue(variables, 'b', 0))
            _w = int(getValue(variables, 'w', 0))

            strip.setLeft([_r, _g, _b, _w])
            #logging.info("Left alcove set to: " + str([_r, _g, _b]))

            self._set_response()
            self.wfile.write("Success!".encode('utf-8'))

        elif path == '/setCenter':
            _r = int(getValue(variables, 'r', 0))
            _g = int(getValue(variables, 'g', 0))
            _b = int(getValue(variables, 'b', 0))
            _w = int(getValue(variables, 'w', 0))

            strip.setCenter([_r, _g, _b, _w])
            #logging.info("Left alcove set to: " + str([_r, _g, _b]))

            self._set_response()
            self.wfile.write("Success!".encode('utf-8'))

        elif path == '/setRight':
            _r = int(getValue(variables, 'r', 0))
            _g = int(getValue(variables, 'g', 0))
            _b = int(getValue(variables, 'b', 0))
            _w = int(getValue(variables, 'w', 0))

            strip.setRight([_r, _g, _b, _w])
            #logging.info("Right alcove set to: " + str([_r, _g, _b]))

            self._set_response()
            self.wfile.write("Success!".encode('utf-8'))

        elif path == '/setLedColor':
            _id = int(getValue(variables, 'id', 0))
            _r =  int(getValue(variables, 'r', 0))
            _g =  int(getValue(variables, 'g', 0))
            _b =  int(getValue(variables, 'b', 0))
            _w =  int(getValue(variables, 'w', 0))

            pixels[_id] = [_r, _g, _b, _w]
            pixels.show()
            #logging.info("Pixel id: " + str(_id) + " set to: " + str([_r, _g, _b]))

            self._set_response()
            self.wfile.write("Success!".encode('utf-8'))

        elif path == '/setRaw':
            _data = getValue(variables, 'data', "AAAA")

            for i in range( LED_COUNT ):
                if int(len(_data)/4) > i:
                    d = _data[ (i*4) : (i*4)+4 ]
                    pixels[i] = decodeColor(d)
            pixels.show()
            #logging.info("Raw data set, length of data: " + str(len(_data)))

            self._set_response()
            self.wfile.write("Success!".encode('utf-8'))

        elif path == '/playAnim':
            anim = getValue(variables, 'anim', 'NONE')
            # params = getValue(variables, 'params', 'null')

            global animProcess
            if animProcess.poll() is None:
                print("Old animation is running, killing process before starting new!")
                animProcess.kill()

            animProcess = subprocess.Popen([
                "python3",
                "./animations/"+anim+".py"
                ], stdout=subprocess.PIPE)

            #logging.info("Left alcove set to: " + str([_r, _g, _b]))

            self._set_response()
            self.wfile.write("Success!".encode('utf-8'))

        elif path == '/getLedCount':
            self._set_response()
            self.wfile.write("{}".format( LED_COUNT ).encode('utf-8'))

        elif path == '/getLedColor':
            _id = int(getValue(variables, 'id', 0))
            self._set_response()
            self.wfile.write("{}".format( pixels[_id] ).encode('utf-8'))

        elif path == '/getColor':
            self._set_response()
            self.wfile.write("{}".format( strip.getColor() ).encode('utf-8'))

        elif path == '/getRaw':
            self._set_response()
            self.wfile.write("{}".format( strip.getRawData() ).encode('utf-8'))

        elif path == '/getConfig':
            _data = "LED_COUNT = " + str(LED_COUNT)
            _data += "\nLEFT_ALCOVE_LEN = " + str(LEFT_ALCOVE_LEN)
            _data += "\nCENTER_ALCOVE_LEN = " + str(CENTER_ALCOVE_LEN)
            _data += "\nRIGHT_ALCOVE_LEN = " + str(RIGHT_ALCOVE_LEN)
            _data += "\nLED_ORDER = \"" + str(LED_ORDER) + "\""
            _data += "\nLED_BRIGHTNESS = " + str(LED_BRIGHTNESS)
            self._set_response()
            self.wfile.write("{}".format( _data ).encode('utf-8'))

        elif path == '/test':
            try:
                _data = "-"
                with open('tests/test.html', 'r') as file:
                    _data = file.read()
                _data = _data.replace("$colorArray", str(pixels))
                _data = _data.replace("$rawData", strip.getRawData())
                _data = _data.replace("$divPixelData", strip.getDivPixelData())

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(_data.encode('utf-8'))
            except:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("Error 404, Page not found! :C".encode('utf-8'))

        elif path == '/help':
            try:
                _data = "-"
                with open('html/help.html', 'r') as file:
                    _data = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(_data.encode('utf-8'))
            except:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("Error 404, Page not found!".encode('utf-8'))

        elif path == '/':
            try:
                _data = "-"
                with open('html/index.html', 'r') as file:
                    _data = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(_data.encode('utf-8'))
            except:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("Error 404, Page not found!".encode('utf-8'))
            #self._set_response()
            #self.wfile.write("LED Strip Controller (Python)\n\ncreated by: Pawel Toborek 19/07/2021\nlast edit: 03/09/2021\nversion: v0.2".encode('utf-8'))

        else:
            try:
                _data = "-"
                with open('html/404.html', 'r') as file:
                    _data = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(_data.encode('utf-8'))
            except:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("Error 404, Page not found!".encode('utf-8'))

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        self.handleQuery( urlparse(self.path) )
    def log_message(self, format, *args):
        return
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


####################################
def run(server_class=HTTPServer, handler_class=S, port=80):
    logging.basicConfig(level=logging.WARNING)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
