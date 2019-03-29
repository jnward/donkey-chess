import numpy as np

import csv

from keras.models import Sequential
from keras.layers import *
from DataGenerator import DataGenerator

def main():
	params = {'dim' : (8,8),
			  'batch_size' : 256,
			  'n_classes' : 3,
			  'n_channels' : 7,
			  'shuffle' : True}

	IDs, num_IDs = setIDs('IDs_shuf.csv')

	pivot = int(np.floor(num_IDs*0.8))
	
	partitions = {'train' : IDs[:pivot],
				  'validation' : IDs[pivot:]}

	train_generator = DataGenerator(partitions['train'], **params)
	validation_generator = DataGenerator(partitions['validation'], **params)

	#X, y = train_generator._DataGenerator__data_generation(partitions['train'][0:params['batch_size']])

	#print(X[0])


	model = Sequential()
	model.add(Conv2D(32,kernel_size=(4,4),data_format='channels_first',batch_size=params['batch_size'], batch_input_shape=(params['batch_size'],7,8,8)))
	model.add(Activation('relu'))
	model.add(Conv2D(64,kernel_size=(2,2), data_format='channels_first'))
	model.add(Flatten())
	model.add(Dense(3))
	model.add(Activation('softmax'))
	model.compile(optimizer='adam',
				  loss='categorical_crossentropy',
				  metrics=['accuracy'])

	print(model.summary())

	filepath = "/data/models"
	checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, mode='max')

	model.fit_generator(generator=train_generator,
						validation_data=validation_generator,
						use_multiprocessing=True,
						workers=16,
						epochs=10,
						verbose=1,
						callbacks=[checkpoint])




def setIDs(filename):
	num_IDs = 0

	with open(filename, 'r') as ID_csv:
		IDreader = csv.reader(ID_csv, delimiter=',')
		for i, ID in enumerate(IDreader):
			num_IDs = i
		num_IDs += 1

	IDs = np.empty(num_IDs, dtype=int)
	with open(filename, 'r') as ID_csv2:
		IDreader2 = csv.reader(ID_csv2, delimiter=',')
		for i, ID in enumerate(IDreader2):
			IDs[i] = ID[0]
			if i%100000 == 0:
				print(i*100/num_IDs, i, ID[0])

	return IDs, num_IDs

if __name__ == '__main__':
	main()