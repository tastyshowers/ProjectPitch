import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, GPIO.HIGH)
time.sleep(20)
GPIO.cleanup()
