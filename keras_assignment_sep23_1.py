# -*- coding: utf-8 -*-
"""Keras_Assignment_Sep23-1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aCbN8xgdNxJAFuv47pus0KRpHiyYVW2p

# Applied Data Science 2 - Keras Assignment - 2023A

In this assignment you will be building a script to classify images of animals. The assignment is broken up into sections and you need to complete each section successively. The sections are:

1. Data Processing
2. Model Definition
3. Model Training
4. Model Evaluation

In addition to this coding exercise, you will also need to write a 1-2 page report analysing and critically evaluating you models results.
"""

# Enter your module imports here, some modules are already provided

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import os
import pathlib
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, GlobalAveragePooling2D, Dense
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import Adam

# CodeGrade Tag Init1
from google.colab import drive
drive.mount('/content/drive')

"""# Data Processing


"""

# CodeGrade Tag DataProc

label_dict = {'cat' : 0,
              'dog' : 1,
              'wild' : 2}

# This function is provided to read in the image files from the folder on your
# Google Drive
def parse_image(filename):
  parts = tf.strings.split(filename, os.sep)
  label = parts[-2]
  label = tf.strings.to_number(label)

  image = tf.io.read_file(filename)
  image = tf.io.decode_jpeg(image)
  return image, label

img_loc = "/content/drive/MyDrive/Animals/"

train_list_ds = tf.data.Dataset.list_files(img_loc + "train/*/*")
valid_list_ds = tf.data.Dataset.list_files(img_loc + "val/*/*")

"""**Create a function called "img_process" converts the images to float32 datatype and resizes them to 64x64 pixels.**"""

# CodeGrade Tag Ex1a
### Write a function called img_process, which takes in the image and label as
### inputs, converts the data type of the image to tf.float32, resizes the
### image to (64,64), and finally returns the image and labels.

def img_process(image, label):
  image = tf.cast(image, tf.float32)
  image = tf.image.resize(image, [64, 64])
  return image, label

"""**Using the tf.data API, load in the training and validation data. Be mindful of efficient data processing good practice to minimise the time it takes to load the data.**"""

# CodeGrade Tag Ex1b
### Use the parse_image and img_process functions to construct the training and
### validation datasets. You should utilise good practice in optimising the
### dataset loading. Use a batch size of 128. Use techniques like caching and
### prefetching to efficiently load the data.
train_ds = (
    train_list_ds
    .map(parse_image, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(128)
    .map(img_process, num_parallel_calls=tf.data.AUTOTUNE)
    .cache()
    .prefetch(tf.data.AUTOTUNE)
)

val_ds = (
    valid_list_ds
    .map(parse_image, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(128)
    .map(img_process, num_parallel_calls=tf.data.AUTOTUNE)
    .cache()
    .prefetch(tf.data.AUTOTUNE)
)

"""# Model Definition

**Using the Keras Functional API, create a convolutional neural network with the architecture show in the model summary below.**

**A few important points to consider:**

* Call the convolutional layers and the first dense layer should have ReLU activation functions. The output layer should have a SoftMax activation function.
* Pay attention to the output shapes and the number of partmeters for each layer, as these give indications as to the correct settings for the number of filters, kernel size, stride length and padding.
* Use the layer names provided in the summary in your model.

```
# Model Summary

Model: "model"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 Input (InputLayer)          [(None, 64, 64, 3)]       0         
                                                                 
 Conv0 (Conv2D)              (None, 32, 32, 16)        1216      
                                                                 
 Conv1 (Conv2D)              (None, 32, 32, 32)        4640      
                                                                 
 Conv2 (Conv2D)              (None, 32, 32, 32)        9248      
                                                                 
 Pool1 (MaxPooling2D)        (None, 16, 16, 32)        0         
                                                                 
 Conv3 (Conv2D)              (None, 16, 16, 64)        18496     
                                                                 
 Conv4 (Conv2D)              (None, 16, 16, 64)        36928     
                                                                 
 Pool2 (MaxPooling2D)        (None, 8, 8, 64)          0         
                                                                 
 Conv5 (Conv2D)              (None, 8, 8, 128)         73856     
                                                                 
 Conv6 (Conv2D)              (None, 8, 8, 128)         147584    
                                                                 
 GlobalPool (GlobalAverageP  (None, 128)               0         
 ooling2D)                                                       
                                                                 
 FC1 (Dense)                 (None, 512)               66048     
                                                                 
 Output (Dense)              (None, 10)                5130      
                                                                 
=================================================================
Total params: 363146 (1.39 MB)
Trainable params: 363146 (1.39 MB)
Non-trainable params: 0 (0.00 Byte)
_________________________________________________________________


```
"""

# CodeGrade Tag Ex2a
### Define the model using the Keras Functional API. Use the summary above as a
### guide for the model parameters. You will need to define the filters/units of
### the layers correctly, as well as the kernel size, stride length and padding
### of the convolutional layers.

Input = tf.keras.Input((64,64,3), name= 'Input')

Conv0 = tf.keras.layers.Conv2D(16, (5,5), (2,2), activation="relu", padding="same", name="Conv0")(Input)
Conv1 = tf.keras.layers.Conv2D(32, (3,3), activation="relu", padding="same", name="Conv1")(Conv0)
Conv2 = tf.keras.layers.Conv2D(32, (3,3), activation="relu", padding="same", name="Conv2")(Conv1)
Pool1 = tf.keras.layers.MaxPooling2D((2,2),name = 'Pool1')(Conv2)
Conv3 = tf.keras.layers.Conv2D(64, (3,3), activation="relu", padding="same", name="Conv3")(Pool1)
Conv4 = tf.keras.layers.Conv2D(64, (3,3), activation="relu", padding="same", name="Conv4")(Conv3)
Pool2 = tf.keras.layers.MaxPooling2D((2,2),name = 'Pool2')(Conv4)
Conv5 = tf.keras.layers.Conv2D(128,(3,3),activation='relu',padding='same',name='Conv5')(Pool2)
Conv6 = tf.keras.layers.Conv2D(128,(3,3),activation='relu',padding='same',name='Conv6')(Conv5)
GlobalPool = tf.keras.layers.GlobalAveragePooling2D(name='GlobalPool')(Conv6)
FC1 = tf.keras.layers.Dense(512,activation='relu',name='FC1')(GlobalPool)
Output = tf.keras.layers.Dense(3,activation='softmax',name='Output')(FC1)
model = tf.keras.models.Model(inputs=Input,outputs = Output, name = 'model')

# CodeGrade Tag Ex2b
### Print the model summary and confirm is has the same architecture as the one
### provided.
model.summary()

"""**Compile the model using the Adam Optimizer with a learning rate of ```5e-5```, ```sparse categorical crossentropy``` loss function, and ```accuracy``` metric.**"""

# CodeGrade Tag Ex2c

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=5e-5),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

"""# Model Training

**Create a Model Checkpoint Callback that saves the weights of the best performing epoch, based on the validation accuracy.**
"""

# CodeGrade Tag Ex3a
### Create a ModelCheckpoint callback to store the bext weights from the model,
### based on the validation accuracy. Call this callback "checkpoint_callback"

checkpoint_filepath = '/content/checkpoint'
checkpoint_callback = keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=True,
    monitor='val_accuracy',
    mode='max',
    save_best_only=True)

