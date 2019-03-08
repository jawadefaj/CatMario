import neat
from game_running import run_game
# from neat_core import Neat
from game_running import open_game
from game_running import kill_game
from game_running import find_window
from log import log_csv
from log import create_file
import time
import pickle
import datetime

# from neat.species import DefaultSpeciesSet


# DO NOT remove the two program names here, comment out the one you don't need

PROGRAM_NAME = 'Syobon Action (??????????)'
#PROGRAM_NAME = 'Syobon Action (しょぼんのアクション)'
LOG_FILE_NAME = ''
TOTAL_GENERATION = 100
CUR_GENERATION = 0

def eval_genomes(genomes, config):
	generation_fitness = 0
	global CUR_GENERATION
	CUR_GENERATION += 1
	maxfitness = 0
	for genome_id, genome in genomes:
		# print("Species ID " ,neat.DefaultSpeciesSet.get_species_id((genome.key, 0)))
		open_game()
		time.sleep(2.0)
		network = neat.nn.FeedForwardNetwork.create(genome, config)
		# print("create RecurrentNetwork")
		genome.fitness = run_game(PROGRAM_NAME, network)
		log_csv(LOG_FILE_NAME, CUR_GENERATION, genome_id, genome.fitness, 0, 0 )
		maxfitness = max(genome.fitness, maxfitness)
		generation_fitness += genome.fitness
		with open(r'C:\Users\abjaw\Documents\GitHub\CatMario\main\dump\%s.pkl' %(genome_id), 'wb') as output:
			pickle.dump(genome, output, pickle.HIGHEST_PROTOCOL)
		# print(genome_id, genome.fitness, genome.key, len(genome.nodes), len(genome.connections))
		if find_window(PROGRAM_NAME):
			kill_game()

	meanfitness = generation_fitness/len(genomes)
	log_csv(LOG_FILE_NAME, CUR_GENERATION, 0, 0, maxfitness, meanfitness)



def run_library(config_file='config'):
	# open_game()
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 config_file)

	population = neat.Population(config)

	# Run for up to n generations.
	winner = population.run(eval_genomes, TOTAL_GENERATION)


	winner_net = neat.nn.FeedForwardNetwork.create(winner, config)


def load_parameters(config_file_name):
	"""

	:param config_file_name: filename
	:type config_file_name: str
	:return: parameters
	:rtype: dict
	"""

	return parameters


# def run_non_library(config_file_name):
# 	#todo: we need to find a way to load parameters
# 	parameters = load_parameters(config_file_name)
#
# 	n = Neat(parameters)

# 	while n.generation < n.MAX_GEN:
# 		for genome in n.population:
# 			genome.fitness = run_game(PROGRAM_NAME, genome)
# 		n.evolve()
# 		n.generation += 1

def run(lib=True):
	run_library() if lib else run_non_library()


def main():
	now = datetime.datetime.now()
	global LOG_FILE_NAME
	LOG_FILE_NAME = create_file(now.month, now.day, now.hour, now.minute)
	# print(LOG_FILE_NAME)
	run()
	

if __name__ == '__main__':
	main()

