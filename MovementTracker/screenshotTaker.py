import pyautogui as pag
import os
import time

if not os.path.exists("slowScreenshots"):
    os.mkdir("slowScreenshots")
    print("Created slowScreenshots folder.")

# Waits 5 seconds for the user to be ready then takes 50 screenshots with 0.2 seconds between them
time.sleep(5)
for i in range(50):

    pag.screenshot("slowScreenshots/frame" + str(i) + ".png")
    time.sleep(0.2)

print("No errors !")