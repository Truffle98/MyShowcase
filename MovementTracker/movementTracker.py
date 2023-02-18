import numpy as np
import cv2
import keyboard as kb
import copy
import os

# Setup parameters
resolution = (1920, 1080)
resize_res = (480, 270)
num_frames = 50
color_tolerance_starting_pixel = 40
color_tolerance_connecting_pixels = 10
minimum_connecting = 200
show_imgs = True
save_imgs = False

# Prepares to save images
if not os.path.exists("unrefinedBlobs") and save_imgs:
    os.mkdir("unrefinedBlobs")
    print("Created unrefinedBlobs folder.")

# Loads up user folder path
path = "None"
while not os.path.exists(path):
    path = input("Enter the screenshots path:")
    if not os.path.exists(path):
        print("Path does not exist.")

# Calculates the RGB difference between three pixels, the third being the noise cancelling pixel
def calculate_color_diff_3(pix1, pix2, pix3):

    diffs = []
    for i in range(3):
        diff = ((abs(int(pix1[i]) - int(pix2[i]))) / 255)
        diff -= ((abs(int(pix1[i]) - int(pix3[i]))) / 255)

        diff = max(diff, 0)
        diffs.append(diff)

    return (sum(diffs) / 3)

# This function takes a full image of RGB differences on a scale from 0-255 and finds clusters of pixels with high RGB difference
def find_blobs(image):

    blobs = []

    # Check for a starting point every 3 x 4 pixels, skips over some to improve speed and I haven't seen it miss a cluster because of pixel skips
    for i in range(resize_res[1]):
        if i % 3 != 0:
            continue

        for j in range(resize_res[0]):

            if j % 4 != 0:
                continue

            cont = False
            for k in range(len(blobs)):
                if [j, i] in blobs[k]:
                    cont = True
                    break

            if cont:
                continue

            if image[i][j][2] >= color_tolerance_starting_pixel:

                connecting_pix = [[j, i]]
                new_pixels = [[j, i]]
                while True:
                    
                    old_len = len(connecting_pix)
                    new_pixels = find_connecting_pixels(image, new_pixels, connecting_pix)
                    connecting_pix += new_pixels
                    new_len = len(connecting_pix)

                    if old_len == new_len:
                        break

                if len(connecting_pix) > minimum_connecting:
                    blobs.append(connecting_pix)

    return blobs

# Takes an image of RGB differences and some pixels to branch out from, then makes sure that the new pixels aren't duplicates
def find_connecting_pixels(image, new_pix, full_pix):

    connecting = []
    for i in range(len(new_pix)):
        if new_pix[i][1] < resize_res[1] - 1:
            if image[new_pix[i][1] + 1][new_pix[i][0]][2] >= color_tolerance_connecting_pixels and check_pixel_already_found([new_pix[i][0], new_pix[i][1] + 1], connecting, full_pix):
                connecting.append([new_pix[i][0], new_pix[i][1] + 1])
        if new_pix[i][1] > 0:
            if image[new_pix[i][1] - 1][new_pix[i][0]][2] >= color_tolerance_connecting_pixels and check_pixel_already_found([new_pix[i][0], new_pix[i][1] - 1], connecting, full_pix):
                    connecting.append([new_pix[i][0], new_pix[i][1] - 1])
        if new_pix[i][0] < resize_res[0] - 1:
            if image[new_pix[i][1]][new_pix[i][0] + 1][2] >= color_tolerance_connecting_pixels and check_pixel_already_found([new_pix[i][0] + 1, new_pix[i][1]], connecting, full_pix):
                connecting.append([new_pix[i][0] + 1, new_pix[i][1]])
        if new_pix[i][0] > 0:
            if image[new_pix[i][1]][new_pix[i][0] - 1][2] >= color_tolerance_connecting_pixels and check_pixel_already_found([new_pix[i][0] - 1, new_pix[i][1]], connecting, full_pix):
                connecting.append([new_pix[i][0] - 1, new_pix[i][1]])

    return connecting.copy()

# Makes sure that a pixel isn't a duplicate in the new_pixels and full_pixels list
def check_pixel_already_found(pixel, new_pixels, full_pixels):

    if pixel in new_pixels or pixel in full_pixels:
        return False

    return True

