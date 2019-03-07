

class A:
	a = 'a'

class B:
	a = A.a
	def __init__(self):
		# self.Cs = initialize_Cs()
		if 'a' == A.a:
			A.a = 'aa'


class C:
	def __init__(self, connection_pair):
		self.connection = connection_pair
		id_set = check_idset(connection_pair)
		self.id = None

def main():
	if -1 in range(4):
		print('yes')

if __name__ == '__main__':


	main()

