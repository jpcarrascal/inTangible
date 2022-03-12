import websocket
import _thread
import time
import rel
import serial

# Serial init:
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.setDTR(False)
#ser.reset_input_buffer()
ser.flushInput()
ser.setDTR(True)
time.sleep(5)
#
rel.safe_read()

def on_message(ws, message):
    arr = message.split(":")
    if len(arr) == 2 and arr[0] in ["x","y","h"]:
        ser.write(bytes(arr[0] + ":" + arr[1] + "\n", 'UTF-8'))
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://JP-3.local:8080?id=jp",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()