import sys
import time
import serial


# you will need to go into /dev and find the relay card's serial port
relayCardSerial = '/dev/ttyACM0'

#Open port for communication    
serPort = serial.Serial(relayCardSerial, 19200, timeout=1)

for i in range(0, 10):
	serPort.write("gpio writeall ffffffff\r")
	time.sleep(0.5)
	serPort.write("gpio writeall 00000000\r")
	time.sleep(0.5)



