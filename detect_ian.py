# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import mediapipe as mp
import numpy as np
import imutils
import time
import cv2
import os

from playsound import playsound
from threading import Thread
 
import winsound

def detect_and_predict_mask(frame, faceNet, maskNet_NoMask_Ian):
    # grab the dimensions of the frame and then construct a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
        (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()
    #print(detections.shape)

    # initialize our list of faces, their corresponding locations,
    # and the list of predictions from our face mask network
    faces = []
    locs = []
    preds = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if confidence > 0.5:
            # compute the (x, y)-coordinates of the bounding box for
            # the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # ensure the bounding boxes fall within the dimensions of
            # the frame
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # extract the face ROI, convert it from BGR to RGB channel
            # ordering, resize it to 224x224, and preprocess it
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            # add the face and bounding boxes to their respective
            # lists
            faces.append(face)
            locs.append((startX, startY, endX, endY))

    # only make a predictions if at least one face was detected
    if len(faces) > 0:
        # for faster inference we'll make batch predictions on *all*
        # faces at the same time rather than one-by-one predictions
        # in the above `for` loop
        faces = np.array(faces, dtype="float32")
        preds = maskNet_NoMask_Ian.predict(faces, batch_size=32)

    # return a 2-tuple of the face locations and their corresponding
    # locations
    return (locs, preds)

# load our serialized face detector model from disk
prototxtPath = r"face_detector\deploy.prototxt"
weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
#maskNet_NoMask_Ian = load_model("mask_detector_1.model")

# initialize the video stream
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# load the face mask detector model from disk
maskNet = load_model("mask_detector.model")
maskNet_NoMask_Ian = load_model("nomask_Ian.model")
# loop over the frames from the video stream

mode = ""
modedict = {"No Mask": {"model":maskNet_NoMask_Ian, "redLabel":"Unmasked Person", "greenLabel":"Ian"},
            "Mask": {"model":maskNet, "redLabel":"No Mask", "greenLabel":"Masked Person"},
            }
employees = {"Ian"}
framecount = 0

def detect(dicti):
    model = modedict[dicti]["model"]
    # grab the frame from the threaded video stream andq resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # detect faces in the frame and determine if they are wearing a
    # face mask or not
    (locs, preds) = detect_and_predict_mask(frame, faceNet, model)

    # loop over the detected face locations and their corresponding
    # locations
    
    pTime = 0
    frame, faces = detector.findFaceMesh(frame, draw=True)
    #if len(faces)!= 0:
        #print(faces[0])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (0, 255, 0), 3)
    
    
    for (box, pred) in zip(locs, preds):
        # unpack the bounding box and predictions
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred
        # determine the class label and color we'll use to draw
        # the bounding box and text
        label = modedict[dicti]["greenLabel"] if mask > withoutMask else modedict[dicti]["redLabel"]
        if modedict[dicti].__contains__("customcolor"):
            color = modedict[dicti]["customcolor"] if label == modedict[dicti]["greenLabel"] else (0, 0, 255)
        else:
            color = (0, 255, 0) if label == modedict[dicti]["greenLabel"] else (0, 0, 255)
        mode = label
        
        #print(pred)
        print(mode)
        
        if employees.__contains__(mode):
            print("Found Employee!")
            color = (0,255,255)
            label = "{}: {:.2f}%".format(mode, max(mask, withoutMask) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            #cv2.imwrite('dataset\ian_without_mask\Frame'+str(i)+'.jpg', frame)
            
            cv2.putText(frame, label, (startX, startY - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

            # show the output frame
            cv2.imshow("Frame", frame)
        else:
            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            #cv2.imwrite('dataset\ian_without_mask\Frame'+str(i)+'.jpg', frame)
            
            cv2.putText(frame, label, (startX, startY - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

            # show the output frame
            cv2.imshow("Frame", frame)

        if mode == "No Mask":
            #playsound("beep-02.mp3")
            if framecount%10 == 0 :
                winsound.PlaySound(r"beep-02.wav", winsound.SND_ASYNC)
            # include the probability in the label
            label = "Unmasked Person"
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
            #playsound('beep-02.mp3', block = False)
            # display the label and bounding box rectangle on the output
            # frame
            #cv2.imwrite('dataset\ian_without_mask\Frame'+str(i)+'.jpg', frame)
            
            cv2.putText(frame, label, (startX, startY - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

            # show the output frame
            cv2.imshow("Frame", frame)
            
            detect(mode)
        
class FaceMeshDetector():
    def __init__(self, staticMode=False, maxFaces=2, refine_landmarks=True, minDetectionCon=0.5):
 
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionCon = minDetectionCon
        self.refine_landmarks = refine_landmarks
        #self.minTrackCon = minTrackCon
        
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.staticMode, self.maxFaces,
                                                 self.refine_landmarks, self.minDetectionCon)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=2)
 
    def findFaceMesh(self, img, draw=True):
        #self.flags.writeable = False
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        faces = []
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS,
                                           self.drawSpec, self.drawSpec)
                face = []
                for id,lm in enumerate(faceLms.landmark):
                    #print(lm)
                    ih, iw, ic = img.shape
                    x,y = int(lm.x*iw), int(lm.y*ih)
                    cv2.putText(img, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN,
                               0.5, (0, 255, 0), 1)
 
                    #print(id,x,y)
                    face.append([x,y])
                faces.append(face)
        return img, faces

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
       # draw circle here (etc...)
       print('x = %d, y = %d'%(x, y))



detector = FaceMeshDetector(maxFaces=2)

while True:
    detect("Mask")
    framecount += 1
    if framecount > 10000:
        framecount = 0
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    
    
    if key == ord("q"):
        break
    

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()