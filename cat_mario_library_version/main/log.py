import csv

#csvData = [['Person', 'Age'], ['Peter', '22'], ['Jasmine', '21'], ['Sam', '24']]
count = 0
def log_csv(generation, ID, fitness, maxfitness, meanfitness):
	csvData = [[str(generation), str(ID), str(fitness), str(maxfitness), str(meanfitness)]]
	global count
	count += 1
	with open('log.csv', 'a') as csvFile:
	    writer = csv.writer(csvFile)
	    print("Writing", count)
	    writer.writerows(csvData)

	csvFile.close()
