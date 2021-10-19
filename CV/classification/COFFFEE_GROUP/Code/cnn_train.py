from cnn_model import t_model
from cnn_utils import display_learning_curves,validate_performance
from my_data import load_train_data
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
# ↑ for ↓ error
# OMP: Error #15: Initializing libiomp5.dylib, but found libomp.dylib already initialized.
# OMP: Hint This means that multiple copies of the OpenMP runtime have been linked into the program. That is dangerous, since it can degrade performance or cause incorrect results. The best thing to do is to ensure that only a single OpenMP runtime is linked into the process, e.g. by avoiding static linking of the OpenMP runtime in any library. As an unsafe, unsupported, undocumented workaround you can set the environment variable KMP_DUPLICATE_LIB_OK=TRUE to allow the program to continue to execute, but that may cause crashes or silently produce incorrect results. For more information, please see http://www.intel.com/software/products/support/.

# Part 1: prepare
dim = (300,300,3)
img_path = '../Input'
X,y,label_dict = load_train_data(dim, img_path)

# Part 2: train the model
clf = t_model(len(label_dict),dim).base_model1
clf.summary()
history = clf.fit(X,y, epochs=20)
print('train finish')

# Part 3: view current model performance
display_learning_curves(history)


# Part 4: save model
model_save_path = '../Model/coffee_img_label.txt'
with open(model_save_path, "w") as f:
	f.write(str(label_dict))
clf.save('../Model/coffee_img_model.h5')

print('done')