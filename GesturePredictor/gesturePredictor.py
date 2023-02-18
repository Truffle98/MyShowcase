import tensorflow as tf
import cv2
import keyboard as kb

import random as random
import numpy as np

model = tf.keras.models.load_model("gesturePredictor")

from handTracker import HandTracker

# Function to calculate X and Y difference between two points
def calculateXYDiff(point1, point2):
    xDiff = point1[1] - point2[1]
    yDiff = point2[2] - point1[2]

    return [xDiff, yDiff]

# Different gestures
gesture_types = ["Peace", "Upsidedown Peace", "O", "OK", "Thumbs Up", "Thumbs Down", 
            "Thumb Left", "Thumb Right", "Fist", "Fully Open Palm", "Point Straight"]

tracker = HandTracker()
cap = cv2.VideoCapture(0)

while True:

    success,image = cap.read()
    image = cv2.flip(image, 1)
    image = tracker.handsFinder(image)
    hand_count = tracker.handCount()

    # If theres a hand
    if hand_count > 0:
        for i in range(hand_count):
            hand = tracker.leftOrRight(i)
            if hand == 0:
                lmList = tracker.positionFinder(image)
                data_points = []
                for i in range(20):
                    dataXY = calculateXYDiff(lmList[i + 1], lmList[0])
                    data_points.append(dataXY[0])
                    data_points.append(dataXY[1])
                
                for i in range(len(data_points)):
                    data_points[i] = (data_points[i] + 350) / 700
                
                prediction = model.predict([data_points], verbose=0)[0].tolist()
                prediction_max = max(prediction)
                prediction_idx = prediction.index(prediction_max)
                print("Gesture: {0}, Confidence: {1:.2f}".format(gesture_types[prediction_idx], prediction_max))
                    

    cv2.imshow("Video",image)
    cv2.waitKey(10)

    if kb.is_pressed("q"):
        break

cv2.destroyAllWindows()

print("No errors !")
