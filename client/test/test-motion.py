import serial
import time
import sys

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
#ser.setDTR(False)
###ser.reset_input_buffer()
#ser.flushInput()
#ser.setDTR(True)
time.sleep(2)
if len(sys.argv) > 1:
    command = bytes(sys.argv[1] + "\n",'UTF-8')
    ser.write(command)
else:
    ser.write(b"01:01\n")
with ser:
    #while True:
    print(ser.readline())