import pyautogui
import keyboard

def press_keys(last_keys_pressed, new_keys_pressed):

	# both keys_pressed are list of four 0/1 values
	# representing left, right, up, down states
	pyautogui.PAUSE = 0
	left_pair = last_keys_pressed[0], new_keys_pressed[0]
	right_pair = last_keys_pressed[1], new_keys_pressed[1]
	up_pair = last_keys_pressed[2], new_keys_pressed[2]
	down_pair = last_keys_pressed[3], new_keys_pressed[3]



	# release key first 
	if left_pair == (1, 0):
		pyautogui.keyUp('left')

	if right_pair == (1, 0):
		pyautogui.keyUp('right')

	if up_pair == (1, 0):
		pyautogui.keyUp('up')

	if down_pair == (1, 0):
		pyautogui.keyUp('down')


	#pressing new key 
		
	if left_pair == (0, 1):
		pyautogui.keyDown('left')
		
	if right_pair == (0, 1):
		pyautogui.keyDown('right')

	if up_pair == (0, 1):
		pyautogui.keyDown('up')

	if down_pair == (0, 1):
		pyautogui.keyDown('down')

	pyautogui.PAUSE = 0.1

	# if left_pair == (1, 0):
	# 	keyboard.KEY_UP = 'left'

	# if right_pair == (1, 0):
	# 	keyboard.KEY_UP = 'right'

	# if up_pair == (1, 0):
	# 	keyboard.KEY_UP = 'up'

	# if down_pair == (1, 0):
	# 	keyboard.KEY_UP = 'down'


	# #pressing new key 
		
	# if left_pair == (0, 1):
	# 	keyboard.KEY_DOWN = 'left'
		
	# if right_pair == (0, 1):
	# 	keyboard.KEY_DOWN = 'right'

	# if up_pair == (0, 1):
	# 	keyboard.KEY_DOWN = 'up'

	# if down_pair == (0, 1):
	# 	keyboard.KEY_DOWN = 'down'
