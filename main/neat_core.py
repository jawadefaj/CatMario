import neat
import os
import time
import pyautogui
from game_running import run_game


PROGRAM_NAME = 'Syobon Action (??????????)'


def eval_genomes(genomes, config):
	
	print("genomes ",len(genomes))
	for genome_id, genome in genomes:
		print("ID " , genome_id, len(genome.connections))
		network = neat.nn.FeedForwardNetwork.create(genome, config)
		#print("network " , network)
		genome.fitness = run_game(PROGRAM_NAME, network)
	print("Out of the loop")


def run(config_file):
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 config_file)

	population = neat.Population(config)

	# Run for up to 100 generations.
	winner = population.run(eval_genomes, 2)


	winner_net = neat.nn.FeedForwardNetwork.create(winner, config)


def open_game():
	cwd = os.getcwd()
	os.chdir("C:\\Users\\abjaw\\Downloads\\SyobonAction_rc2_win32bin")
	os.startfile("C:\\Users\\abjaw\\Downloads\\SyobonAction_rc2_win32bin\\OpenSyobonAction.exe")
	time.sleep(1.0)
	os.chdir(cwd)
	pyautogui.keyDown('enter')
	pyautogui.keyUp('enter')


def main():
	open_game();
	run('config')


if __name__ == '__main__':
	main()

