import tensorflow as tf
import numpy as np
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from sklearn import metrics
from tensorflow.keras.utils import to_categorical
from my_data import load_train_data
from image_class import t_model,raw_model
from image_util import display_learning_curves

# Part 1: prepare
# base = t_model().base_model
base = raw_model().base_model
dim = (71,71)
(x_train, y_train), (x_test, y_test) = load_train_data(dim)

X = np.repeat(np.reshape(x_train, (len(x_train),*dim))[...,np.newaxis], 3, -1) # 灰度to三通道
y_train = to_categorical(y_train)

# Part 2: train the model
print(base.summary())
history = base.fit(X, y_train, epochs=10, validation_split=0.2)
display_learning_curves(history)
print('train finish')
# Part 3: view current model performance
X_test = np.repeat(np.reshape(x_test, (len(x_test),*dim))[...,np.newaxis], 3, -1) # 灰度to三通道
X_test=tf.cast(X_test,tf.float32)
y_pred_raw = base.predict(X_test)
y_pred = np.argmax(y_pred_raw,axis=1)
y_pred_proba = np.max(y_pred_raw,axis=1)
print(metrics.classification_report(y_test,y_pred))
print(metrics.confusion_matrix(y_test,y_pred))


# Part 4: save model
base.save('./image_raw_model.h5')
print('done')
