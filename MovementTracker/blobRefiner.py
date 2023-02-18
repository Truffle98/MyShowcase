import cv2
import keyboard as kb
import os

if not os.path.exists("refinedBlobs"):
    os.mkdir("refinedBlobs")
    print("Created refinedBlobs folder.")

resize_res = (512, 512)

blob_counter = 0
saved_blob_counter = 0

"""
start_box = np.zeros((resize_res[1], resize_res[0], 3), dtype=np.uint8)
cv2.imshow("Press any key to begin", start_box)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

# Iterates through all blobs in the unrefinedBlobs folder and determines if they should be saved
while True:

    if os.path.exists("unrefinedBlobs/blob" + str(blob_counter) + ".png"):
        
        cur_blob = cv2.imread("unrefinedBlobs/blob" + str(blob_counter) + ".png")
        resized_blob = cv2.resize(cur_blob, resize_res)
        cv2.imshow("Current blob", resized_blob)
        cv2.waitKey(0)
        # Saves blob if user hits 'space'
        # Always saves first one because of weird interactions with the keyboard library
        if kb.is_pressed('space') or blob_counter == 0:
            cv2.imwrite("refinedBlobs/blob" + str(saved_blob_counter) + ".png", cur_blob)
            saved_blob_counter += 1
            print("Blob saved")
        elif kb.is_pressed('q'):
            break
        else:
            print("Blob discarded")

        blob_counter += 1

    else:
        break

cv2.destroyAllWindows()
print("No errors !")