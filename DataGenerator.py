import numpy as np
import keras

class DataGenerator(keras.utils.Sequence):

	def __init__(self, list_IDs, batch_size=128, dim=(8,8), n_channels = 7, n_classes=3, shuffle=True):
		self.dim = dim
		self.batch_size = batch_size
		#self.labels = labels
		self.list_IDs = list_IDs
		self.n_channels = n_channels
		self.n_classes = n_classes
		self.shuffle = shuffle
		self.on_epoch_end()

	def __len__(self):
		return int(np.floor(len(self.list_IDs)/self.batch_size))

	def __getitem__(self, index):

		indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

		list_IDs_temp = [self.list_IDs[k] for k in indexes]

		X, y = self.__data_generation(list_IDs_temp)

		return X, y

	def on_epoch_end(self):
		self.indexes = np.arange(len(self.list_IDs))
		if self.shuffle:
			np.random.shuffle(self.indexes)

	def __data_generation(self, list_IDs_temp):

		X = np.empty((self.batch_size, self.n_channels, *self.dim), dtype=int)
		y = np.empty((self.batch_size), dtype=int)

		for i, ID in enumerate(list_IDs_temp):

			datum = np.load('data/npfiles/%s.npy'%(str(ID)))
			#X[i,] = datum[1:]
			X[i,] = np.reshape(datum[1:], (self.n_channels, self.dim[0], self.dim[1]))
			y[i] = int(datum[0])+1


		#return X, y
		return X, keras.utils.to_categorical(y, num_classes=self.n_classes)
