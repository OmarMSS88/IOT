import RPi.GPIO as GPIO
import time
import datetime
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)
GPIO.setup(21, GPIO.IN)
feedtime = datetime.datetime(2022, 5, 13, 15, 14, 0)
now = datetime.datetime.now()
while True:
    if (GPIO.input(20) == 0):
        print("now spinning")
        exec(open("stepper.py").read())
    elif (GPIO.input(21) == 0):
        exec(open("LCD.py").read())
        exec(open("echo.py").read())
    elif (now.strftime('%H:%M') == feedtime.strftime('%H:%M')):
        if fed == False:
            print("now spinning")
            exec(open("stepper.py").read())
            fed = True
    else:
        fed = False;
        time.sleep(0.3)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.IN)
    GPIO.setup(21, GPIO.IN)
    now = datetime.datetime.now()
