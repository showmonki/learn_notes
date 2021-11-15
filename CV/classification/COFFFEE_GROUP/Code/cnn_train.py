from cnn_model import t2
from cnn_utils import display_learning_curves
from my_data import load_train_data
import os
from tensorflow import keras
import numpy as np
np.random.seed(0)
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
# ↑ for ↓ error
# OMP: Error #15: Initializing libiomp5.dylib, but found libomp.dylib already initialized.
# OMP: Hint This means that multiple copies of the OpenMP runtime have been linked into the program. That is dangerous, since it can degrade performance or cause incorrect results. The best thing to do is to ensure that only a single OpenMP runtime is linked into the process, e.g. by avoiding static linking of the OpenMP runtime in any library. As an unsafe, unsupported, undocumented workaround you can set the environment variable KMP_DUPLICATE_LIB_OK=TRUE to allow the program to continue to execute, but that may cause crashes or silently produce incorrect results. For more information, please see http://www.intel.com/software/products/support/.

# Part 1: prepare
height, width = 500, 500
dim = (height,width,3)

img_path = '../Input'
X,y,label_dict = load_train_data(dim, img_path)
# label_dict1 = {v:k for k,v in label_dict.items()} # predict 中有convert func
num_classes=len(label_dict)

# Part 2: train the model
clf = t2(num_classes,dim).base_model
clf.summary()
my_callbacks = [
    keras.callbacks.EarlyStopping(monitor='accuracy',min_delta=0.05, patience=4),
#     tf.keras.callbacks.ModelCheckpoint(filepath='model.{epoch:02d}-{val_loss:.2f}.h5'),
    keras.callbacks.TensorBoard(log_dir='./logs', update_freq=5),
]
history = clf.fit(X,y, epochs=30, callbacks=my_callbacks)#, validation_split=0.2)
print('train finish')

# Part 3: view current model performance
display_learning_curves(history)


# Part 4: save model
# model_save_path = '../Model/coffee_img_label.txt'
# with open(model_save_path, "w") as f:
# 	f.write(str(label_dict))
clf.save('../Model/coffee_img_model_t2_202111.h5')

print('done')