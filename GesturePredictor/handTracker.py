import cv2
import mediapipe as mp
import time
import keyboard as kb
import pyautogui as pag
import ctypes
from google.protobuf.json_format import MessageToDict

# HandTracker class to deal with a lot of the hand tracking functions from the library, and determine classifiers about the data
# Classifiers are the amount of hands, left or right hand, location of points on hands, and hand count
class HandTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def handsFinder(self,image,draw=True):
        imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def positionFinder(self,image, handNo=0, draw=False):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id,cx,cy])
            if draw:
                cv2.circle(image,(cx,cy), 15 , (255,0,255), cv2.FILLED)

        return lmlist

    def leftOrRight(self, handNo):
        single_classification = self.results.multi_handedness[handNo]
        handedness_dict = MessageToDict(single_classification)
        label = handedness_dict['classification'][0]['label']
        #print('Handedness:', label)
        if label == "Right":
            return 0
        elif label == "Left":
            return 1

    def handCount(self):
        if self.results.multi_handedness:
            num_hands = len(self.results.multi_handedness)
        else:
            num_hands = 0
        #print('Number of hands:', num_hands)
        return num_hands