# Import packages
from scipy.spatial import distance as dist
import numpy as np
import dlib
import cv2
import requests
import os, sys

from pygame import mixer

image = cv2.imread('aLERT.png') # Load input (coffee break) image
image = cv2.resize(image, (100,100)) # Resize image to 100x100

def alert():
     pass
     #mixer.init()
     #mixer.music.load('aLERT.mp3')
     #mixer.music.play()
     

def sms_fun():
    number1 = mobile1
    number2 = mobile2

    url = "https://www.fast2sms.com/dev/bulkV2" 
    payload = "sender_id=TXTIND&message= Driver Sleepy &route=v3&numbers={},{}".format(number1,number2)
    headers = {
    'authorization': "suhveRXO69iT2cDlAxZ0GrjYHLz1opQ4FPamBgMNbn85It7kwWh16l2UVWc3RozmAvQEGHSLg9tCeFq0",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print("Emergency Alert sent")
    print(response.text)
    sys.exit()
'''
Eye Aspect Ratio (E.A.R.)
Function to calculate eye aspect ratio as in paper :
"Real-Time Eye Blink Detection using Facial Landmarks [Soukupova, Cech]"             
Landmarks |   0  1  2  3  4  5
 Left Eye : [36,37,38,39,40,41]
Right Eye : [42,43,44,45,46,47]
'''
def eye_aspect_ratio(eye):
     # Vertical distances
     dist1 = dist.euclidean(eye[1], eye[5]) # P2-P6
     dist2 = dist.euclidean(eye[2], eye[4]) # P3-P5
     # Horiontal distance
     dist3 = dist.euclidean(eye[0], eye[3]) # P1-P4

     # Eye Aspect Ratio (E.A.R.)
     ear = (dist1 + dist2) / (2.0 * dist3)

     return ear



'''
Lips Aspect Ratio (L.A.R.)
Function to calculate lips aspect ratio in the same way as in E.A.R.
Landmarks |   0  1  2  3  4  5  6  7
     Lips : [60,61,62,63,64,65,66,67]
'''
def lips_aspect_ratio(lips):
     # Vertical distance
     dist1 = dist.euclidean(lips[2], lips[6]) # L3-L7
     # Horiontal distance
     dist2 = dist.euclidean(lips[0], lips[4]) # L1-L5

     # Lips Aspect Ratio (L.A.R.)
     lar = float(dist1/dist2)

     return lar


'''
Facial Landmarks for any face part
Function to calculate facial landmark point coordinates (x,y),
draw them on frame and return a numpy array with the corresponding points
'''
def draw_landmarks(face_part, landmarks):
     landmarks_list = []
     for point in face_part:
          x, y = landmarks.part(point).x, landmarks.part(point).y
          landmarks_list.append([x,y])
          cv2.circle(frame, (x,y), 2, (0,0,255), -1)
          
     return np.array(landmarks_list)


# DLIB - Face Detector
detector = dlib.get_frontal_face_detector()
# DLIB - Predictor
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


# Video Capture
cap = cv2.VideoCapture(0)
#path = 'video num 1.mp4'
#cap = cv2.VideoCapture(path)
# Text settings
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.6

# Initializations
frames = 0

# ear & lar, threshold values
ear_thresh = 0.3
lar_thresh = 0.3

# Blink initializations
blink_counter, total_blinks = 0, 0
# Yawn initializations
yawn_counter, total_yawns = 0, 0

mobile1 = int(input("Enter that mobile number u need to send alert Message\n---->>")) 
mobile2 = int(input("Enter that mobile number u need to send alert Message\n-----$$"))
while True:
     _, frame = cap.read()
     frame = cv2.flip(frame, 1) # May not be necessary
     h, w = frame.shape[:2]    # Height and Width of frame
     
     frames += 1

     # Grayscale
     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

     # Detect faces in the gray frame
     faces = detector(gray, 0)

     # Loop through each face
     for face in faces:
          # Determine facial landmarks
          facial_landmarks = predictor(gray, face)

          # Landmark indexes for eyes and lips
          left_eye = [36,37,38,39,40,41]
          right_eye = [42,43,44,45,46,47]
          
          lips = [60,61,62,63,64,65,66,67]

          # Convert to numpy array the above lists and
          # draw the corresponding facial landmark points on frame
          left_eye_points = draw_landmarks(left_eye, facial_landmarks)
          right_eye_points = draw_landmarks(right_eye, facial_landmarks)

          lips_points = draw_landmarks(lips, facial_landmarks)

          # Find and draw the convex hulls of left and right eye, and lips
          left_eye_hull = cv2.convexHull(left_eye_points)      
          cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
          
          right_eye_hull = cv2.convexHull(right_eye_points)
          cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)

          lips_hull = cv2.convexHull(lips_points)
          cv2.drawContours(frame, [lips_hull], -1, (0, 255, 0), 1)

          # Calculate E.A.R. and L.A.R.
          left_ear = eye_aspect_ratio(left_eye_points)    # Left eye aspect ratio
          right_ear =  eye_aspect_ratio(right_eye_points) # Right eye aspect ratio
          ear = (left_ear + right_ear) / 2.0              # Average eye aspect ratio
          cv2.putText(frame, "E.A.R. : {:.2f}".format(ear), (10,30), font, font_scale, (0,0,255), 2)

          lar = lips_aspect_ratio(lips_points) # Lips aspect ratio
          cv2.putText(frame, "L.A.R. : {:.2f}".format(lar), (10,90), font, font_scale, (0,0,255), 2)

          # Check for blinks or yawns
          # BLINK
          if ear < ear_thresh:
               blink_counter += 1
          else:
               if blink_counter > 3:
                    total_blinks += 1
               blink_counter = 0
          cv2.putText(frame, "Blinks: {}".format(total_blinks), (10, 50), font, font_scale, (0, 0, 255), 2)

          # YAWN
          if lar > lar_thresh:
               yawn_counter += 1
          else:
               if yawn_counter > 1:
                    total_yawns += 1
               yawn_counter = 0
          cv2.putText(frame, "Yawns: {}".format(total_yawns), (10, 110), font, font_scale, (0, 0, 255), 2)
          
          # Drowsiness Detection
          if total_yawns > 2 and total_yawns <4  or total_blinks > 3 and total_blinks <7:
               frame[20:120, w-120:w-20] = image 
               cv2.putText(frame, "ALERT", (w-120, 160), font, 1.2, (0, 0, 255), 4)
          elif total_yawns > 4 and total_yawns <7  or total_blinks > 7 and total_blinks <10:
               alert()
          elif total_yawns > 7 or total_blinks <10:
               #sms_fun()
               pass



     cv2.imshow('Frame', frame)
     key = cv2.waitKey(1)
     if key == 27:
          break
     if key==ord('r') or key==ord('R'):
          total_blinks, total_yawns = 0, 0 # Reset calculations by pressing 'r' or 'R'

cap.release()
cv2.destroyAllWindows()