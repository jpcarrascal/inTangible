import websocket
import _thread
import rel
import serial
from picamera import PiCamera
from time import sleep
import json
import requests

serverURL = "JP-3.local:8080"
camera = PiCamera()

# Serial init:
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.setDTR(False)
#ser.reset_input_buffer()
ser.flushInput()
ser.setDTR(True)
sleep(5)
#
rel.safe_read()

def on_message(ws, message):
    print(message)
    params = json.loads(message)
    if "x" in params and "y" in params and "id" in params:
        x =  params["x"]
        y =  params["y"]
        id = params["id"]
        filename = '/tmp/'+id+".jpg"
        if x >= 1 and x <= 3:
            sercom = "x:" + str(x) + "\n"
            ser.write(bytes(sercom, 'UTF-8'))
        if y >= 1 and y <= 5:
            sercom = "y:" + str(y) + "\n"
            ser.write(bytes(sercom, 'UTF-8'))
        camera.start_preview()
        sleep(5)
        camera.capture(filename)
        camera.stop_preview()
        with open(filename, 'rb') as f:
            r = requests.post("http://"+serverURL+'/upload-image', files={filename: f})
    else:
        print("Error in incoming message")

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://" + serverURL + "?id=jp",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()