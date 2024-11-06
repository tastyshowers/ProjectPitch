
# @description: this file is used to test and pair audio input volume with the brightness of an LED
import sounddevice as sd
import RPi.GPIO as GPIO
import numpy as np
from rpi_ws281x import *
import time

# LED strip configuration:
LED_COUNT      = 30     # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev>
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transisto>
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

#LED strip setup and start
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
#variables for updating strip in timely manner
last_update = time.time()
def clearLights(strip):
	for i in range (0, LED_COUNT):
		strip.setPixelColor(i, Color(0,0,0))
	strip.show()
def showNumLights (strip, color, numLights):
	for i in range (0, numLights):
		strip.setPixelColor(i, color)
	for i in range (numLights, LED_COUNT):
		strip.setPixelColor(i, Color(0,0,0))
	strip.show()
def volumeToNumLights (indata):
	volume_norm = np.linalg.norm(indata)
	volume_norm *= 1000000000000
	numLights = int(np.clip((volume_norm / 10000000000 - 100) * 3, 0, 30))
	return numLights
def audio_process_input(indata, frmes, times, status):
	global last_update
	numLights = volumeToNumLights(indata)
	if time.time() - last_update > 0.0005:
		showNumLights(strip, Color(255,0,0), numLights)
		last_update = time.time()
try:
	with sd.InputStream(callback=audio_process_input, device=2):
		while True:
			time.sleep(1)
except KeyboardInterrupt:
	print("Stopped by user")
finally:
	GPIO.cleanup()