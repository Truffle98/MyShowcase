import cv2
import keyboard as kb
import os

from handTracker import HandTracker

# Function to calculate X and Y difference between two points
def calculateXYDiff(point1, point2):
    xDiff = point1[1] - point2[1]
    yDiff = point2[2] - point1[2]

    return [xDiff, yDiff]

# Writes data to a text file
def writeData(data_list):
    data_string = ""
    for i in range(len(data_list)):
        data_string += str(data_list[i])
        if i == len(data_list) - 1:
            data_string += "\n"
        else:
            data_string += " "

    data_file.write(data_string)

# Makes TrainingData folder
if not os.path.exists("TrainingData"):
    os.mkdir("TrainingData")
    print("Created TrainingData folder.")

# Different gestures
gesture_types = ["Peace", "Upsidedown Peace", "O", "OK", "Thumbs Up", "Thumbs Down", 
            "Thumb Left", "Thumb Right", "Fist", "Fully Open Palm", "Point Straight"]

tracker = HandTracker()
cap = cv2.VideoCapture(0)
data_file = open("TrainingData/handData.txt", "a")
intermission_wait = 200
data_points_per_gest = 400
data_count = data_points_per_gest
gest_idx = -1
intermission = False

while True:

    # Starts the intermission and tells the user what gesture to make
    if not intermission and data_count == data_points_per_gest:

        intermission = True
        data_count = 0
        gest_idx += 1
        if gest_idx < len(gesture_types):
            print("Prepare to make a gesture.")
            print("The gesture to make is: {}".format(gesture_types[gest_idx]))
        else:
            print("All gestures recorded.")
            break

    # Initiates data collection
    elif intermission and data_count == intermission_wait:

        intermission = False
        data_count = 0
        print("Ok recording data !")

    # Image capture through webcam
    success,image = cap.read()
    image = cv2.flip(image, 1)
    image = tracker.handsFinder(image)
    hand_count = tracker.handCount()

    # Collects and saves data
    if not intermission:
        if hand_count > 0:
            for i in range(hand_count):
                hand = tracker.leftOrRight(i)
                if hand == 0:
                    lmList = tracker.positionFinder(image)
                    data_points = [gest_idx]
                    for i in range(20):
                        dataXY = calculateXYDiff(lmList[i + 1], lmList[0])
                        data_points.append(dataXY[0])
                        data_points.append(dataXY[1])
                    writeData(data_points)

    cv2.imshow("Video",image)
    cv2.waitKey(10)
    data_count += 1

    if kb.is_pressed("q"):
        break

print("No errors !")