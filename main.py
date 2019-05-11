import numpy as np

import csv

from keras.models import Sequential, Model
from keras.layers import *
from keras.callbacks import ModelCheckpoint
from DataGenerator import DataGenerator
from BatchGenerator import BatchGenerator
from keras.optimizers import Adam
from keras import regularizers

from tensorflow.python.client import device_lib

print(device_lib.list_local_devices())

def main():
	params = {'dim' : (8,8),
	    	  'batch_size' : 512,
		  'n_classes' : 3,
		  'n_channels' : 7,
		  'shuffle' : True}

	#IDs, num_IDs = setIDs('IDs_shuf.csv')
	
	#pivot = int(np.floor(num_IDs*0.8))
	
	#partitions = {'train' : IDs[:pivot],
	#			  'validation' : IDs[pivot:]}

	#train_generator = DataGenerator(partitions['train'], **params)
	#validation_generator = DataGenerator(partitions['validation'], **params)

	#X, y = train_generator._DataGenerator__data_generation(partitions['train'][0:params['batch_size']])

	#print(X[0])

	'''
	model = Sequential()
	model.add(Conv2D(200,kernel_size=(4,4),data_format='channels_first',batch_size=params['batch_size'], batch_input_shape=(params['batch_size'],7,8,8)))
	model.add(Activation('relu'))
	model.add(Conv2D(300,kernel_size=(3,3), data_format='channels_first'))
	model.add(Activation('relu'))
	model.add(Conv2D(400,kernel_size=(2,2),data_format='channels_first'))
	model.add(Flatten())
	model.add(Dense(200))
	model.add(Dense(3))
	model.add(Activation('softmax'))
	'''

	inputs = Input(batch_shape=(params['batch_size'],7,8,8))
	y = res_block(y=inputs, nb_channels=32)
	y = res_block(y=y, nb_channels=32, _project_shortcut=False)
	y = res_block(y=y, nb_channels=32, _project_shortcut=False)
	y = res_block(y=y, nb_channels=32, _project_shortcut=False)
	y = res_block(y=y, nb_channels=64, _project_shortcut=True)	
	#y = Conv2D(32,kernel_size=(5,5),data_format='channels_first',batch_size=params['batch_size'],padding='same',batch_input_shape=(params['batch_size'],7,8,8))(inputs)
	#y = LeakyReLU()(y)
	y = Flatten()(y)
	y = Dense(128, activation=None)(y)
	#y = LeakyReLU()(y)
	outputs = Dense(3, activation='softmax', kernel_regularizer=regularizers.l2(0.00005))(y)

	model = Model(inputs=inputs, outputs=outputs)


	adam = Adam(lr=0.00005)
	model.compile(optimizer=adam,
		      loss='categorical_crossentropy',
                      metrics=['accuracy'])

	print(model.summary())

	filepath="models/mod6/model-{epoch:02d}-{val_acc:.3f}.hdf5"
	checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=False, mode='max')
	callbacks_list = [checkpoint]

	#filepath = "/data/models"
	#checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, mode='max')

	gen = BatchGenerator(batch_size=params['batch_size'], data_path='data/parsed_games_aug2/shuf')
	val_gen = BatchGenerator(batch_size=params['batch_size'], data_path='data/parsed_games_aug2/val')

	model.fit_generator(generator=gen.gen_boards(),
			    validation_data=val_gen.gen_boards(),
                            validation_steps=592,
			    steps_per_epoch=40622,
			    use_multiprocessing=True,
			    workers=2,
			    epochs=100,
			    verbose=1,
			    callbacks=callbacks_list)
	'''
	model.fit_generator(generator=train_generator,
			    validation_data=validation_generator,
			    use_multiprocessing=False,
			    workers=1,
			    epochs=100,
			    verbose=1,
			    callbacks=callbacks_list)
	'''

def res_block(y, nb_channels, _strides=(1,1), _project_shortcut=True):
	shortcut = y

	y = Conv2D(nb_channels, kernel_size=(4,4), strides=_strides, padding='same', data_format='channels_first')(y)
	y = BatchNormalization()(y)
	y = LeakyReLU()(y)

	y = Conv2D(nb_channels, kernel_size=(4,4), strides=(1,1), padding='same', data_format='channels_first')(y)
	y = BatchNormalization()(y)
	y = LeakyReLU()(y)

	if _project_shortcut:
		shortcut = Conv2D(nb_channels, kernel_size=(1,1), strides=_strides, padding='same', data_format='channels_first')(shortcut)

	y = add([shortcut, y])
	#y = LeakyReLU()(y)

	return y

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
