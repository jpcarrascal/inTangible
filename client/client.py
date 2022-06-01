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
import conf

serverURL = conf.serverURL
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
    params = json.loads(message)
    print(params)
    if "command" in params and params.command == "fetch":
        if "x" in params and "y" in params and "c" in params and "tid" in params:
            x =  str(params["x"]).zfill(3)
            y =  str(params["y"]).zfill(3)
            tid = str(params["tid"])
            filename = '/tmp/' + tid + ".jpg"
            sercommand = x + ";" + y + "\n"
            ser.write(bytes(sercommand, 'UTF-8'))
            while 1:
                tdata = ser.read()           # Wait forever for anything
                sleep(2)              # Sleep (or inWaiting() doesn't give the correct value)
                data_left = ser.in_waiting  # Get the number of characters ready to be read
                tdata += ser.read(data_left) # Do the read and combine it with the first character
                message = tdata.decode('utf-8')
                print(message)
                if message.find("done") != -1:
                    print(message)
                    break
                if message.find("Wrong") != -1:
                    print(message)
                    return -1
            if "c" in params:
                c = params["c"]
                neopixel_functions.illum(c)
            else:
                neopixel_functions.rainbow()
            camera.iso = 200
            camera.shutter_speed = 50000
            camera.start_preview()
            sleep(3)
            camera.capture(filename)
            camera.stop_preview()
            neopixel_functions.pixels_off()
            try:
                with open(filename, 'rb') as f:
                    r = requests.post("http://"+serverURL+'/upload-image', files={"image": f}, timeout=5)
                print(r)
                print("Done uploading image.")
            except:
                print("Error when calling /upload-image.")
        else:
            print("Error in incoming message.")
    else:
        print("Unknown command.")
def on_error(ws, error):
    print(error)
    sys.exit()

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Connection open")

if __name__ == "__main__":
    while True:
        try:
            websocket.enableTrace(True)
            ws = websocket.WebSocketApp("ws://" + serverURL + "?id=pi",
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
            ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
            rel.signal(2, rel.abort)  # Keyboard Interrupt
            rel.dispatch()
        except KeyboardInterrupt:
            print("Exiting...")
            rel.abort()
        except:
            print("Websocket connection Error:")
            rel.abort()
        print("Reconnecting websocket  after 5 sec")
        sleep(5)