import numpy as np
import tensorflow as tf
from tensorflow import keras
from cnn_utils import url_to_image,make_gradcam_heatmap,convert_image,save_and_display_gradcam,url_to_image_crop
import matplotlib.pyplot as plt
# from azure.cognitiveservices.vision.computervision import ComputerVisionClient
# from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
# from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
# from msrest.authentication import CognitiveServicesCredentials
from PIL import ImageDraw
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


def url_predict_plot(url,conv_layer):
	test_IMG = url_to_image(url)
	test_convert = convert_image(test_IMG,dim)
	test_vec = np.expand_dims(test_convert,axis=0) # 一个图片因此加dim
	test_vec=tf.cast(test_vec,tf.float32)
	result = clf.predict(test_vec)
	predict_label, prediction_prob = result.argmax(), result.max()
	print('prediction is {0} with prob {1}'.format(label_dict[predict_label], prediction_prob))
	heatmap = make_gradcam_heatmap(test_vec, clf, conv_layer)
	# plt.imshow(heatmap)
	# plt.show()
	save_and_display_gradcam(test_IMG, heatmap,test_IMG.size,label_dict[predict_label], alpha=0.8)


def plot_func(url, conv_layer):
	"""    结合azure computervision api 使用      """


	from array import array
	import sys
	import time


	print("===== Prediction Probability =====")
	test_IMG = url_to_image(url)
	test_convert = convert_image(test_IMG, dim)
	test_vec = np.expand_dims(test_convert, axis=0)  # 一个图片因此加dim
	test_vec = tf.cast(test_vec, tf.float32)
	result = clf.predict(test_vec)
	predict_label, prediction_prob = result.argmax(), result.max()
	print('prediction is {0} with prob {1}'.format(label_dict[predict_label], prediction_prob))

	print("===== Detect Objects - remote =====")
	# Get URL image with different objects
	# Call API with URL
	detect_objects_results_remote = computervision_client.detect_objects(url)
	# Print detected objects results with bounding boxes
	draw = ImageDraw.Draw(test_IMG)
	print("Detecting objects in remote image:")
	if len(detect_objects_results_remote.objects) == 0:
		print("No objects detected.")
	else:
		for object in detect_objects_results_remote.objects:
			print("object at location {}, {}, {}, {}".format(object.rectangle.x, object.rectangle.y, \
			                                                 object.rectangle.x + object.rectangle.w,
			                                                 object.rectangle.y + object.rectangle.h))
			draw.rectangle([object.rectangle.x, object.rectangle.y, object.rectangle.x + object.rectangle.w,
			                object.rectangle.y + object.rectangle.h], outline='red', width=5)
	heatmap = make_gradcam_heatmap(test_vec, clf, conv_layer)
	save_and_display_gradcam(test_IMG, heatmap, test_IMG.size, label_dict[predict_label], alpha=0.8)


# COMMAND ----------

def plot_box_predict(url, conv_layer):
	print("===== Detect Objects - remote =====")
	# Get URL image with different objects
	# Call API with URL
	detect_objects_results_remote = computervision_client.detect_objects(url)
	#   test_IMG = url_to_image(url)
	# Print detected objects results with bounding boxes
	#   draw = ImageDraw.Draw(test_IMG)
	print("Detecting objects in remote image:")
	if len(detect_objects_results_remote.objects) == 0:
		print("No objects detected.")
		box = False
	else:
		for object in detect_objects_results_remote.objects:
			box = object.rectangle.x, object.rectangle.y, object.rectangle.x + object.rectangle.w, object.rectangle.y + object.rectangle.h
			print("object at location {}, {}, {}, {}".format(*box))
	#           draw.rectangle([*box], outline='red',width=5)

	print("===== Prediction Probability =====")
	test_IMG_crop = url_to_image_crop(url, box)
	test_convert = convert_image(test_IMG_crop, dim)
	test_vec = np.expand_dims(test_convert, axis=0)  # 一个图片因此加dim
	test_vec = tf.cast(test_vec, tf.float32)
	result = clf.predict(test_vec)
	predict_label, prediction_prob = result.argmax(), result.max()
	print('prediction is {0} with prob {1}'.format(label_dict[predict_label], prediction_prob))

	heatmap = make_gradcam_heatmap(test_vec, clf, conv_layer)
	save_and_display_gradcam(test_IMG_crop, heatmap, test_IMG_crop.size, label_dict[predict_label], alpha=0.8)


if __name__ == '__main__':
	clf = keras.models.load_model('../Model/coffee_img_model_t2.h5')
	with open('../Model/coffee_img_label.txt', "r") as f:
		label_dict = {v: k for k, v in eval(f.read()).items()}
	dim = (500, 500, 3)
	url1 = 'https://img.alicdn.com/bao/uploaded/i3/1752533979/O1CN01VT7bYk1fGQZ3Li5Pj_!!1752533979.jpg'  # GCOFFEE
	url2 = 'https://img.alicdn.com/bao/uploaded/i1/1724505357/TB2EvprhlDH8KJjSszcXXbDTFXa_!!1724505357.jpg'  # RTDC
	url3 = 'https://img.alicdn.com/bao/uploaded/i4/2549841410/O1CN01tbWrDO1MHp9vTP2t6_!!2549841410.jpg'  # RTDC
	url4 = 'https://img.alicdn.com/bao/uploaded/i3/1724505357/O1CN01SYl5Vs1pRYMcZdflg_!!1724505357.jpg'  # COFF
	url5 = 'https://img.alicdn.com/imgextra/i4/1124569589/O1CN010ePi4e2KhoYInmkIo_!!1124569589.jpg'  # GCOFF
	urls = [url1, url2, url3, url4, url5]
	for url in urls:
		url_predict_plot(url,'conv_7b')
	for url in urls:
		plot_box_predict(url, 'conv_7b')
	print('done')