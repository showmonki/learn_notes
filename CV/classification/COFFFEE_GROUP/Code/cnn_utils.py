import matplotlib.pyplot as plt
import numpy as np
import requests
from io import BytesIO
from PIL import Image
import tensorflow as tf


def validate_performance(X_test,y_test, clf):
	y_pred_raw = clf.predict(X_test)
	y_pred = np.argmax(y_pred_raw, axis=1)
	y_test_label = np.argmax(y_test, axis=1)
	# y_pred_proba = np.max(y_pred_raw, axis=1)
	from sklearn import metrics
	print(metrics.classification_report(y_test_label, y_pred))
	print(metrics.confusion_matrix(y_test_label, y_pred))


def display_learning_curves(history,val=False):
	fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

	ax1.plot(history.history["loss"])
	if val:
		ax1.plot(history.history["val_loss"])
	ax1.legend(["train", "test"], loc="upper right")
	ax1.set_xlabel("Epochs")
	ax1.set_ylabel("Loss")

	ax2.plot(history.history["accuracy"])
	if val:
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


def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = requests.get(url)
	im = Image.open(BytesIO(resp.content))
	if im.mode != 'RGB':
		im = im.convert('RGB')
	return im

def convert_image(im, dim):
	image_resized = im.resize(dim[:2], Image.ANTIALIAS)
	temp_data = np.array(image_resized) / 255
	# 	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	# return the image
	return temp_data


def save_and_display_gradcam(img, heatmap, img_dim, cam_path="cam.jpg", alpha=0.4):
	import matplotlib.cm as cm
	# Rescale heatmap to a range 0-255
	heatmap = np.uint8(255 * heatmap)

	# Use jet colormap to colorize heatmap
	jet = cm.get_cmap("jet")

	# Use RGB values of the colormap
	jet_colors = jet(np.arange(256))[:, :3]
	jet_heatmap = jet_colors[heatmap]

	# Create an image with RGB colorized heatmap
	jet_heatmap = tf.keras.preprocessing.image.array_to_img(jet_heatmap)
	jet_heatmap = jet_heatmap.resize(img_dim)
	jet_heatmap = tf.keras.preprocessing.image.img_to_array(jet_heatmap)

	# Superimpose the heatmap on original image
	superimposed_img = jet_heatmap * alpha + img
	superimposed_img = tf.keras.preprocessing.image.array_to_img(superimposed_img)

	# Save the superimposed image
# 	superimposed_img.save(cam_path)
	# Display Grad CAM
	plt.imshow(superimposed_img)
	plt.show()