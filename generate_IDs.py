import os
import csv

path = './data/npfiles'

files = os.listdir(path)

with open('IDs.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	for i, ID in enumerate(files):
		ID = ID[:-4]

		if(i%1000==0):
			print(i*100/(39000*50))

		writer.writerow([ID])

