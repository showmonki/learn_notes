from tensorflow import keras
from tensorflow.keras import backend as K

class t_model():

    def __init__(self):
        self.input_shape = (71, 71, 3) # xception at least 71x71
        self.base_model = self.load_model()
        # self.base_model1 = self.load_model1()

    def load_model(self):
        inputs = keras.Input(shape=self.input_shape, name = 'model_origin_input')
        K.set_learning_phase(0)
        base_model = keras.applications.Xception(weights='imagenet', include_top=False,input_tensor=inputs)
        base_model.trainable = False
        K.set_learning_phase(1)
        gmp = keras.layers.GlobalMaxPool2D(name='gmp')(base_model.output)
        # bn = keras.layers.BatchNormalization()(gmp)
        top_dropout_rate = 0.2
        # rld = keras.layers.Dense(16, activation='relu')(gmp)
        dp = keras.layers.Dropout(top_dropout_rate, name="top_dropout")(gmp)
        outputs = keras.layers.Dense(10, activation='softmax')(dp)
        model = keras.Model(inputs, outputs,name = 'new_model')

        model.compile(optimizer=keras.optimizers.Adam(),
                      loss='categorical_crossentropy',
                      # keras.losses.BinaryCrossentropy(from_logits=True),
                      metrics=['accuracy'])
        return model

    def load_model1(self):
        inputs = keras.Input(shape=self.input_shape, name = 'model_origin_input')
        base_model = keras.applications.Xception(weights='imagenet', include_top=False)
        base_model.trainable = False
        x = base_model(inputs,training = False)
        x = keras.layers.Conv2D(filters=32, kernel_size=3, padding='same', activation='relu',name='top_conv')(x)
        x = keras.layers.GlobalMaxPool2D(name='gmp')(x)
        # gmp2 = keras.layers.GlobalMaxPool2D(name='gmp2')(gmp)
        x = keras.layers.Dense(30, activation='relu')(x)
        top_dropout_rate = 0.5
        x = keras.layers.Dropout(top_dropout_rate, name="top_dropout")(x)
        outputs = keras.layers.Dense(10, activation='softmax')(x)
        model = keras.Model(inputs, outputs,name = 'top_model')

        model.compile(optimizer=keras.optimizers.Adam(),
                      loss='categorical_crossentropy',
                      # keras.losses.BinaryCrossentropy(from_logits=True),
                      metrics=['accuracy'])
        return model


class raw_model():

    def __init__(self):
        self.input_shape = (71, 71, 3)
        self.base_model = self.load_model()

    def load_model(self):
        inputs = keras.Input(shape=self.input_shape, name = 'model_input')
        dropout_rate = 0.2

        x = keras.layers.Conv2D(filters=64,kernel_size=3,name='conv1_1',padding='same',activation='relu')(inputs)
        x = keras.layers.Conv2D(filters=64,kernel_size=1,name='conv1_2',activation='relu')(x)
        x = keras.layers.MaxPool2D(name='mp1')(x)
        x = keras.layers.BatchNormalization(name='bn1')(x)
        # x = keras.layers.Dropout(dropout_rate, name="drp1")(x)

        x = keras.layers.Conv2D(filters=64, kernel_size=3, name='conv2_1',padding='same',activation='relu')(x)
        x = keras.layers.Conv2D(filters=64, kernel_size=1, name='conv2_2',activation='relu')(x)
        x = keras.layers.MaxPool2D(name='mp2')(x)
        x = keras.layers.BatchNormalization(name='bn2')(x)
        # x = keras.layers.Dropout(dropout_rate, name="drp2")(x)

        x = keras.layers.Conv2D(filters=64, kernel_size=3, name='conv3',padding='same',activation='relu')(x)
        x = keras.layers.Conv2D(filters=64, kernel_size=1, name='conv3_2',activation='relu')(x)
        x = keras.layers.MaxPool2D(name='mp3')(x)
        x = keras.layers.BatchNormalization(name='bn3')(x)
        # x = keras.layers.Dropout(dropout_rate, name="drp3")(x)

        x = keras.layers.Dense(200, activation='relu')(x)
        x = keras.layers.GlobalMaxPool2D(name='gmp')(x)
        outputs = keras.layers.Dense(10, activation='softmax')(x)
        model = keras.Model(inputs, outputs,name = 'raw_model')

        model.compile(optimizer=keras.optimizers.Adam(),
                      loss='categorical_crossentropy',
                      # keras.losses.BinaryCrossentropy(from_logits=True),
                      metrics=['accuracy'])
        return model
