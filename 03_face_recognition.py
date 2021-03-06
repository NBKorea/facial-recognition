import serial
import time
from datetime import datetime

import cv2
import numpy as np
import os



recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./trainer/trainer.yml")
cascadePath = "./haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> loze: id=1,  etc
names = ['None', 'pikay', 'TK', 'The_other']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

ser = serial.Serial('/dev/ttyACM0', 9600) #USB0', 9600)

while True:
    ret, img =cam.read()
    access = False
    #c = '0'
    #c = c.encode('utf-8')
    #ser.write(c)
    img = cv2.flip(img, -1) # Flip vertically
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        userDefine = False

	# Check if confidence is less them 100 ==> "0" is perfect match
	if (confidence < 40):
	    id = names[id]
	    confidence = "  {0}%".format(round(100 - confidence))
	    userDefine = True
	    if (id != "The_other" and 77 <= float(confidence.replace('%', ''))):
		access = True
        	c = '1'
        	c = c.encode('utf-8')
        	ser.write(c)
        	print("\n [INFO] Access accepted. Welcome, " + id + "! \n [Access] " + str(access) + " \n [confidence]" + str(confidence))
		time.sleep(2)

	    else :
		access = False
                c = '0'
                c = c.encode('utf-8')
                ser.write(c)
                print("\n [INFO] Access denied, " + id + "! \n [Access] " + str(access) + " \n [confidence]" + str(confidence))

        else :
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
	    userDefine = False
	    access = False
            c = '0'
            c = c.encode('utf-8')
            ser.write(c)
            print("\n [INFO] Access denied, " + id + "! \n [Access] " + str(access) + " \n [confidence]" + str(confidence))

        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)

    cv2.imshow('camera',img)
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()

