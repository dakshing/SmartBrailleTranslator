#Main program to run the Braille Translator
#Serial makes connection to the COM3 port, where the arduino is connected.

import serial
import time
import alphaToBraille
import ocr_improvement
import camera

img_name=camera.capture()
str=ocr_improvement.ocr(img_name)
if str is not None:
    str=alphaToBraille.translate(str)
    ser = serial.Serial('COM3', 9600)
    print(str)
    while 1:
        ser.write(str.encode())
        time.sleep(5)
