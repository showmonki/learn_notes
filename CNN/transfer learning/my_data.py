import numpy as np


def load_train_data(dim):
	from keras.datasets import mnist
	(x_train, y_train), (x_test, y_test) = mnist.load_data()

	x_train_convert = [convert_pic(data,dim) for data in x_train]
	x_test_convert = [convert_pic(data,dim) for data in x_test]
	return (np.array(x_train_convert),y_train),(np.array(x_test_convert),y_test)


def convert_pic(data,dim):
	import cv2
	return cv2.resize(data, dim, interpolation=cv2.INTER_AREA)


def load_test_data(path,dim):
	import cv2
	img = cv2.imread(path)
	img_convert = convert_pic(img, dim)
	return img_convert