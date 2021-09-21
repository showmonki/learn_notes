from cnn_model import CNNKeras,TCNNConfig
from sklearn.model_selection import train_test_split
from cnn_utils import display_learning_curves,load_train,init_vec,validate_performance
import pickle

# Part 1: prepare
input_path = '../Input/CERE310/train.txt'
cols = ['label','desc']  # 可以改顺序，但是不要改列名
config = TCNNConfig()
X, y, config.num_classes, config.label_dict = load_train(input_path, cols)
X_vec, config.vocab = init_vec(X,config.seq_length,config.vocab_size)


# Part 2: train the model
clf = CNNKeras(config)
clf.model.summary()
X_train, X_val, y_train, y_val = train_test_split(X_vec,y,test_size=0.2,random_state=0)
history = clf.model.fit(X_train,y_train, epochs=2, validation_split=0.2)
print('train finish')

# Part 3: view current model performance
display_learning_curves(history)
# TODO 增加logging for train log

validate_performance(X_val,y_val, clf.model)

# Part 4: save model
# TODO 模型只能以h5保存。pkl报错：TypeError: can't pickle _thread.RLock objects
# model_save_path = '../Model/textcnn_model.pkl'
# with open(model_save_path, "wb") as f:
# 	pickle.dump(clf, f)
clf.model.save('../Model/textcnn_model.h5')
with open('../Model/textcnn_model_config.pkl', "wb") as f:
	pickle.dump(clf.config, f)

print('done')