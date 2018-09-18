import spidev
import time
import os
import sys
import RPi.GPIO as GPIO
# Open SPI bus


spi = spidev.SpiDev() # create spi object
spi.open(0,0)
spi.max_speed_hz = 1000000

GPIO.setmode(GPIO.BCM)

# switch 1 & switch 2: input pull-up
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def callback1(channel1):
    global timer
    timer = 0
    print ("\n" * 50) 

def callback2(channel2):

    global delay
        
    if (delay >= 2):
        delay = 0.5
    else:
        delay = delay * 2    

def callback3(channel3):
    
    global y
    
    y = not y      
    
    

def callback4(channel4):
    global arr
    print('_______________________________________________')
    print('Time        Timer          Pot    Temp   Light')

    for i in range(5,0,-1):
        if i<len(arr):

            print(arr[len(arr)-i])   
            print('_____________________________________________')


GPIO.add_event_detect(23,GPIO.FALLING,callback=callback1,bouncetime=500)
GPIO.add_event_detect(22,GPIO.FALLING,callback=callback2,bouncetime=500)
GPIO.add_event_detect(27,GPIO.FALLING,callback=callback3,bouncetime=500)
GPIO.add_event_detect(17,GPIO.FALLING,callback=callback4,bouncetime=500)
