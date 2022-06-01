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

def three(c):
    for i in range(num_pixels // 3):
        pixels[i] = (c[0], c[1], c[2])
    for i in range(num_pixels // 3, (num_pixels // 3)*2-1):
        pixels[i] = (c[3], c[4], c[5])
    for i in range((num_pixels // 3)*2, num_pixels):
        pixels[i] = (c[6], c[7], c[8])
    pixels.show()

def illum(c):
    for i in range(num_pixels):
        pixels[i] = tuple(c[i])
    pixels.show()

def pixels_on(option=-1):
    three()
    '''
    if option < 0 or option > 4:
        option = random.randrange(0, 4)
    if option == 0:
        pixels.fill((255, 0, 0))
    elif option == 1:
        pixels.fill((0, 255, 0))
    elif option == 2:
        pixels.fill((0, 0, 255))
    elif option == 3:
        pixels.fill((55, 55, 55))
    elif option == 4:
        rainbow()
    else:
        pixels.fill((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
    pixels.show()
    '''

def pixels_off():
    pixels.fill((0, 0, 0))
    pixels.show()

#------------ Neopixel functions/ ------------