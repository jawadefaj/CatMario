from input import capture_input
from neat.nn.feed_forward import FeedForwardNetwork # for the 'network' parameter
from output import press_keys
import win32gui
import time, cv2, math, os
import pyautogui


DIS_UPDATE_THRESHOLD = 0.0
ACTION_SELECT_THRESHOLD = 0.7
RESTART_THRESHOLD = 5.0
PROJECT_DIR = r'C:\Users\abjaw\Documents\GitHub\CatMario\main'

def run_game(program_name, network):
	# todo: open the game program
	# open_game()
	focus_program(program_name)

	# initialization
	cat_is_dead = False
	max_fitness = 0
	last_keys_pressed = [0, 0, 0, 0]  # left, right , up , down, 0/1: not/pressed
	last_frame_timestamp = 0
	cat_travel_dis = 0  # subtract when cat moves left, increment when cat moves right
	last_img_obj_corners = []

	# track_for_trap = 0
	# track_for_trap_time = time.time()
	
	track_for_trap = 0
	track_for_trap_time = time.time() + 5.0

	
	# last_update = 0
	flag = True
	while not cat_is_dead:
		fps_time = time.time()
		input_matrix, img_obj_corners, cat_is_dead = capture_input(program_name)
		# print("cat_is_dead ",cat_is_dead)
		if (time.time() - last_frame_timestamp) > DIS_UPDATE_THRESHOLD:
			cat_travel_dis += distance_update(last_img_obj_corners, img_obj_corners)

		if cat_travel_dis>track_for_trap:
			track_for_trap_time = time.time() + 5.0

		track_for_trap = max(cat_travel_dis, track_for_trap)
		# print(int(track_for_trap) , int(cat_travel_dis), (last_frame_timestamp - track_for_trap_time))
		print(track_for_trap_time - time.time(), cat_is_dead, track_for_trap, cat_travel_dis)
		if time.time() > track_for_trap_time:
			if track_for_trap > cat_travel_dis:
				# print("killing for trap", time.time(), track_for_trap_time, track_for_trap, cat_travel_dis)
				# cat_is_dead = True
				kill_game()
				break
			if track_for_trap == cat_travel_dis:
				cat_travel_dis -=1
				# print("counter increase")
				track_for_trap_time = time.time() + 2.0


		last_img_obj_corners = img_obj_corners
		last_frame_timestamp = time.time()
		input_list = matrix_to_list(input_matrix)
		# return list of floats(one for each out_node)

		output_list = network.activate(input_list)
		new_keys_pressed = action_decision(output_list)
		# we have focus the program so need to put program_name in press_key
		press_keys(last_keys_pressed, new_keys_pressed)
		fitness = calculate_fitness(cat_travel_dis)
		max_fitness = max(fitness, max_fitness)
		# if 1.0/(time.time() - fps_time) < 20.0:
		# 	print(last_keys_pressed, new_keys_pressed, 1.0/(time.time() - fps_time))
		last_keys_pressed = new_keys_pressed
	# print("Return to the main loop")
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

def find_window(program_name):
	return win32gui.FindWindow(None, program_name)
		

def open_game():
	cwd = os.getcwd()
	os.chdir(PROJECT_DIR + r'\SyobonAction')
	os.startfile(PROJECT_DIR + r'\SyobonAction' + r'\OpenSyobonAction.exe')
	time.sleep(2.0)
	os.chdir(cwd)
	pyautogui.keyDown('enter')
	pyautogui.keyUp('enter')

def kill_game():
	# pyautogui.PAUSE = 1
	os.system("TASKKILL /F /IM OpenSyobonAction.exe")
	pyautogui.keyUp('up')
	pyautogui.keyUp('down')
	pyautogui.keyUp('left')
	pyautogui.keyUp('right')
	pyautogui.PAUSE = 0.1
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
		if output_list[2] > output_list[3]:
			new_keys_pressed[3] = 0
		else:
			new_keys_pressed[2] = 0

	return new_keys_pressed


def matrix_to_list(matrix):
	lst = []
	for row in matrix:
                
                lst += [float(value) for value in row]
	return lst
