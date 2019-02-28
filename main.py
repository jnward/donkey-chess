import numpy as np

import csv

from keras.models import Sequential
import DataGenerator

def main():
	params = {'dim' : (8,8),
			  'batch_size' : 128,
			  'n_classes' : 3,
			  'n_channels' : 7,
			  'shuffle' : True}

	IDs, num_IDs = setIDs('IDs_shuf.csv')

	pivot = int(np.floor(num_IDs*0.8))
	
	partitions = {'train' : IDs[:pivot],
				  'validation' : IDs[pivot:]}

	print(num_IDs)
	print(partitions.get('train'), partitions['validation'])
	print(partitions['train'][-2:], partitions['validation'][0:2])


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