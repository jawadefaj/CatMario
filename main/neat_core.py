import neat
from game_running import run_game

# DO NOT remove the two program names here, comment out the one you don't need

# PROGRAM_NAME = 'Syobon Action (??????????)'
PROGRAM_NAME = 'Syobon Action (しょぼんのアクション)'


def eval_genomes(genomes, config):
	for genome_id, genome in genomes:
		network = neat.nn.FeedForwardNetwork.create(genome, config)
		genome.fitness = run_game(PROGRAM_NAME, network)


def run_library(config_file='config'):
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 config_file)

	population = neat.Population(config)

	# Run for up to n generations.
	winner = population.run(eval_genomes, 2)


	winner_net = neat.nn.FeedForwardNetwork.create(winner, config)


def run_non_library():
	

def run(lib=True):
	run_library() if lib else run_non_library()

def main():
	run()


if __name__ == '__main__':
	main()

