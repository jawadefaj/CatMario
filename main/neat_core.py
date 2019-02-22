import neat
from game_running import run_game
import pyautogui
import os
import time

PROGRAM_NAME = 'Syobon Action (??????????)'


def eval_genomes(genomes, config):
	for genome_id, genome in genomes:
		network = neat.nn.FeedForwardNetwork.create(genome, config)
		genome.fitness = run_game(PROGRAM_NAME, network)
		# print("Genome fitness")
		# print(genome.fitness)


def run(config_file):
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 config_file)

	population = neat.Population(config)
	open_game()
	# Run for up to 100 generations.
	winner = population.run(eval_genomes, 100)

	winner_net = neat.nn.FeedForwardNetwork.create(winner, config)


def main():
	run('config')


def open_game():
	cwd = os.getcwd()
	os.chdir("C:\\Users\\abjaw\\Downloads\\SyobonAction_rc2_win32bin")
	os.startfile("C:\\Users\\abjaw\\Downloads\\SyobonAction_rc2_win32bin\\OpenSyobonAction.exe")
	time.sleep(1.0)
	os.chdir(cwd)
	pyautogui.keyDown('enter')
	pyautogui.keyUp('enter')

if __name__ == '__main__':
	main()

