#!/usr/bin/env python3 
import time
import datetime
import busio
import digitalio
import board
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 23
ECHO = 24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
time.sleep(2)
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)
while GPIO.input(ECHO)==0:
 pulse_start = time.time()
while GPIO.input(ECHO)==1:
 pulse_end = time.time()
pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17165
distance = round(distance, 1)

#variabele feedingtime
feedtime = datetime.datetime(2022, 5, 17, 15, 30, 0)
now = datetime.datetime.now().strftime("%H:%M:%S")

# Initialize SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize display
dc = digitalio.DigitalInOut(board.D26)  # data/command
cs1 = digitalio.DigitalInOut(board.CE1)  # chip select CE1 for display
reset = digitalio.DigitalInOut(board.D13)  # reset
display = adafruit_pcd8544.PCD8544(spi, dc, cs1, reset, baudrate= 1000000)
display.bias = 4
display.contrast = 60
display.invert = True

#  Clear the display.  Always call show after changing pixels to make the display update visible!
display.fill(0)
display.show()

# Load default font.
font = ImageFont.load_default()
#font=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 10)

# Get drawing object to draw on image
image = Image.new('1', (display.width, display.height)) 
draw = ImageDraw.Draw(image)
 	
# Draw a white filled box to clear the image.
draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)

# Write some text.
draw.text((1,0), (str(now)) , font=font)
draw.text((1,8), 'afstand ', font=font)
draw.text((1,16), str(distance) + 'cm' , font=font)
draw.text((1,24), 'Volgende voed tijd:', font=font)
draw.text((1,32), feedtime.strftime("%X"), font=font)
display.image(image)
display.show()
