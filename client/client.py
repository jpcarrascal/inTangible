import websocket
import _thread
import rel
import serial
from picamera import PiCamera
from time import sleep
import json
import requests
import neopixel_functions
import sys

serverURL = "JP-3.local:8080"
camera = PiCamera()
camera.resolution = (2592, 1944)

# Serial init:
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.setDTR(False)
ser.reset_input_buffer()
ser.flushInput()
ser.setDTR(True)
sleep(5)
#
rel.safe_read()

def on_message(ws, message):
    print(message)
    params = json.loads(message)
    if "x" in params and "y" in params and "id" in params:
        x =  str(params["x"]).zfill(2)
        y =  str(params["y"]).zfill(2)
        id = params["id"]
        filename = '/tmp/'+id+".jpg"
        sercommand = x + ":" + y + "\n"
        ser.write(bytes(sercommand, 'UTF-8'))
        while 1:
            tdata = ser.read()           # Wait forever for anything
            sleep(1)              # Sleep (or inWaiting() doesn't give the correct value)
            data_left = ser.in_waiting  # Get the number of characters ready to be read
            tdata += ser.read(data_left) # Do the read and combine it with the first character
            message = tdata.decode('utf-8')
            print(message)
            if message.find("done") != -1:
                print(message)
                break
        neopixel_functions.pixels_on()
        camera.start_preview()
        sleep(5)
        camera.capture(filename)
        camera.stop_preview()
        neopixel_functions.pixels_off()
        with open(filename, 'rb') as f:
            r = requests.post("http://"+serverURL+'/upload-image', files={"image": f}, timeout=5)
        print(r)
        print("Done uploading image.")
    else:
        print("Error in incoming message.")

def on_error(ws, error):
    print(error)
    sys.exit()

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://" + serverURL + "?id=pi",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()