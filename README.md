Real Time Drowsiness Detection
This Real Time Drowsiness Detection System in Python(3.6) will allow you to prevent road accidents, works with just your regular webcam. Its hands-free, no wearable hardware or sensors needed.
At this point, you are forced to work with the facial movements I chose but I am working on making them configurable. The list of actions include:
Blinking your eyes  - To look with the eyes partially closed or opened
Yawning detection in mouth

Code Requirements

Numpy - 1.13.3
OpenCV - 3.2.0
Playsound
Dlib - 19.4.0


Execution
Order of Execution is as follows:

1.	Follow these installation guides - Numpy, OpenCV, Playsound, Dlib,  and install the right versions of the libraries (mentioned above).
2.	Make sure you have the model.
3.	python drowsy_v4.py

How It Works
This project is deeply centered around predicting the facial landmarks of a given face. We can accomplish a lot of things using these landmarks. From detecting eye-blink, yawns of mouth . The applications, outcomes and possibilities of facial landmarks are immense and intriguing.
Using these predicted landmarks of the face, we can build appropriate features that will further allow us to detect certain actions, like using the eye-aspect-ratio  to detect a blink , using the mouth-aspect-ratio to detect a yawn . In this project, these actions are programmed as triggers to detect the drivers drowsiness. 

Eye-Aspect-Ratio (EAR)

You will see that Eye-Aspect-Ratio is the simplest and the most elegant feature that takes good advantage of the facial landmarks. EAR helps us in detecting blinks and winks etc.
You can see that the EAR value drops whenever the eye closes. We can train a simple classifier to detect the drop. However, a normal if condition works just fine. Something like this:


Mouth-Aspect-Ratio (MAR)

Highly inspired by the EAR feature, I tweaked the formula a little bit to get a metric that can detect open/closed mouth. Unoriginal but it works.
Similar to EAR, MAR value goes up when the mouth opens. Similar intuitions hold true for this metric as well.

 
If the height of the mouth is greater than width then it will consider as yawning.

