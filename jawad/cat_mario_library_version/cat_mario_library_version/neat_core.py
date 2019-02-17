import neat
from game_running import run_game

PROGRAM_NAME = 'Syobon Action (??????????)'


def eval_genomes(genomes, config):
	for genome_id, genome in genomes:
		network = neat.nn.FeedForwardNetwork.create(genome, config)
		genome.fitness = run_game(PROGRAM_NAME, network)


def run(config_file):
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 config_file)

	population = neat.Population(config)

	# Run for up to 100 generations.
	winner = population.run(eval_genomes, 100)

	winner_net = neat.nn.FeedForwardNetwork.create(winner, config)


def main():
	run('config')


if __name__ == '__main__':
	main()

