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


pickle_file = r'C:\Users\abjaw\Documents\GitHub\CatMario\main\dump\612.pkl'
PROGRAM_NAME = 'Syobon Action (??????????)'


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 'config')

genome = pickle.load(open(pickle_file, "rb"))
open_game()
time.sleep(2.0)
network = neat.nn.FeedForwardNetwork.create(genome, config)
genome.fitness = run_game(PROGRAM_NAME, network)
# print(genome)
