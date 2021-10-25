from tensorflow import keras
from tensorflow.keras import backend as K

class t_model():

    def __init__(self,num_class,input_shape):
        self.input_shape = input_shape # xception at least 71x71
        self.num_cls = num_class
        # self.base_model = self.load_model()
        self.base_model1 = self.load_model1()

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
        outputs = keras.layers.Dense(self.num_cls, activation='softmax')(dp)
        model = keras.Model(inputs, outputs,name = 'new_model')

        model.compile(optimizer=keras.optimizers.Adam(),
                      loss='categorical_crossentropy',
                      # keras.losses.BinaryCrossentropy(from_logits=True),
                      metrics=['accuracy'])
        return model

    def load_model1(self):
        base_model = keras.applications.Xception(weights='imagenet', include_top=False,input_shape=self.input_shape)
        base_model.trainable = False
        x = base_model.output
        x = keras.layers.GlobalMaxPool2D(name='gmp')(x)
        # x = keras.layers.Dense(30, activation='relu')(x)
        outputs = keras.layers.Dense(self.num_cls, activation='softmax')(x)
        model = keras.Model(inputs = base_model.inputs, outputs = outputs,name = 'top_model')

        model.compile(optimizer=keras.optimizers.Adam(),
                      loss='categorical_crossentropy',
                      # keras.losses.BinaryCrossentropy(from_logits=True),
                      metrics=['accuracy'])
        return model


class t2():

    def __init__(self,num_classes,img_shape):
        self.input_shape = img_shape
        self.num_classes = num_classes
        self.base_model = self.load_model()

    def load_model(self):
        pretrain_model = keras.applications.InceptionResNetV2(include_top=False,input_shape=self.input_shape,weights='imagenet')
        pretrain_model.trainable = False
        x=pretrain_model.output
        x = keras.layers.GlobalMaxPool2D(name='gmp')(x)
        x = keras.layers.Dense(100, activation='softmax')(x)
        outputs = keras.layers.Dense(self.num_classes, activation='softmax')(x)
        model = keras.Model(inputs=pretrain_model.input, outputs=outputs, name='transfer_model')

        model.compile(optimizer=keras.optimizers.Adam(),
                      loss='categorical_crossentropy',
                      # keras.losses.BinaryCrossentropy(from_logits=True),
                      metrics=['accuracy'])
        return model

