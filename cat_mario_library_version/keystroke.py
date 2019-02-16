import pyautogui
import win32gui
import time



def set_appliaction_focus(appname = 'Syobon Action (??????????)'):
	window = win32gui.FindWindow(None, appname)
	win32gui.SetForegroundWindow(window)

## value goes by 
## [1, 0, 0, 0] = up
## [0, 1, 0, 0] = bottom
## [0, 0, 1, 0] = left
## [0, 0, 0, 1] = right
## [1, 0, 0, 1] = up_right
## [1, 0, 1, 0] = up_left

# m is test data, 14 sequestial key press
m = [[1.0, 0, 0, 0],
	 [1.0, 0, 0, 1.0],
	 [1.0, 0, 0, 1.0],
	 [1.0, 0, 0, 1.0],
	 [1.0, 0, 0, 1.0],
	 [1.0, 0, 0, 1.0],
	 [1.0, 0, 0, 0],
	 [0, 0, 0, 0],
	 [1.0, 0, 0, 0],
	 [1.0, 0, 0, 0],
	 [1.0, 0, 0, 0],
	 [0, 0, 0, 1.0],
	 [0, 0, 0, 1.0],
	 [0, 0, 0, 1.0]]


# call with a array size 4
# for longer key press set any value
def move(value, threshold = 1.0, delay = 0.0):
	if value[0] >= threshold:
		if value[2] >= threshold:
			press_up_left(delay)
		elif value[3] >= threshold:
			press_up_right(delay)
		else:
			press_up(delay)
	elif value[1] >= threshold:
		press_down(delay)
	elif value[2] >= threshold:
		press_left(delay)
	elif value[3] >= threshold:
		press_right(delay)
	else:
		print("No Key to press")

def press_up(delay = 0.0):
	pyautogui.keyDown('up')
	time.sleep(delay)
	pyautogui.keyUp('up')


def press_down(delay = 0.0):
	pyautogui.keyDown('down')
	time.sleep(delay)
	pyautogui.keyUp('down')


def press_right(delay = 0.0):
	pyautogui.keyDown('right')
	time.sleep(delay)
	pyautogui.keyUp('right')

def press_left(delay = 0.0):
	pyautogui.keyDown('left')
	time.sleep(delay)
	pyautogui.keyUp('left')


def press_up_left(delay = 0.0):
	pyautogui.keyDown('up')
	pyautogui.keyDown('left')
	time.sleep(delay)
	pyautogui.keyUp('left')
	pyautogui.keyDown('up')

def press_up_right(delay = 0.0):
	pyautogui.keyDown('up')
	pyautogui.keyDown('right')
	time.sleep(delay)
	pyautogui.keyUp('right')
	pyautogui.keyDown('up')





set_appliaction_focus()
for i in range(13):
	time.sleep(0.5)
	print(time.time())
	move(m[i], 1.0, 0.3)




