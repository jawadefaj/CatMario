import neat
from game_running import run_game
# from neat_core import Neat
from game_running import open_game

# DO NOT remove the two program names here, comment out the one you don't need

# PROGRAM_NAME = 'Syobon Action (??????????)'
PROGRAM_NAME = 'Syobon Action (しょぼんのアクション)'



def eval_genomes(genomes, config):
	for genome_id, genome in genomes:
		network = neat.nn.FeedForwardNetwork.create(genome, config)
		genome.fitness = run_game(PROGRAM_NAME, network)


def run_library(config_file='config'):
	open_game()
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 config_file)

	population = neat.Population(config)

	# Run for up to n generations.
	winner = population.run(eval_genomes, 2)


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
	run()


if __name__ == '__main__':
	main()

