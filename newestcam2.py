import urllib.request
import cv2
import numpy as np
from picamera import PiCamera
from time import sleep
from gpiozero import Button
from signal import pause
import time
import urllib.request
import RPi.GPIO as GPIO
import requests
import subprocess


#url = "http://10.112.55.8:8080/shot.jpg"
button_pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def capture_image():
    # IP webcam URL
    #url = 'http://10.149.144.165:8080/shot.jpg'  # Replace with the IP address and port of your IP webcam
    url = 'http://192.168.191.4:8080/shot.jpg'  # Replace with the IP address and port of your IP webcam
    # Send a GET request to the IP webcam URL
    response = requests.get(url)
    # Convert the response content to a NumPy array
    image_array = np.array(bytearray(response.content), dtype=np.uint8)
    # Decode the image array
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    # Save the captured image
    cv2.imwrite('/images/text.jpg', image)
    # Display a message
    print("Image saved successfully.")



def button_press(channel):
    if GPIO.input(button_pin) == GPIO.LOW:
        #print("Button pressed")
        capture_image()
        print("Reading")
        subprocess.call(["python", "text_from_image.py"])
        

GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_press, bouncetime=300)

try:
    while True:
        pass
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    
    
