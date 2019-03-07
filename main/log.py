import csv
import os
from shutil import copy

#csvData = [['Person', 'Age'], ['Peter', '22'], ['Jasmine', '21'], ['Sam', '24']]
count = 0

def create_file(month, day, hour, _min):
	# file_name = str(month) + '_' + str(day) + '_' + str(hour) + '_' + str(_min) + '.csv'
	file_name = 'log\\' + str(month) + '_' + str(day) + '_' + str(hour) + '_' + str(_min) + '.csv'
	config_file_name = 'config' + str(month) + '_' + str(day) + '_' + str(hour) + '_' + str(_min)
	cwd = os.getcwd()
	log_dir = cwd + '\\log'
	config_dir = cwd + '\\config'
	if not os.path.exists(cwd):
		os.makedirs(cwd)
	copy(config_dir, log_dir)
	os.chdir(log_dir)
	# print ("The dir is: " , os.listdir(os.getcwd()))
	os.rename("config", config_file_name)
	os.chdir(cwd)
	with open(file_name, 'w+') as csvFile:
		csvData = [['Generation', 'ID', 'fitness', 'max_fitness', 'mean_fitness']]
		# print("creating file.....")
		writer = csv.writer(csvFile)
		writer.writerows(csvData)
		csvFile.close()

	return file_name
		

def log_csv(file_name,generation, ID, fitness, maxfitness, meanfitness):
	csvData = [[str(generation), str(ID), str(fitness), str(maxfitness), str(meanfitness)]]
	global count
	count += 1
	# print("file name .............",file_name)
	with open(file_name, 'a') as csvFile:
	    writer = csv.writer(csvFile)
	    print("Writing", count)
	    writer.writerows(csvData)

	csvFile.close()
