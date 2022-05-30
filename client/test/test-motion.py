import serial
import time
import sys

#ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser = serial.Serial()
ser.port = '/dev/ttyUSB0'
ser.baudrate = 115200
ser.timeout = 1
ser.setDTR(False)
time.sleep(2)
ser.open()

#ser.setDTR(False)
###ser.reset_input_buffer()
#ser.flushInput()
#ser.setDTR(True)
time.sleep(2)
if len(sys.argv) > 1:
    command = bytes(sys.argv[1] + "\n",'UTF-8')
    ser.write(command)
else:
    comm = ""
    #ser.write(b"01:01\n")
    with ser:
        while comm != "exit":
            comm = input("Serial command: ")
            if comm != "exit":
                command = bytes(comm + "\n",'UTF-8')
                ser.write(command)
                print(ser.readline())
            else:
                print("Exiting...")