# Takes the location of all the pixels in a blob and gets it's cutout based on its maximum and minimum x and y values
# Returns a cutout of the original image
def get_blob_rectangle(image, blob):
    top_left = [1000, 1000]
    bottom_right = [-1, -1]

    for i in range(len(blob)):
        for j in range(2):

            if blob[i][j] < top_left[j]:
                top_left[j] = blob[i][j]
            if blob[i][j] > bottom_right[j]:
                bottom_right[j] = blob[i][j]

    blob_image = []
    for i in range(bottom_right[1] - top_left[1] + 1):
        temp = []
        for j in range(bottom_right[0] - top_left[0] + 1):
            temp.append(image[i + top_left[1]][j + top_left[0]].tolist())
        blob_image.append(temp)

    return np.array(blob_image, dtype=np.uint8)

# Sets up the first reference image
original_img = cv2.imread(path + "/frame0.png")
original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
original_img = cv2.resize(original_img, resize_res)

prev_original = copy.deepcopy(original_img)

saved_blobs_count = 0

# Iterates through every image and runs the algorithm
for imgN in range(1, num_frames - 1):

    # Loads up new image
    current_img = cv2.imread(path + "/frame" + str(imgN) + ".png")
    current_img = cv2.cvtColor(current_img, cv2.COLOR_BGR2RGB)
    current_img = cv2.resize(current_img, resize_res)

    movement_map = np.zeros((resize_res[1], resize_res[0], 3), dtype=np.uint8)

    if show_imgs:
        cv2.imshow("Reference image", original_img)
        cv2.imshow("Current image", current_img)
        cv2.imshow("Noise cancelling image", prev_original)

    # Gets RGB difference for all images and saves it in the movement map
    for i in range(resize_res[1]):
        for j in range(resize_res[0]):

            diff = calculate_color_diff_3(original_img[i][j], current_img[i][j], prev_original[i][j])

            movement_light = min(255 * diff, 255)
            movement_map[i][j][2] = movement_light
            
    # Collects all the blobs from the movement map
    blobs = find_blobs(movement_map)
    blob_images = []

    movement_map_with_blobs = movement_map.copy()

    # Collects all the blob images from the blobs
    for i in range(len(blobs)):

        blob_images.append(get_blob_rectangle(current_img, blobs[i]))
        for j in range(len(blobs[i])):

            movement_map_with_blobs[blobs[i][j][1]][blobs[i][j][0]][2] = 0
            movement_map_with_blobs[blobs[i][j][1]][blobs[i][j][0]][0] = 255

    prev_original = copy.deepcopy(original_img)

    # Changes all pixels in reference image to pixels from the most recent image, except for pixels that were part of a blob
    for i in range(resize_res[1]):
        for j in range(resize_res[0]):

            if movement_map_with_blobs[i][j][0] == 0:
                original_img[i][j] = current_img[i][j]

    movement_map = cv2.resize(movement_map, resolution)
    
    movement_map_with_blobs = cv2.resize(movement_map_with_blobs, resolution)

    # Shows the movement map and blobs to the user
    print("Num blobs: {}".format(len(blob_images)))

    if show_imgs:

        cv2.imshow("Movement map", movement_map)
        cv2.imshow("Movement map with blobs", movement_map_with_blobs)

    for i in range(len(blob_images)):

        blob_resized = cv2.resize(blob_images[i], [64, 64])
        blob_recolored = cv2.cvtColor(blob_resized, cv2.COLOR_RGB2BGR)

        if show_imgs:

            cv2.imshow("Blob image" + str(i), blob_recolored)

        # Saves the blobs to the unrefinedBlobs folder if save_imgs is true
        if save_imgs:
            cv2.imwrite("unrefinedBlobs/blob" + str(saved_blobs_count) + ".png", blob_recolored) 
            saved_blobs_count += 1

    if show_imgs:

        cv2.waitKey(0)

    if kb.is_pressed("q"):
        break
    cv2.destroyAllWindows()

print("Total blobs:", saved_blobs_count)

cv2.destroyAllWindows()
print("No errors !")