"""**Create a Learning Rate Scheduler Callback that utilises the provided function to decrease the learning rate during training.**"""

# CodeGrade Tag Ex3b
### Using the function provided, create a LearningRateScheduler callback, call
### it "lr_callback"

def scheduler(epoch, lr):
    if epoch < 10:
        return lr
    else:
        return lr * tf.math.exp(-0.01)
lr_callback = keras.callbacks.LearningRateScheduler(scheduler)

"""**Train the model for 100 epochs, using the callbacks you made previously. Store the losses and metrics to use later.**"""

# CodeGrade Tag Ex3c
### Train the model for 100 epochs, using the callbacks you have created. Store
### the losses and metrics in a history object.

history = model.fit(train_ds,
                    validation_data=val_ds,
                    epochs=100,
                    callbacks=[checkpoint_callback, lr_callback])

"""# Model Evaluation

**Create plots using the losses and metrics. In your report, discuss these results and critically evaluate the models performance.**
"""

# CodeGrade Tag Ex4a
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc='upper right')
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc='upper right')
plt.show()

"""**Load the best weights from your model checkpoint, and create plots demonstrating the classification perfomnce for all three classes. Include these plots in your report, and critically evaluate on the performance of the model across the classes.**"""

# CodeGrade Tag Ex4b

# Load best weights
model.load_weights(checkpoint_filepath)

# Get predictions on validation data
predictions = np.argmax(model.predict(val_ds), axis=1)

# Convert true labels from dataset into numpy array
true_labels = np.concatenate([y for x, y in val_ds], axis=0)

# Plot confusion matrix
cm = tf.math.confusion_matrix(true_labels, predictions)

fig, ax = plt.subplots(figsize=(6, 6))
cax = ax.matshow(cm, cmap='Blues')
fig.colorbar(cax)

tick_locations = [0, 1, 2]

ax.set_xticks(tick_locations)
ax.set_yticks(tick_locations)
ax.set_xticklabels(['cat', 'dog', 'wild'])
ax.set_yticklabels(['cat', 'dog', 'wild'])
ax.set_xlabel('Predicted Label')
ax.set_ylabel('True Label')
ax.set_title('Confusion Matrix')

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        ax.text(j, i, str(cm.numpy()[i, j]), ha='center', va='center', color='red', fontsize=12)
plt.show()