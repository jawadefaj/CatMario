import pyautogui
import win32gui
import time



def set_appliaction_focus(appname = 'Syobon Action (??????????)'):
	window = win32gui.FindWindow(None, appname)
	print(window)
	win32gui.SetForegroundWindow(window)

## value goes by 
## [1, 0, 0, 0] = up
## [0, 1, 0, 0] = down
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

	if value[0] >= threshold  and value[1] > threshold:
		if value[0] >= value[1]:
			value[1] = 0  #come here when up, down > threshold and take the greater value up > down
		else:
			value[0] = 0 #come here when up, down > threshold and take the greater value down > up

	if value[2] >= threshold  and value[3] > threshold:
		if value[2] >= value[3]:
			value[3] = 0  #come here when up, down > threshold and take the greater value left > right
		else:
			value[2] = 0 #come here when up, down > threshold and take the greater value right > left
	# for i in rang(1, 4):
	# 	if value[i] >= threshold:
	# 		for j in range(i+1, 4):
	# 			if value[j] >= threshold:
	# 				if value[i] > value[j]:
	# 					value[j] = 0
	# 				else: value[i] = 0

	if value[0] >= threshold:
		if value[2] >= threshold:
			press_up_left(delay) #come here when up - left
		elif value[3] >= threshold:
			press_up_right(delay) #come here when up - right
		else:
			press_up(delay)    #come here when only up
	elif value[1] >= threshold:
		if value[2] >= threshold: 
			if value[1] >= value[2]:
				press_down(delay) #come here when down > left
			else:
				press_left(delay) #come here when down < left
		if value[3] >= threshold:
			if value[1] >= value[3]: 
				press_down(delay)  #come here when down > right
			else:
				press_right(delay) #come here when down < right 







		press_down(delay)      #come here when only down
	elif value[2] >= threshold:
		press_left(delay)      #come here when only left
	elif value[3] >= threshold:
		press_right(delay)     #come here when only right
	else:
		print("No Key to press") #come here when only none

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




