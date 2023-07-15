# coding: utf-8

import tensorflow as tf


class TCNNConfig(object):
	"""CNN-Hyperparameters"""
	td_nsplit = 100  # Number of splits of each training data set (TD) for training, eliminates the RAM memory error for big data sets
	embedding_dim = 128  # Embedding dimension
	# Sequence length in characters gives the max length of each training example that is considered by the model
	seq_length = 50  # Previously set to 30
	num_filters = 512  # Number of conv kernels/filters: *16,32,64,128,256,..
	kernel_size = 3  # The length of the 1D convolution window, value range 2-5

	vocab_size = 10000  # Max vocabulary size; previously set to 50k
	hidden_dim = 128  # Number of neurons in the fully connected layer

	# Probabilistically drop out nodes in the network, this is used as a simple and effective regularization method.
	# For further details, please refer to:
	# https://machinelearningmastery.com/dropout-for-regularizing-deep-neural-networks/,
	# http://jmlr.org/papers/v15/srivastava14a.html
	# A common value is a probability of 0.5 for retaining the output of each node in a hidden layer
	# and a value close to 1.0, such as 0.8, for retaining inputs from the visible layer.
	dropout_keep_prob = 0.5  # Dropout probability to keep nodes

	# Learning rate controls how much we are adjusting the weights of our network w.r.t. the loss gradient.
	# The lower the value, the slower we move along the downward slope.
	# For further details, please refer to:
	# https://towardsdatascience.com/understanding-learning-rates-and-how-it-improves-performance-in-deep-learning-d0d4059c1c10
	learning_rate = 1e-3

	# The batch size defines the number of samples (training examples in a TD) that will be propagated through the network
	batch_size = 10240  # For small data sets, set to 1024
	# An epoch means one complete - forward and backward - pass of the entire TD through the network.
	# Usually, one epoch contains several / many iterations.
	# The number of iterations per epoch depends on the number of training examples and specified batch size.
	# For instance, if we have 10 million examples and a batch size of 10k, an epoch will contain 1000 iterations
	num_epochs = 5  # Defines how many times the entire TD is passed forward and backward through the network.
	# The maximum number of iterations that we allow for no improvement in training accuracy.
	max_no_improve_iters = 10000

	print_per_batch = 100  # Print batch of the size of 100 (default)
	save_per_batch = 100  # Number of batches to save learning into TensorBoard

	# Specifies the number of the top k predictions returned for each prediction example (item description).
	top_k = 1


