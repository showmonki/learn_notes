import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import backend as K
import matplotlib.pyplot as plt


def grad_cam(input_model, image, category_index, layer_index):
	"""
	GradCAM method for visualizing input saliency.

	Args:
		input_model (Keras.model): model to compute cam for
		image (tensor): input to model, shape (1, H, W, 3)
		cls (int): class to compute cam with respect to
		layer_name (str): relevant layer in model
		H (int): input height
		W (int): input width
	Return:
		cam ()
	"""
	cam = None

	### START CODE HERE (REPLACE INSTANCES OF 'None' with your code) ###

	# 1. Get placeholders for class output and last layer
	# Get the model's output
	output_with_batch_dim = input_model.output

	# Remove the batch dimension
	output_all_categories = output_with_batch_dim[0]

	# Retrieve only the disease category at the given category index
	y_c = output_all_categories[category_index]

	# Get the input model's layer specified by layer_name, and retrive the layer's output tensor
	spatial_map_layer = input_model.get_layer(index=layer_index).output

	# 2. Get gradients of last layer with respect to output

	# get the gradients of y_c with respect to the spatial map layer (it's a list of length 1)
	# with GradientTape() as g_tape:
	# 	grads_l = g_tape.gradients(y_c, spatial_map_layer)
	import tensorflow as tf
	tf.compat.v1.disable_eager_execution()
	grads_l = K.gradients(y_c, spatial_map_layer)

	# Get the gradient at index 0 of the list
	grads = grads_l[0]

	# 3. Get hook for the selected layer and its gradient, based on given model's input
	# Hint: Use the variables produced by the previous two lines of code
	spatial_map_and_gradient_function = K.function([input_model.input], [spatial_map_layer, grads])

	# Put in the image to calculate the values of the spatial_maps (selected layer) and values of the gradients
	spatial_map_all_dims, grads_val_all_dims = spatial_map_and_gradient_function([image])

	# Reshape activations and gradient to remove the batch dimension
	# Shape goes from (B, H, W, C) to (H, W, C)
	# B: Batch. H: Height. W: Width. C: Channel
	# Reshape spatial map output to remove the batch dimension
	spatial_map_val = spatial_map_all_dims[0]

	# Reshape gradients to remove the batch dimension
	grads_val = grads_val_all_dims[0]

	# 4. Compute weights using global average pooling on gradient
	# grads_val has shape (Height, Width, Channels) (H,W,C)
	# Take the mean across the height and also width, for each channel
	# Make sure weights have shape (C)
	weights = np.mean(grads_val, axis=(0, 1))

	# 5. Compute dot product of spatial map values with the weights
	cam = np.dot(spatial_map_val, weights)

	### END CODE HERE ###

	# We'll take care of the postprocessing.
	H, W = image.shape[1], image.shape[2]
	cam = np.maximum(cam, 0)  # ReLU so we only get positive importance
	cam = cv2.resize(cam, (W, H), cv2.INTER_NEAREST)
	cam = cam / cam.max()

	return cam


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
	pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

	# We multiply each channel in the feature map array
	# by "how important this channel is" with regard to the top predicted class
	# then sum all the channels to obtain the heatmap class activation
	last_conv_layer_output = last_conv_layer_output[0]
	heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
	heatmap = tf.squeeze(heatmap)

	# For visualization purpose, we will also normalize the heatmap between 0 & 1
	heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
	return heatmap.numpy()

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
	superimposed_img = tf.keras.preprocessing.image.array_to_img(superimposed_img[0])

	# Save the superimposed image
	superimposed_img.save(cam_path)
	# Display Grad CAM
	plt.imshow(superimposed_img)
	plt.show()
