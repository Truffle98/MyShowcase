import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.models import Model
from keras.layers.core import Dense
from keras.layers import Input
import random as random
import numpy as np

print(tf.__version__)

# Data read and normalization

file = open("TrainingData/handData.txt")
dataLines = file.readlines()
file.close()

# Different gestures
gesture_types = ["Peace", "Upsidedown Peace", "O", "OK", "Thumbs Up", "Thumbs Down", 
            "Thumb Left", "Thumb Right", "Fist", "Fully Open Palm", "Point Straight"]

yData = []
xData = []
highest_num = -10000
lowest_num = 10000

for line in dataLines:
    splitLine = line[:-1].split(" ")
    data_list = []

    for data in splitLine:
        data_list.append(int(data))

    single_data = []

    yData.append(data_list[0])
    for i in range(len(data_list) - 1):
        single_data.append((data_list[i + 1] + 350) / 700)

    xData.append(single_data)

# Make sure all data is inside bounds
found_outside_data = False
for i in range(len(xData)):
    for j in range(len(xData[0])):
        if xData[i][j] > 1 or xData[i][j] < 0:
            found_outside_data = True

if found_outside_data:
    raise ValueError("Data was outside the set range.")
else:
    print("Data normalization succeeded.")

# Shuffle data
random_idxs = list(range(len(dataLines)))
random.shuffle(random_idxs)

shuffled_xData = []
shuffled_yData = []

for i in range(len(dataLines)):
    shuffled_xData.append(xData[random_idxs[i]])
    shuffled_yData.append(yData[random_idxs[i]])

train_length = round(len(dataLines) * 0.8)
test_length = round(len(dataLines) * 0.2)

print("Train length: {}".format(train_length))
print("Test length: {}".format(test_length))

xTrain = shuffled_xData[:train_length]
xTest = shuffled_xData[train_length:]

xTrain = (np.array(xTrain))
xTest = (np.array(xTest))

yTrain = shuffled_yData[:train_length]
yTest = shuffled_yData[train_length:]

yTrain = (np.array(yTrain)).T
yTest = (np.array(yTest)).T

#Making the model

def BuildModel():

    inputLayer = Input(shape=(40), name = "inputLayer")
    firstDense = Dense(units = "12", activation = "relu") (inputLayer)

    output = Dense(units = len(gesture_types) + 1, activation = "softmax", name = "outputLayer") (firstDense) 

    model = Model(inputs = inputLayer, outputs = output)

    return model

model = BuildModel()
model.summary()

model.compile(optimizer="adam", loss={"outputLayer": keras.losses.SparseCategoricalCrossentropy(from_logits=False)}, metrics=["accuracy"])

#Training the model and saving it

model.fit(x = xTrain, y = yTrain, epochs = 100, batch_size = 32)
print("Evaluation:")
model.evaluate(x = xTest, y = yTest, verbose=2)

model.save("gesturePredictor", save_format = tf)

print("No errors !")