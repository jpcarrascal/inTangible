import websocket
import _thread
import rel
import serial
from picamera import PiCamera
from time import sleep
import json
import requests
import board
import neopixel
import random
# Neopixel vars:
pixel_pin = board.D18
num_pixels = 12
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER 
)
#
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
        sleep(10)
        pixels_on()
        camera.start_preview()
        sleep(5)
        camera.capture(filename)
        camera.stop_preview()
        pixels_off()
        with open(filename, 'rb') as f:
            r = requests.post("http://"+serverURL+'/upload-image', files={"image": f}, headers={'Connection':'close'})
            r.close()
        print("Done uploading image.")
    else:
        print("Error in incoming message.")

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

#------------ Neopixel functions: ------------

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def rainbow():
    for i in range(num_pixels):
        pixel_index = (i * 256 // num_pixels)
        pixels[i] = wheel(pixel_index & 255)
    pixels.show()

def pixels_on():
    option = random.randrange(0, 5)
    option = 9
    if option == 0:
        pixels.fill((255, 0, 0))
        pixels.show()
    elif option == 1:
        pixels.fill((0, 255, 0))
        pixels.show()
    elif option == 2:
        pixels.fill((0, 0, 255))
        pixels.show()
    elif option == 3:
        pixels.fill((55, 55, 55))
        pixels.show()
    elif option == 4:
        rainbow()
    else:
        pixels.fill((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
        pixels.show()

def pixels_off():
    pixels.fill((0, 0, 0))
    pixels.show()

#------------ Neopixel functions/ ------------

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