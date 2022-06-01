import board
import neopixel
#------------ Neopixel vars and functions: ------------
pixel_pin = board.D18
num_pixels = 12
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER 
)

def pixels_on(option=-1):
    for i in range(num_pixels):
        pixels[i] = tuple(c[i])
    pixels.show()

def pixels_off():
    pixels.fill((0, 0, 0))
    pixels.show()

#------------ Neopixel functions/ ------------