import spidev
import time
import os
import sys
import RPi.GPIO as GPIO
# Open SPI bus


spi = spidev.SpiDev() # create spi object
spi.open(0,0)
spi.max_speed_hz = 1000000