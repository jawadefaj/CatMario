import speciation
import numpy as np

class Neat:

	INPUT_NUM = 169
	OUTPUT_NUM = 4
	generation = 1

	##-----------parametres for weight generation--------##
	WEIGHT_MAX = 10
	WEIGHT_MIN = -10
	WEIGHT_MEAN = 0
	WEIGHT_DEVIATION = 4
	WEIGHT_MUTATION_RATE = 0.5
	WEIGHT_REPLACE_RATE = 0
	##-----------parametres for weight generation--------##	

	max_node_inno = INPUT_NUM + OUTPUT_NUM - 1
	max_conn_inno = OUTPUT_NUM * INPUT_NUM - 1
	bias_weight = {} # we don't really need bias connection, imagine we
	# have one bias node only, also avoid both node and conn innovation numbers
	speciations = []

	def initialize_nodes():
		# I use (a, b) to represent nodes because each new node is created
		# between two old nodes and a,b are the two old nodes that the new node
		# depends. Hence for initial nodes, I just give them (a, a) where a is
		# there node innovation number.

		# In my encoding, output nodes have innovation number 0 to 3(left, right,
		# up, down) and the input node have innovation number 4 to 172

		nodes = {}
		for i in range(INPUT_NUM + OUTPUT_NUM):
			nodes[(i, i)] = i
		return nodes

	def initialize_connections():
		# notice that the index of connections IS the innovation number
		connections = {}
		for output_node_i in range(OUTPUT_NUM):
			for j in range(INPUT_NUM):
				input_node_i = j + OUTPUT_NUM
				connections[(input_node_i, output_node_i)] = output_node_i * Neat.INPUT_NUM + j
		return connections

	node_inno_nums = initialize_nodes()  # storing existed nodes
	conn_inno_nums = initialize_connections()  # storing existed conn

	#------------class variables above-----------------------------------

	def __init__(self, max_gen, max_pop, top_n_spec, weight_):
		self.MAX_GEN = max_gen
		self.MAX_POP = max_pop
		self.population = self.initialize_population()
		self.top_n_speciation = top_n_spec  # how many top genomes keep in the speciation during evolution.

	def initialize_population(self):
		population = []
		for i in range(self.MAX_POP):
			genome = Genome()
			population.append(genome)
		return population

	def initialize_speciation(self):
		# Todo: initialize speciation
		"""

		:return: list of speciations
		:rtype: list of list of Genomes
		"""



		return speciated_population

	def calculate_adjusted_fitness(self):
		for speciation_id, speciation in enumerate(Neat.speciations):
			speciation_size = len(speciation)

	def evolve(self):
		if self.generation == 1:
			Neat.speciations = self.initialize_speciation()
			# Todo: initial_speciation first

		baby_quota = self.calculated_adjusted_fitness()

		# Todo:calculate adjusted weights, get the proportion of offsprings for each species
		# Todo: mutate/crossover in each species for getting offsprings
			# Todo:update self.connections and self.nodes during mutation(important)
		# Todo: re-speciation:
		# write the above functions in speciation.py(except the mutation/crossover part)


class Genome:
	def __init__(self, genes=None):
		# self.genes for easier crossover(order by innovation number)
		# self.connections for easier computing outputs, details in reorder function

		if genes:
			self.genes = genes  # after first generation
		else:
			self.genes = self.initialize_genes()  # first generation
		self.fitness = None
		# self.connections = self.reorder_connections([gene.connection for gene in self.genes])

	# def reorder_connections(self, connections):
	# 	# Todo: connections should be ordered such that the take_value_node's innovation number
	# 	# Todo:	increases e.g. (5, 0), (6, 0), (7, 1), (8, 3)....
	# 	# Todo:	keeping this structure is important for calculating output faster
	# 	return new_connections

	def get_output(self, input_list):
		# Todo: basically we are computing the NN here.
		"""

		:param input_list: input from CV_unit
		:type input_list: list of float
		:return: output for determine actions
		:rtype: list of float
		"""
		# in_nodes are the one GETTING values from other nodes including output_nodes
		# out_nodes are the one GIVING values includes input_nodes
		in_nodes = [node_inno for node_inno in Neat.node_inno_nums.values() if value in range(4)]
		in_out_total = Neat.INPUT_NUM + Neat.OUTPUT_NUM
		if len(Neat.node_inno_nums) > in_out_total:
			in_nodes += [node_inno for node_inno in Neat.node_inno_nums.values() if value in range(in_out_total, len(Neat.node_inno_nums))]

		# for in_node, out_node in self.connections:

		return output_list

	def initialize_genes(self):
		# for new initial genomes only, not for the ones after first generation
		""""
		:return: list of genes, 4 * 169 connections with random weights within some range
		:rtype: list of genes

		"""
		genes = []
		for to_node_n in range(OUTPUT_NUM):
			for i in range(INPUT_NUM):
				from_node_n = i + 4
				weight = np.random.normal(WEIGHT_MEAN, WEIGHT_DEVIATION) * (WEIGHT_MAX - WEIGHT_MEAN) + WEIGHT_MIN
				gene = Gene((from_node_n, to_node_n), weight)
				genes.append(gene)
		return genes


class Gene:
	def __init__(self, connection, weight):
		self.connection = connection
		self.conn_inno = Neat.connections[connection] # assume we have checked the gene in mutation
		self.disabled = False
		self.weight = weight


