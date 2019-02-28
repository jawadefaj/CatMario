# # import neat_core.Neat
#
#
# # function performed in mutation phase
# def check_gene(self, connection):
# 	innovation_number = Neat.connections.get(connection)
# 	if innovation_number:
# 		return innovation_number
# 	else:
# 		Neat.max_conn_inno += 1
# 		Neat.connections[connection] = Neat.max_conn_inno
