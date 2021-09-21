from tensorflow import keras


class TCNNConfig(object):
	"""CNN-Hyperparameters"""
	td_nsplit = 100
	embedding_dim = 128
	seq_length = 50  # 原50， 暂时修改，因为tfidf
	num_filters = 512
	kernel_size = 3

	vocab_size = 10000
	hidden_dim = 128

	dropout_keep_prob = 0.5
	learning_rate = 1e-3

	batch_size = 10240
	num_epochs = 5
	max_no_improve_iters = 10000

	print_per_batch = 100
	save_per_batch = 100

	top_k = 1


class CnnBau(object):

	def __init__(self, config, num_classes):
		self.num_classes = num_classes
		self.model = self.load_model()
		self.config = config

	def load_model(self):
		inputs = keras.Input(shape=(self.config.seq_length,), name='model_input')

		x = keras.layers.Embedding(input_dim=self.config.vocab_size, output_dim=self.config.embedding_dim, input_length=self.config.seq_length)(inputs)
		x = keras.layers.Conv1D(filters=self.config.num_filters, kernel_size=self.config.kernel_size, name='conv', activation='relu')(x)
		x = keras.layers.Dropout(self.config.dropout_keep_prob, name="drp")(x)
		x = keras.layers.GlobalMaxPool1D(name='gmp')(x)
		x = keras.layers.Dense(self.config.hidden_dim, activation='relu', name='fc1')(x)
		x = keras.layers.Dense(self.config.hidden_dim, name='fc2')(x)
		outputs = keras.layers.Dense(self.num_classes, activation='softmax')(x)

		model = keras.Model(inputs, outputs, name='ec_bau_model')
		model.compile(optimizer=keras.optimizers.Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
		return model


class CNNKeras(object):

	def __init__(self, config):
		self.config = config
		self.num_filters = config.num_filters
		self.kernel_size = config.kernel_size
		self.model = self.load_model()

	def load_model(self):
		inputs = keras.Input(shape=(self.config.seq_length,), name='model_input')

		x = keras.layers.Embedding(input_dim=self.config.vocab_size, output_dim=self.config.embedding_dim, input_length=self.config.seq_length)(inputs)
		x = keras.layers.Conv1D(filters=self.num_filters,kernel_size=self.kernel_size,name='conv1_1',padding='same',activation='relu')(x)
		x = keras.layers.Conv1D(filters=self.num_filters,kernel_size=1,name='conv1_2',activation='relu')(x)
		x = keras.layers.MaxPool1D(name='mp1')(x)
		x = keras.layers.BatchNormalization(name='bn1')(x)
		# x = keras.layers.Dropout(dropout_rate, name="drp1")(x)

		x = keras.layers.Conv1D(filters=self.num_filters, kernel_size=self.kernel_size, name='conv2_1',padding='same',activation='relu')(x)
		x = keras.layers.Conv1D(filters=self.num_filters, kernel_size=1, name='conv2_2',activation='relu')(x)
		x = keras.layers.MaxPool1D(name='mp2')(x)
		x = keras.layers.BatchNormalization(name='bn2')(x)
		# x = keras.layers.Dropout(dropout_rate, name="drp2")(x)

		x = keras.layers.Conv1D(filters=self.num_filters, kernel_size=self.kernel_size, name='conv3',padding='same',activation='relu')(x)
		x = keras.layers.Conv1D(filters=self.num_filters, kernel_size=1, name='conv3_2',activation='relu')(x)
		x = keras.layers.MaxPool1D(name='mp3')(x)
		x = keras.layers.BatchNormalization(name='bn3')(x)
		# x = keras.layers.Dropout(dropout_rate, name="drp3")(x)

		x = keras.layers.Dense(self.config.hidden_dim, activation='relu')(x)
		x = keras.layers.GlobalMaxPool1D(name='gmp')(x)
		outputs = keras.layers.Dense(self.config.num_classes, activation='softmax')(x)
		model = keras.Model(inputs, outputs, name='keras_model')

		model.compile(optimizer=keras.optimizers.Adam(),loss='categorical_crossentropy', metrics=['accuracy'])
		return model

