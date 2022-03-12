import serial
import time
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.setDTR(False)
#ser.reset_input_buffer()
ser.flushInput()
ser.setDTR(True)
time.sleep(5)
ser.write(b"x:1\n")
with ser:
    while True:
        print(ser.readline())