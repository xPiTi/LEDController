from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import logging

import random
import board
import neopixel
import time

LED_COUNT        = 10            # Number of LED pixels.
LED_PIN          = board.D18     # GPIO pin
LED_ORDER        = neopixel.GRBW # order of LED colours. May also be RGB, GRBW, or RGBW
LED_BRIGHTNESS   = 0.5           # max brightenss of the led strip
LEFT_ALCOVE_LEN  = 5             # length of the left alcove LED strip
RIGHT_ALCOVE_LEN = 5             # length of the right alcove LED strip

pixels  = neopixel.NeoPixel( LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False, pixel_order=LED_ORDER)

# For debugining, sets LED Strip to a random color
#def rndColor():
#	color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#	print("Random Color:", color)
#	pixels.extend()
#	pixels.fill(color[2:])
#	pixels.show()

def rndColor():
	return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 0)

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
		

####################################
class LedStrip:
	def __init__(self, left_alcove_len, right_alcove_len):
		pixels.fill((0, 0, 0, 1))
		pixels.show()

		self._left_alcove =  LedAlcove(0, left_alcove_len)
		self._right_alcove = LedAlcove(left_alcove_len, left_alcove_len+right_alcove_len)

	def setColor(self, c):
		pixels.fill(c)
		pixels.show()

	def setLeft(self, c):
		self._left_alcove.setColor(c)
		pixels.show()

	def setRight(self, c):	
		self._right_alcove.setColor(c)
		pixels.show()


####################################
def main():
	strip = LedStrip(LEFT_ALCOVE_LEN, RIGHT_ALCOVE_LEN)

	strip.setLeft( rndColor())
	strip.setRight(rndColor())

####################################
main()