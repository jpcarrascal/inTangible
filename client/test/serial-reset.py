import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.setDTR(False)
time.sleep(2)
ser.reset_input_buffer()
ser.flushInput()
#ser.setDTR(True)
ser.setDTR(False)
time.sleep(2)