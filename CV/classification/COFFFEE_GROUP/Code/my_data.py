import numpy as np
from tensorflow.keras.utils import to_categorical


def load_train_data(dim, image_path):
	from os import listdir
	imgs = listdir(image_path)
	if '.DS_Store' in imgs:
		imgs.remove('.DS_Store')
	ids_all = []
	num_classes = len(imgs)
	label_dict = dict(zip(imgs, range(num_classes)))
	for label in imgs:
		ids = listdir(image_path+'/'+label)
		ids_all.extend([[prod_id, transfer_to_array(prod_id,image_path+'/'+label,dim[:2]), label_dict[label]] for prod_id in ids])
	X = np.array([ary[1] for ary in ids_all])
	y = [ary[2] for ary in ids_all]
	return X,to_categorical(y),label_dict


def convert_pic(data,dim):
	import cv2
	return cv2.resize(data, dim, interpolation=cv2.INTER_AREA)


def load_test_data(path,dim):
	import cv2
	img = cv2.imread(path)
	img_convert = convert_pic(img, dim)
	return img_convert

def transfer_to_array(prod_id, img_path,dim):
	from PIL import Image
	im = Image.open('{0}/{1}'.format(img_path, prod_id))
	if im.mode != 'RGB':
		im = im.convert('RGB')
	image_resized = im.resize((dim), Image.ANTIALIAS)
	temp_data = np.array(image_resized) / 255
	return temp_data