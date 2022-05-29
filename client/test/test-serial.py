import serial
import time
import sys

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.setDTR(False)
#ser.reset_input_buffer()
ser.flushInput()
ser.setDTR(True)
time.sleep(5)
if len(sys.argv) > 1:
    command = bytes(sys.argv[1] + "\n")
    ser.write(command,'UTF-8')
else:
    ser.write(b"01:01\n")
with ser:
    while True:
        print(ser.readline())