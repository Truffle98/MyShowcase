import tensorflow as tf
import numpy as np
import os
import cv2
print(tf.__version__)

blob_counter = 0
images = []
original_images = []

# Loads up the refined blobs from the refinedBlobs folder
while True:

    if os.path.exists("refinedBlobs/blob" + str(blob_counter) + ".png"):

        temp_img = cv2.imread("refinedBlobs/blob" + str(blob_counter) + ".png")
        original_images.append(temp_img)
        temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY)
        temp_img = temp_img.flatten()
        images.append(temp_img)
        blob_counter += 1

    else:
        break

# Specify clusters and iterations
num_clusters = 2
num_iterations = 100

images = np.array(images)
kmeans = tf.compat.v1.estimator.experimental.KMeans(num_clusters=num_clusters, use_mini_batch=False)

def input_fn():
    return tf.compat.v1.train.limit_epochs(tf.convert_to_tensor(images, dtype=tf.float32), num_epochs=1)

# Train
num_iterations = 10
previous_centers = None
for _ in range(num_iterations):
    kmeans.train(input_fn)
    cluster_centers = kmeans.cluster_centers()
    previous_centers = cluster_centers
    print( 'score:', kmeans.score(input_fn))

image_clusters = []
for i in range(num_clusters):
    image_clusters.append([])

# Map the input images to their clusters
cluster_indices = list(kmeans.predict_cluster_index(input_fn))
for i, image in enumerate(original_images):
    cluster_index = cluster_indices[i]
    image_clusters[cluster_index].append(image)
    
labels = []

for i, cluster in enumerate(image_clusters):

    print("Now showing cluster", i + 1)
    for j, image in enumerate(cluster):
        cv2.imshow("Image " + str(j + 1), image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

print("No errors !")