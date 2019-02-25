from input import capture_input
from neat.nn.feed_forward import FeedForwardNetwork # for the 'network' parameter
from output import press_keys
import win32gui
import time, cv2, math, os
import pyautogui
from neat_core.Neat import Genome

ACTION_SELECT_THRESHOLD = 0.7
RESTART_THRESHOLD = 5.0


def run_game(program_name, network, lib=True):
	start_game()
	focus_program(program_name)

	# initialization
	cat_is_dead = False
	max_fitness = 0
	last_keys_pressed = [0, 0, 0, 0]  # left, right , up , down, 0/1: not/pressed
	cat_travel_dis = 0  # subtract when cat moves left, increment when cat moves right
	last_img_obj_corners = []
	trapped_start_time = 0
	trapped = False
	last_frame_timestamp = 0

	while not cat_is_dead:

		input_matrix, img_obj_corners, cat_is_dead = capture_input(program_name)
		print(cat_is_dead)
		distance_changed = distance_update(last_img_obj_corners, img_obj_corners)
		if (time.time() - last_frame_timestamp) > 0:
			cat_travel_dis += distance_changed
			last_frame_timestamp = time.time()

		checking trapped
		fitness = calculate_fitness(cat_travel_dis)
		if not trapped:
			if fitness <= max_fitness:
				trapped = True
				trapped_start_time = time.time()
			else:
				max_fitness = fitness
		if trapped:
			if fitness > max_fitness:
				trapped = False
				max_fitness = fitness
			else:
				if time.time() - trapped_start_time >= RESTART_THRESHOLD:
					print("Killing and RESTART")
					kill_game()
					start_game()
					break

		last_img_obj_corners = img_obj_corners
		input_list = matrix_to_list(input_matrix)
		# return list of floats(one for each out_node)

		if lib:
			output_list = network.activate(input_list)
		else:
			# for non_lib version, network here is the genome object
			output_list = network.get_output(input_list)
		new_keys_pressed = action_decision(output_list)
		# we have focus the program so no need to put program_name in press_key
		press_keys(last_keys_pressed, new_keys_pressed)
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
		#cv2.circle(cat_view_bgr, (x1, y1), 3, 255, -1)
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


def start_game():
	cwd = os.getcwd()
	os.chdir('SyobonAction')
	os.startfile('OpenSyobonAction.exe')
	time.sleep(1.5)
	os.chdir(cwd)
	pyautogui.keyDown('enter')
	pyautogui.keyUp('enter')


def kill_game():
	os.system("TASKKILL /F /IM OpenSyobonAction.exe")
	pyautogui.keyUp('up')
	pyautogui.keyUp('down')
	pyautogui.keyUp('left')
	pyautogui.keyUp('right')
	time.sleep(2.0)


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
		lst += [float(value) for value in row]
	return lst
