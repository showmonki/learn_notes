from tensorflow import keras
import tensorflow as tf
import numpy as np
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from sklearn import metrics
from tensorflow.keras.utils import to_categorical
from my_data import load_train_data,load_test_data

class t_model():

    def __init__(self):
        self.input_shape = (71, 71, 3) # xception at least 71x71
        self.base_model = self.load_model()

    def load_model(self):
        base_model = keras.applications.Xception(weights='imagenet', input_shape=self.input_shape, include_top=False)
        base_model.trainable = False

        inputs = keras.Input(shape=self.input_shape)
        x = base_model(inputs, training=False)
        x = keras.layers.GlobalMaxPool2D()(x)
        outputs = keras.layers.Dense(10, activation='softmax')(x)
        model = keras.Model(inputs, outputs)

        model.compile(optimizer=keras.optimizers.Adam(),
                      loss=
                      'categorical_crossentropy',
                      # keras.losses.BinaryCrossentropy(from_logits=True),
                      metrics=['accuracy'])
        return model



# Part 1: prepare
base = t_model().base_model
dim = (71,71)
(x_train, y_train), (x_test, y_test) = load_train_data(dim)

X = np.repeat(np.reshape(x_train, (len(x_train),*dim))[...,np.newaxis], 3, -1) # 灰度to三通道
y_train = to_categorical(y_train)

# Part 2: train the model
print(base.summary())
base.fit(X, y_train, epochs=10, validation_split=0.2)
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
# base.save('./image_xception_model.h5')
print('done')
# Part 5: Prediction Real cases

test_path = 'data/test_5_1.jpg'
test_img = load_test_data(test_path,dim)
test_IMG = np.expand_dims(test_img,axis=0) # 一个图片因此加dim
test_IMG=tf.cast(test_IMG,tf.float32)
result = base.predict(test_IMG)
predict_digit, prediction_prob = result.argmax(), result.max()
print('prediction is {0} with prob {1}'.format(predict_digit, prediction_prob))