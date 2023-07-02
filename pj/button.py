import RPi.GPIO as GPIO
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BUTTON_PIN = 22

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_callback(channel):
    # Execute the desired file or command
    subprocess.call(["python", "/home/rahel/Object_Detection_Files/text_from_image.py"])

# Register the button callback function for the falling edge
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=200)

# Keep the script running
while True:
    pass
