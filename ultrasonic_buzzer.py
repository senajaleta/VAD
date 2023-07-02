import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Ultrasonic Sensor Pins
TRIG_PIN = 23
ECHO_PIN = 24

# Buzzer Pin
BUZZER_PIN = 22

# Set up GPIO pins
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def measure_distance():
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

def activate_buzzer(delay):
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

try:
    while True:
        distance = measure_distance()
        print("Distance:", distance, "cm")

        if distance < 10:
            activate_buzzer(0.005)
        if distance < 15:
            activate_buzzer(0.025)
        elif distance < 20:
            activate_buzzer(0.05)
        elif distance < 30:
            activate_buzzer(0.1)
        elif distance < 50:
            activate_buzzer(0.25)
        elif distance < 70:
            activate_buzzer(0.5)
        elif distance < 100:
            activate_buzzer(0.9)
        elif distance < 150:
            activate_buzzer(1.2)
        elif distance < 200:
            activate_buzzer(1.4)
            
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)

        time.sleep(0.1)
        
except KeyboardInterrupt:
    GPIO.cleanup()
