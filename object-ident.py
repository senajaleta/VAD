import cv2
import pytesseract
import urllib.request

import pyttsx3
import RPi.GPIO as GPIO
import time

# Buzzer Pin
BUZZER_PIN = 22


#thres = 0.45 # Threshold to detect object

classNames = []
classFile = "/home/rahel/Object_Detection_Files/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/rahel/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/rahel/Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(480,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
engine =pyttsx3.init()


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 23
ECHO = 24

# Set up GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def measure_distance():
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    print("Distance:", distance, "cm")

    return distance

def suggest_direction(frame, boxes, scores, classNames):
    width = frame.shape[1]
    midpoint = width // 2
    for i in range(len(boxes)):
        ymin, xmin, ymax, xmax = boxes[i]
        score = scores[i]
        if score > 0.5:
            box_midpoint = (xmin + xmax) / 2 * width
            if box_midpoint < midpoint:
                print("Object is on the left")
                engine.say("Go Right")
                engine.runAndWait()
                return "Object is on the left"
            else:
                print("Object is on the right")
                engine.say("Go Left")
                engine.runAndWait()
                return "Object is on the right"
def activate_buzzer(delay):
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)
    # print(classIds,bbox)
    if len(objects) == 0:
        objects = classNames
    objectInfo = []
    detected_classes = []

    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box, className])
                detected_classes.append(className)
                if draw:
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(img, classNames[classId-1].upper(), (box[0]+10, box[1]+30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(img, str(round(confidence*100, 2)), (box[0]+200, box[1]+30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # Check for detected classes
    distance = measure_distance()
    if "person" in detected_classes and distance < 500:
        #engine.say("person detected at", distance, "meter")
        #engine.runAndWait()
        print("person and distance")
    #elif "car" in detected_classes and distance < 20000:
    #    engine.say("car detected!")
    #    engine.runAndWait()

    # Call suggest_direction functions
    # suggest_direction(img, bbox, confs, classNames)
    elif distance < 10:
            activate_buzzer(0.05)
    elif distance < 10:
        activate_buzzer(0.1)
    elif distance < 20:
        activate_buzzer(0.3)
    elif distance < 30:
        activate_buzzer(0.5)
    elif distance < 50:
        activate_buzzer(0.7)
    elif distance < 70:
        activate_buzzer(0.9)
    elif distance < 90:
        activate_buzzer(1.2)
    elif distance < 130:
        activate_buzzer(2)
    elif distance < 200:
        activate_buzzer(1)
        
    else:
        GPIO.output(BUZZER_PIN, GPIO.LOW)

    time.sleep(0.1)

    return objectInfo, img

if __name__ == "__main__":
    #url = "http://192.168.137.216:4747/video"
    url = 'http://192.168.137.164:8080/video'
    cap = cv2.VideoCapture(url)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)


    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.45,0.2)
        #print(objectInfo)
        cv2.imshow("Output",img)
        cv2.waitKey(1)
