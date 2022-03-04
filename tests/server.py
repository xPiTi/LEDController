#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<IP> <port>]
"""
global strip_r
global strip_g
global strip_b
global strip_w

strip_r = 0
strip_g = 0
strip_b = 0
strip_w = 0

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import logging

import random
import board
import neopixel

pixels  = neopixel.NeoPixel( board.D18, 430, brightness=0.5, auto_write=False, pixel_order=neopixel.GRBW )
random.seed(1)

# For debugining, sets LED Strip to a random color
def rndColor():
    pixels.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    pixels.show()

# Function for retriving data from GET response
def getValue(variables, key):
    for x in variables:
        parts = x.split('=')
        if parts[0] == key:
            return int(parts[1])
    return 0


class S(BaseHTTPRequestHandler):
    def handleQuery(self, bits):
        path = bits.path
        query = bits.query.replace(' ', '')
        query = query.replace('&amp;', '&')
        variables = query.split('&')
        logging.info("Path: %s, variables: %s", path, variables)
    
        if path == '/setColor':
            global strip_r
            global strip_g
            global strip_b
            global strip_w

            strip_r = getValue(variables, 'r')
            strip_g = getValue(variables, 'g')
            strip_b = getValue(variables, 'b')
            strip_w = getValue(variables, 'w')

            logging.info("LED Strip set to color: %s", (strip_r, strip_g, strip_b, strip_w))
            pixels.fill((strip_r, strip_g, strip_b, strip_w))
            pixels.show()

            self._set_response()
            self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

        elif path == '/getColor':
            self._set_response()
            self.wfile.write("LED Strip set to color: {}".format((strip_r, strip_g, strip_b, strip_w)).encode('utf-8'))

        elif path == '/':
            self._set_response()
            self.wfile.write("LED Strip Controller (Python)\n\ncreated by: Pawel Toborek 19/07/2021\nlast edit: 20/07/2021\nversion: v0.1".encode('utf-8'))

        else:
            self._set_response()
            self.wfile.write("404".encode('utf-8'))

    def _set_response(self):
        self.send_response(200)
        #self.send_header('Content-type', 'text/html')
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        self.handleQuery( urlparse(self.path) )
        

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=80):
    logging.basicConfig(level=logging.INFO)
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
