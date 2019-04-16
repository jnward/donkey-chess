import keras
import tensorflow as tf
import numpy as np
import csv
from os import walk

class BatchGenerator():

	def __init__(self, list_IDs=None, batch_size=128, dim=(8,8), n_channels = 7, n_classes=3, shuffle=True):
		self.dim = dim
		self.batch_size = batch_size
		#self.labels = labels
		self.list_IDs = list_IDs
		self.n_channels = n_channels
		self.n_classes = n_classes
		self.shuffle = shuffle

	def gen_boards(self):
		for _, _, file in walk('data/parsed_games'):
			files = file
			break
		print(files)
		#with open('parsedGames_shuf.csv', 'r') as file:
		#file = open('parsedGames_small.csv', 'r')
		
		while True:
			#reader = csv.reader(file, delimiter=',')

			count = 0
			boards = []

			'''
			for i, board in enumerate(reader):
				board = tf.convert_to_tensor(board, dtype=tf.int8)
				boards.append(i)
				count += 1

				if count >= 16:
					yield boards
					boards = []
					count = 0
			'''
			for file_name in files:
				file = open('data/parsed_games/'+file_name)
				print("Reading from file: " + file_name)
				reader = csv.reader(file, delimiter=',')
				X = np.empty((self.batch_size, self.n_channels, *self.dim), dtype=int)
				y = np.empty((self.batch_size), dtype=int)
				steps = 0
				count = 0
				for board in reader:
					datum = np.array([int(string) for string in board[1:]])
					count += 1
					#X[i,] = datum[1:]
					X[count-1,] = np.reshape(datum, (self.n_channels, self.dim[0], self.dim[1]))
					y[count-1] = int(board[0])+1
					if steps >= 15:
						print("Break")
						file.close()
						break
						#file = open('data/parsed_games/'+files[0])
						#file.seek(0)
						#steps = 0

					if count >= self.batch_size:
						yield X, keras.utils.to_categorical(y, num_classes=self.n_classes)
						steps += 1
						count = 0
						X = np.empty((self.batch_size, self.n_channels, *self.dim), dtype=int)
						y = np.empty((self.batch_size), dtype=int)



		#return X, y
		#return X, keras.utils.to_categorical(y, num_classes=self.n_classes)



#gen = BatchGenerator()

#for board in gen.gen_boards():
#	print(board)

