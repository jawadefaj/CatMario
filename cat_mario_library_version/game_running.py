from input import capture_input
import neat.nn.feed_forward  # for the 'network' parameter
from output import press_keys
import win32gui
import time

DIS_UPDATE_THRESHOLD = 0.05
ACTION_SELECT_THRESHOLD = 0.6


def run_game(program_name, network):
	# todo: open the game program

	focus_program(program_name)

	# initialization
	cat_is_dead = False
	max_fitness = 0
	last_keys_pressed = [0, 0, 0, 0]  # left, right , up , down, 0/1: not/pressed
	last_frame_timestamp = 0
	cat_travel_dis = 0  # subtract when cat moves left, increment when cat moves right
	last_img_obj_corners = []

	while not cat_is_dead:
		input_matrix, img_obj_corners, cat_is_dead = capture_input(program_name)
		if (time.time() - last_frame_timestamp) > DIS_UPDATE_THRESHOLD:
			cat_travel_dis += distance_update(last_img_obj_corners, img_obj_corners)
		last_frame_timestamp = time.time()
		input_list = matrix_to_list(input_matrix)
		# return list of floats(one for each out_node)
		output_list = network.activate(input_list)
		new_keys_pressed = action_decision(output_list)
		# we have focus the program so need to put program_name in press_key
		press_keys(last_keys_pressed, new_keys_pressed)

		fitness = calculate_fitness(cat_travel_dis)
		max_fitness = max(fitness, max_fitness)
		last_keys_pressed = new_keys_pressed
	return max_fitness


def calculate_fitness(cat_travel_dis):
	# different fitness function later
	return cat_travel_dis


def distance_update(last_img_obj_corners, img_obj_corners):
	corner_travels = []

	for corner in img_obj_corners:
		x1, y1 = corner.ravel()
		x0, y0 = 0, 0
		cv2.circle(cat_view_bgr, (x1, y1), 3, 255, -1)
		distance = [1000]
		dirs = [0]
		dx = [0]
		for corner_0 in last_img_obj_corners:
			x0, y0 = corner_0.ravel()
			distance.append(math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2))
			dx.append(abs(x1 - x0))
			if x1 > x0:
				dirs.append(-1)
			else:
				dirs.append(1)

		corner_travels.append(dx[distance.index(min(distance))] * dirs[
			distance.index(min(distance))])
	corner_travels.sort()
	cat_dx = sum(corner_travels[int(len(corner_travels) / 2) - 5:int(
		len(corner_travels) / 2) + 5]) / 10
	return cat_dx


def focus_program(program_name):
	window_handle = win32gui.FindWindow(None, program_name)
	win32gui.SetForegroundWindow(window_handle)


def action_decision(output_list):
	# todo: action decision function
	# we only return left, right, up, down, left and up, right and up(6 possibilities)

	new_keys_pressed = [1 if val >= ACTION_SELECT_THRESHOLD else 0 for val in output_list]
	if (new_keys_pressed[0], new_keys_pressed[1]) == (1, 1):
		if output_list[0] > output_list[1]:
			new_keys_pressed[1] = 0
		else:
			new_keys_pressed[0] = 0

	if (new_keys_pressed[2], new_keys_pressed[3]) == (1, 1):
		if output_list[2] >= output_list[3]:
			new_keys_pressed[1] = 0
		else:
			new_keys_pressed[0] = 0

	return new_keys_pressed


def matrix_to_list(matrix):
	lst = []
	for row in matrix:
		lst.append([float(value) for value in row])
	return lst
