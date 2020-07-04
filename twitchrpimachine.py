import sys
import time
import serial
from urllib2 import urlopen


# you will need to go into /dev and find the relay card's serial port
relayCardSerial = '/dev/ttyACM0'

#Open port for communication    
serPort = serial.Serial(relayCardSerial, 19200, timeout=1)

serPort.write("gpio readall\n\r")


def relayWrite(_relay, _mode):
    if (int(_relay) < 10):
        relayIndex = str(_relay)
    else:
        relayIndex = chr(55 + int(_relay))
    
    outgoing = "relay "+ str(_mode) +" "+ relayIndex 
    serPort.write(outgoing + "\n\r")
    if _relay == 6:
        print outgoing




def printDigit(_numeral, _offset):
    sevenSegment = {
        "0": (1, 1, 1, 1, 1, 1, 0),
        "1": (0, 1, 1, 0, 0, 0, 0),
        "2": (1, 1, 0, 1, 1, 0, 1),
        "3": (1, 1, 1, 1, 0, 0, 1),
        "4": (0, 1, 1, 0, 0, 1, 1),
        "5": (1, 0, 1, 1, 0, 1, 1),
        "6": (1, 0, 1, 1, 1, 1, 1),
        "7": (1, 1, 1, 0, 0, 0, 0),
        "8": (1, 1, 1, 1, 1, 1, 1),
        "9": (1, 1, 1, 1, 0, 1, 1),
        " ": (0, 0, 0, 0, 0, 0, 0)
    }

    for segment in range(0, 7):
        relayWrite(segment + _offset, "off" if sevenSegment[str(_numeral)][segment] else "on")


def printNumber(_number):
    number_string = str(_number).rjust(3)  # rjust is to pad the string with spaces

    for i in range(0, 3):
        printDigit(number_string[i], i * 7)

    

try:
    # while True:
    #     for number in range(0, 1000):
    #         printNumber(number)
    #         time.sleep(0.5)
    for iterations in range(0, 6):
        
        root = ET.fromstring(page.read())
        printNumber(root[0][0].text)
        time.sleep(10)

except KeyboardInterrupt:
    pass
finally:
    #Close the port
    serPort.close()