class TextCNN(object):
	"""
	A CNN for text classification.
	Uses an embedding layer, followed by a convolutional, max-pooling and softmax layer.
	"""

	def __init__(self, num_classes, config):
		self.config = config
		self.num_classes = num_classes
		self.input_x = tf.placeholder(tf.int32, [None, self.config.seq_length], name='input_x')
		self.input_y = tf.placeholder(tf.float32, [None, self.num_classes], name='input_y')
		self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')
		self.cnn()

	def cnn(self):
		"""
		If a TensorFlow operation has both CPU and GPU implementations,
		the GPU devices will be given priority when the operation is assigned to a device.
		On a typical system, there are multiple computing devices.
		In TensorFlow, the supported device types are CPU and GPU. They are represented as strings.

		For example:
			"/cpu:0": The CPU of your machine.
			"/device:GPU:0": The GPU of your machine, if you have one.
			"/device:GPU:1": The second GPU of your machine, etc.
		"""
		with tf.device('/cpu:0'):
			"""
			An embedding is a mapping from discrete objects, such as words, to vectors of real numbers. 
			For example, a 300-dimensional embedding for word/character could include:
				绿:  (0.01359, 0.00075997, 0.24608, ..., -0.2524, 1.0048, 0.06259)
				blues:  (0.01396, 0.11887, -0.48963, ..., 0.033483, -0.10007, 0.1158)
			'embedding_inputs' will contain the embeddings for all words/character in the vocabulary.
			"""
			embedding = tf.get_variable('embedding', [self.config.vocab_size, self.config.embedding_dim])
			embedding_inputs = tf.nn.embedding_lookup(embedding, self.input_x)

		with tf.name_scope("cnn"):
			"""
			In general, a CNN will perform a series of convolutions and pooling operations during which the features are detected.
			conv layer: the convolution is performed on the input data with the use of
			a filter or kernel (these terms are used interchangeably) to produce a feature map.

			CONV layer：Functional interface for 1D convolution layer
			Functional interface for 1D convolution layer (e.g. temporal convolution).

			The originally used function tf.layers.conv1d() is now deprecated.
			Instructions for updating: Use tf.keras.layers.Conv1D instead.
			"""
			# conv = tf.keras.layers.Conv1D(embedding_inputs, self.config.num_filters, self.config.kernel_size, name='conv')
			conv = tf.layers.conv1d(embedding_inputs, self.config.num_filters, self.config.kernel_size, name='conv')

			"""
			After a convolution layer, it is common to add a pooling layer in between CNN layers. 
			The function of pooling is to continuously reduce the dimensionality of the network, i.e. the number of parameters
			and computation performed in the network. This shortens the training time and controls overfitting.
			Here, we use the global max pooling layer.
			"""
			gmp = tf.reduce_max(conv, reduction_indices=[1], name='gmp')
			# gmp = tf.layers.max_pooling1d(conv,self.config.pool_size,self.config.strides,name='gmp')

			"""
			 After the convolution and pooling layers, our classification part consists of a few fully connected layers. 
			 Neurons in a fully connected layer have full connections to all the activations in the previous layer.
			 This part is in principle the same as a regular Neural Network.
			"""
		with tf.name_scope("score"):
			fc = tf.layers.dense(inputs=gmp, units=self.config.hidden_dim, name='fc1')

			"""
			# Add dropout 
			Dropout is a regularization technique for reducing overfitting in NNs by preventing complex co-adaptations on training data. 
			It is a very efficient way of performing model averaging with neural networks.

			Details:
			1/ At every training step, every neuron (including the input neurons, but always excluding the output neurons) has a probability p of 
			being temporarily “dropped out,” meaning it will be entirely ignored during this training step, but it may be active during the next step.
			The hyperparameter p is called the dropout rate, and it is typically set between 10% and 50%: closer to 20–30% in recurrent neural nets, 
			and closer to 40–50% in convolutional neural networks. After training, neurons don’t get dropped anymore.
			2/ Important technicality. Suppose p = 50%, in which case during testing a neuron would be connected to twice as many input neurons as 
			it would be (on average) during training. To compensate for this fact, we need to multiply each neuron’s input connection weights by 0.5 after training. 
			If we don’t, each neuron will get a total input signal roughly twice as large as what the network was trained on and will be unlikely to perform well. 
			More generally, we need to multiply each input connection weight by the keep probability (1 – p) after training. Alternatively, we can divide 
			each neuron’s output by the keep probability during training (these alternatives are not perfectly equivalent, but they work equally well).
			3/ We can usually apply dropout only to the neurons in the top 1 to 3 layers (excluding the output layer).
			4/ Since dropout is only active during training, comparing the training loss and the validation loss can be misleading. 
			In particular, a model may be overfitting the training set and yet have similar training and validation losses.
			So make sure to evaluate the training loss without dropout (e.g., after training).
			5/ If you want to regularize a self-normalizing network based on the SELU activation function (Scaled Exponential LU), you should use alpha dropout: 
			this is a variant of dropout that preserves the mean and standard deviation of its inputs (it was introduced in the same paper as SELU, 
			as regular dropout would break self-normalization).

			Warning:
			Contrib module (https://www.tensorflow.org/versions/r1.15/api_docs/python/tf/contrib) contains volatile or experimental code.
			The tf.contrib module is not included in TensorFlow 2. 
			Many of its submodules have been integrated into TensorFlow core, or spun-off into other projects like tensorflow_io, or tensorflow_addons.
			Links:
			https://github.com/tensorflow/io
			https://github.com/tensorflow/addons
			https://www.tensorflow.org/guide/migrate

			Use tf.keras.layers.Dropout instead.
			"""
			fc = tf.contrib.layers.dropout(fc, self.keep_prob)

			# Apply nonlinearity with Rectified linear unit (ReLU) and softmax activiation functions
			fc = tf.nn.relu(fc)
			# Add a fully-connected output layer
			self.logits = tf.layers.dense(inputs=fc, units=self.num_classes, name='fc2')
			# Store the index of the class with the highest probability
			"""
			tf.argmax() returns the index with the largest value across axes of a tensor.
			axis: A Tensor, must be one of the following types: int32, int64. int32 or int64, 
			must be in the range [-rank(input), rank(input)). 
			Describes which axis of the input Tensor to reduce across. For vectors, use axis = 0.
			"""
			self.y_pred_cls = tf.argmax(input=tf.nn.softmax(self.logits), axis=1)
			# We need to use the softmax function again to get the results (class probabilities) from the output layer
			self.y_prob_cls = tf.nn.softmax(self.logits, name="softmax_probs_class")

		# Define loss and optimizer
		with tf.name_scope("optimize"):
			# Computes softmax cross-entropy between logits and labels.
			# The originally used function 'tf.nn.softmax_cross_entropy_with_logits' is deprecated and will be removed in the future.
			# Hence, it was replaced with its newer version. No change in arguments and their values as well as the output returned.
			cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.logits, labels=self.input_y)
			# Please note that np.mean has a dtype parameter that could be used to specify the output type. By default this is dtype=float64.
			# On the other hand, tf.reduce_mean has an aggressive type inference from input_tensor, i.e. integer vs float value.
			self.loss = tf.reduce_mean(cross_entropy)

			"""
			Optimizer that implements the Adam (adaptive moment estimation) algorithm.
			For details, see https://arxiv.org/abs/1412.6980
			optimizer = tf.train.AdamOptimizer().minimize(loss)
			The default parameter values：learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-08, 
			which are fine for most circumstances.
			"""
			self.optim = tf.train.AdamOptimizer(learning_rate=self.config.learning_rate).minimize(self.loss)

		# Score the model
		with tf.name_scope("accuracy"):
			correct_pred = tf.equal(tf.argmax(self.input_y, 1), self.y_pred_cls)
			self.acc = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

