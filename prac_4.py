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

# function to read ADC data from a channel
def GetData(channel): # channel must be an integer 0-7
    adc = spi.xfer2([1,(8+channel)<<4,0]) # sending 3 bytes
    data = ((adc[1]&3) << 8) + adc[2]
    return data

# function to convert data to voltage level (ALSO function for pot)
# places: number of decimal places needed
def ConvertVolts(data):
    volts = (data * 3.3) / float(1023)
    return volts

# function to convert voltage to temperature
def Temperature (voltage):
    temp = voltage
    temp = ((temp - 0.5)/0.01)
    return temp

# function to convert voltage to %
def Percent (voltage):
    per = (int (voltage/3.1*100))
    return per

# Define sensor channels
channel1 = 0
channel2 = 1
channel3 = 2

# Define delay between readings
delay = .5
timer = 0
minute = 0
hour = 0
arr = []
y = True 
try:
    while 1:
        if(y == True):
   
            sensor_data1 = GetData (channel1)
            pot = round(ConvertVolts(sensor_data1),2)
            sensor_data2 = GetData (channel2)
            sensor_volt2 = round(ConvertVolts(sensor_data2),2)
            sensor_data3 = GetData (channel3)
            sensor_volt3 = ConvertVolts(sensor_data3)
            temp = round(Temperature(sensor_volt3),2)
            light = Percent(sensor_volt2)
            element = (str(time.strftime("%H:%M:%S   ")) + str(hour).zfill(2) +':' +str(minute).zfill(2) +':' + str(int(timer*10)).zfill(2) + "     " + str(pot)+ 'V    ' + str(temp) + 'C     ' + str(light) +'%')
            arr.append(element) 
            print(element)
          
        # Wait before repeating loop
        time.sleep(delay)
        timer = timer + delay
       
        if timer >= 6:
            timer = timer - 6
            minute = minute + 1
        if minute >= 60:
            minute = minute - 60
            hour = hour + 1

except KeyboardInterrupt:
    spi.close()

