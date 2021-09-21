import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
from collections import Counter
from itertools import chain
import tensorflow as tf


def load_train(input_path,cols):
	df = pd.read_csv(input_path,names=cols).dropna(axis=0,subset=['desc'])
	X = [[c.upper() for c in desc] for desc in df['desc'].to_list()]
	# X = [' '.join([c.upper() for c in desc]) for desc in df['desc'].to_list()]  # 空格是为了tfidf,counter使用
	labels = list(set(df['label']))
	num_classes = len(labels)
	label_dict = dict(zip(labels,range(num_classes)))
	y = to_categorical(df['label'].map(label_dict))
	# y.shape -> (?, num_classes)
	return X,y,num_classes, label_dict


def txt2vec(txt_str, max_len,vocab):
	txt_vec = [vocab[char.upper()] if char.upper() in vocab  else vocab['<pad>']  for char in txt_str]
	txt_vec = pad_sequences([txt_vec],max_len,padding='post')
	return txt_vec


def multi_txt2vec(txts, max_len,vocab):
	txt_vec = [[vocab[char.upper()]  if char.upper() in vocab  else vocab['<pad>'] for char in txt_l] for txt_l in txts]
	txt_vec = pad_sequences(txt_vec,max_len,padding='post')
	return txt_vec


def count_vec(txt,vocab_size):
	"""  min_df不加入，以防出现次数过少但有用的词    """
	vocab = CountVectorizer(analyzer='char',max_df=0.9,max_features=vocab_size)
	counter = vocab.fit_transform(txt)
	return counter, vocab


def tfidf_vec(txt,vocab_size):
	vocab = TfidfVectorizer(analyzer='char', max_df=0.9, min_df=0.1,max_features=vocab_size)
	tfidf = vocab.fit_transform(txt)
	return tfidf, vocab


def count_id(txt,vocab_size):
	counter = Counter(list(chain(*txt)))
	count_pairs = counter.most_common(vocab_size - 1)
	vocab = dict(zip([freq[0] for freq in count_pairs],range(2,len(count_pairs))))  # 从2开始计数，pad 补1，pad_sequence后面补数会补0
	vocab['<pad>'] = 1
	txt_vec = [[vocab[char]  if char in vocab  else vocab['<pad>'] for char in txt_l] for txt_l in txt]
	return txt_vec,vocab


def init_vec(txt,max_len ,vocab_size):
	"""  在train_test_split前使用比较好"""
	txt_list,vocab = count_id(txt,vocab_size)  # txt_list type list，但是已经转换过count——id了
	txt_vec = pad_sequences(txt_list,max_len,padding='post')
	# txt_vec,vocab = count_vec(txt,vocab_size)
	# txt_vec,vocab = tfidf_vec(txt,vocab_size)
	# txt_vec = pad_sequences(txt_vec.toarray(),max_len)
	return txt_vec, vocab


def validate_performance(X_test,y_test, clf):
	y_pred_raw = clf.predict(X_test)
	y_pred = np.argmax(y_pred_raw, axis=1)
	y_test_label = np.argmax(y_test, axis=1)
	# y_pred_proba = np.max(y_pred_raw, axis=1)
	from sklearn import metrics
	print(metrics.classification_report(y_test_label, y_pred))
	print(metrics.confusion_matrix(y_test_label, y_pred))


def display_learning_curves(history):
	fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

	ax1.plot(history.history["loss"])
	ax1.plot(history.history["val_loss"])
	ax1.legend(["train", "test"], loc="upper right")
	ax1.set_xlabel("Epochs")
	ax1.set_ylabel("Loss")

	ax2.plot(history.history["accuracy"])
	ax2.plot(history.history["val_accuracy"])
	ax2.legend(["train", "test"], loc="upper right")
	ax2.set_xlabel("Epochs")
	ax2.set_ylabel("Accuracy")
	plt.savefig('train_log.png')
	plt.show()


def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
	# First, we create a model that maps the input image to the activations
	# of the last conv layer as well as the output predictions
	grad_model = tf.keras.models.Model(
		[model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
	)
	# Then, we compute the gradient of the top predicted class for our input image
	# with respect to the activations of the last conv layer
	with tf.GradientTape() as tape:
		last_conv_layer_output, preds = grad_model(img_array)
		if pred_index is None:
			pred_index = tf.argmax(preds[0])
		class_channel = preds[:, pred_index]

	# This is the gradient of the output neuron (top predicted or chosen)
	# with regard to the output feature map of the last conv layer
	grads = tape.gradient(class_channel, last_conv_layer_output)

	# This is a vector where each entry is the mean intensity of the gradient
	# over a specific feature map channel
	pooled_grads = tf.reduce_mean(grads, axis=(0, 1))

	# We multiply each channel in the feature map array
	# by "how important this channel is" with regard to the top predicted class
	# then sum all the channels to obtain the heatmap class activation
	last_conv_layer_output = last_conv_layer_output[0]
	heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
	heatmap = tf.squeeze(heatmap)

	# For visualization purpose, we will also normalize the heatmap between 0 & 1
	heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
	return heatmap.numpy()


def _plot_score(heatmap, pred_label, xticks,txt_len):
	import matplotlib.pyplot as plt
	plt.rcParams['font.sans-serif'] = ['SimHei']  # ['SimHei'], Arial Unicode MS
	_axis_fontsize = 14
	fig = plt.figure(figsize=(14, 10))
	plt.yticks([])
	# 若报错does not match the number of ticklabels， matplotlib 版本更新
	plt.xticks(range(0, txt_len), xticks, fontsize=_axis_fontsize)
	fig.add_subplot(1, 1, 1)
	plt.figtext(x=0.13, y=0.54, s='Prediction: {}'.format(pred_label), fontsize=14, fontproperties="SimSun")
	img = plt.imshow([heatmap])
	plt.show()


def _get_text_xticks(sentence):
	tokens = [c for c in sentence]
	return tokens


