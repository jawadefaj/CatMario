import pyautogui


def press_keys(last_keys_pressed, new_keys_pressed, up_count, right_count, down_count, left_count):

	# both keys_pressed are list of four 0/1 values
	# representing left, right, up, down states

	left_pair = last_keys_pressed[0], new_keys_pressed[0]
	right_pair = last_keys_pressed[1], new_keys_pressed[1]
	up_pair = last_keys_pressed[2], new_keys_pressed[2]
	down_pair = last_keys_pressed[3], new_keys_pressed[3]

	if left_pair == (0, 1):
		left_count = left_count + 1
		pyautogui.keyDown('left')
		
	if left_pair == (1, 0):
		pyautogui.keyUp('left')

	if right_pair == (0, 1):
		right_count = right_count + 1
		pyautogui.keyDown('right')

	if right_pair == (1, 0):
		pyautogui.keyUp('right')

	if up_pair == (0, 1):
		up_count = up_count + 1
		pyautogui.keyDown('up')

	if up_pair == (1, 0):
		pyautogui.keyUp('up')

	if down_pair == (0, 1):
		down_count = down_count + 1
		pyautogui.keyDown('down')

	if down_pair == (1, 0):
		pyautogui.keyUp('down')


	return up_count, right_count, down_count, left_count