# import os
# os.chdir('NLP/textcnn/Code')
import numpy as np
import tensorflow as tf
from cnn_model import CNNKeras
from tensorflow import keras
import pickle
import matplotlib.pyplot as plt
from cnn_utils import make_gradcam_heatmap, txt2vec, _plot_score, _get_text_xticks

clf = keras.models.load_model('../Model/textcnn_model.h5')
with open('../Model/textcnn_model_config.pkl', "rb+") as f:
	train_config = pickle.load(f)
label_list = {v:k for k,v in train_config.label_dict.items()}


test_txt = 'Calbee/卡乐比进口原味水果麦片即食燕麦片早餐饱腹食品700g冲饮'
test_vec = txt2vec(test_txt,train_config.seq_length,train_config.vocab)
result = clf.predict(test_vec)
predict_label, prediction_prob = result.argmax(), result.max()
heatmap = make_gradcam_heatmap(test_vec, clf, 'conv3')
# plt.imshow([heatmap])
# plt.show()

resize_heatmap = tf.keras.preprocessing.image.array_to_img(heatmap[...,np.newaxis,np.newaxis])
resize_heatmap = resize_heatmap.resize((1,35))
resize_heatmap = tf.keras.preprocessing.image.img_to_array(resize_heatmap)
# plt.matshow(resize_heatmap[:,0])
# plt.show()
_plot_score(resize_heatmap[:,0,0], pred_label=label_list[predict_label], txt_len=len(test_txt), xticks=_get_text_xticks(test_txt))

