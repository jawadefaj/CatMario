#Setup: win32gui only support 32bit Python 3.5 and 3.6 !!!
#run the game before running this program
#press ESC anytime in shell to exit program

#use the following commands in shell to install necessary libraries
#pip install opencv-python
#pip install matplotlib
#pip install pywin32
#pip install win32gui
#pip install win32ui
#pip3 install pillow
#pip3 install keyboard
#pip install pynput

import cv2, time, keyboard, os, sys, math
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageGrab
from pynput.keyboard import Key, Controller
import win32gui, win32ui, win32con


def capture_game():
    #text = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    #os.startfile("SyobonAction\OpenSyobonAction.exe")
    try:
        #modified from: https://www.programcreek.com/python/example/89821/win32gui.GetWindowDC (Example 8)
        hwnd = win32gui.FindWindow(None, "Syobon Action (??????????)")  #The "???????" are actually Japanese char
        rect = win32gui.GetWindowRect(hwnd)
        w = rect[2]-rect[0]
        h = rect[3]-rect[1]
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
        im = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(im, dtype='uint8')
        img.shape = (h,w,4)
        crop_img = img[29:h, 3:w-3,0:4] #crop the boarders
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        return crop_img
    
    except:
        #os.startfile("SyobonAction\OpenSyobonAction.exe")
        print("Cannot locate game")
        #hwnd = win32gui.FindWindow(None, "Syobon Action (??????????)")


def get_cat_view(game_bgr, cat_pos):
    CAT_VIEW = [4,6,9,7] #[Left,top,right,bot] block units
    block_size = 29
    cat_view_bound = [cat_pos[0]-block_size*CAT_VIEW[0],cat_pos[1]-block_size*CAT_VIEW[1],\
                      cat_pos[0]+block_size*CAT_VIEW[2],cat_pos[1]+block_size*CAT_VIEW[3]]   
    cat_view_bound_fix = cat_view_bound.copy()
    
    # cat_view_bound_fix reset the index so it doesnt go out of range
    if cat_view_bound[0]< 0:
        cat_view_bound_fix[0] = 0
    if cat_view_bound[1]< 0:
        cat_view_bound_fix[1] = 0
    if cat_view_bound[2]> game_bgr.shape[1]:
        cat_view_bound_fix[2] = game_bgr.shape[1]
    if cat_view_bound[3]> game_bgr.shape[0]:
        cat_view_bound_fix[3] = game_bgr.shape[0]
          
    cat_view_boarder = abs(np.subtract(cat_view_bound,cat_view_bound_fix))
    cv2.rectangle(game_bgr,(cat_view_bound[0],cat_view_bound[1]),(cat_view_bound[2],cat_view_bound[3]), (255,0,0), 2)
    cat_view_bgr = game_bgr[cat_view_bound_fix[1]:cat_view_bound_fix[3],cat_view_bound_fix[0]:cat_view_bound_fix[2]]
    cat_view_bgr = cv2.copyMakeBorder(cat_view_bgr,cat_view_boarder[1],cat_view_boarder[3],cat_view_boarder[0],cat_view_boarder[2],0, None, 0)

    return cat_view_bgr

    
def find_object(game_gray, object_temp):
    #time_start = time.time()
    #template = cv2.imread(object_temp,0)
    res = cv2.matchTemplate(game_gray,object_temp,cv2.TM_CCOEFF_NORMED)
    object_loc = (0,0)
    try:
        loc = np.where( res >= 0.6)
        object_loc = (loc[0][0],loc[1][0])
    except:
        pass
    #print(time.time()-time_start)
    return object_loc


def get_matrix_out(cat_view_bgr,CAT_VIEW,BLOCK_COLORS, PIX_COLORS):
    timeStamp_low_res = time.time()
    matrix = []
    for row in range (CAT_VIEW[0] + CAT_VIEW[2]):
        matrix_row = []
        for col in range(CAT_VIEW[1] + CAT_VIEW[3]):
            img_block = np.array(cat_view_bgr[row*29:(row+1)*29,col*29:(col+1)*29])
            img_block = cv2.cvtColor(img_block, cv2.cv2.COLOR_BGR2HSV)
            block_type = classify_block(img_block,BLOCK_COLORS)
           # block_type = classify_block2(img_block,PIX_COLORS)
            matrix_row.append(block_type)
        matrix.append(matrix_row)
    return matrix


def classify_block(img_block,BLOCK_COLORS):
    errors = []
    
    for i in range (len(BLOCK_COLORS)):
        error_block = abs(img_block - BLOCK_COLORS[i])
        errors.append(np.sum(error_block))

    blocktype = errors.index(min(errors))
    
    if blocktype == 8 or blocktype == 9:     
        hostile_pix_cnt = 0
        for i in range(10):
            if img_block[i*3][0][0] == 0 and img_block[i*3][0][2]==255:
                hostile_pix_cnt += 1
        for i in range(10):
            if img_block[i*3][15][0] == 0 and img_block[i*3][15][2]==255:
                hostile_pix_cnt += 1
        for i in range(10):
            if img_block[i*3][28][0] == 0 and img_block[i*3][28][2]==255:
                hostile_pix_cnt += 1
        if hostile_pix_cnt > 5:
            return blocktype
        errors.pop(9)
        errors.pop(8)
    return errors.index(min(errors))


def classify_block2(img_block,PIX_COLORS):
    img_block = img_block[::3,::3]
    pix_cnt = len(img_block)*len(img_block[0])
    hostile_pix_cnt = 0
    platform_pix_cnt = 0
    for row in img_block:
        for pix in row:
            if pix.all() == PIX_COLORS[8].all() or pix.all() == PIX_COLORS[9].all():
                hostile_pix_cnt += 1
            if pix.all() == PIX_COLORS[3].all() or pix.all() == PIX_COLORS[4].all() or pix.all() == PIX_COLORS[5].all() \
               or pix.all() == PIX_COLORS[6].all() or pix.all() == PIX_COLORS[7].all():
                platform_pix_cnt += 1
            if hostile_pix_cnt > pix_cnt*0.2:
                return 8
            if platform_pix_cnt > pix_cnt*0.3:
                return 3
    return 0

    
def print_matrix_val(matrix):
    for row in matrix:
        print("")
        print(row)


def pix_info(event,img):
    print (event.x, event.y)
    print("BGR color")
    print (img[event.y, event.x])
    # convert color from BGR to HSV color scheme
    hsv = cv.cvtColor(imgCV, cv.COLOR_BGR2HSV)
    print("HSV color")
    print (hsv[event.y, event.x])


def map_matrix(matrix, cat_pos, background_ini_index, platform_ini_index, enemy_ini_index):
    #print(matrix[3][0])
    new_matrix=[]
    for row in range(len(matrix)):
        row_list = []
        for col in range(len(matrix[0])):
            val = matrix[row][col]
            if val >= 0 and val < platform_ini_index:
                row_list.append(128)
            if val >= platform_ini_index and val < enemy_ini_index:
                row_list.append(255)
            if val >= enemy_ini_index:
                row_list.append(0)
            if (row,col)== cat_pos:
                row_list[col]=128
        new_matrix.append(row_list)
    return new_matrix


def build_matrix_img(matrix, block_size):
    h = len(matrix)
    w = len(matrix[0])
    matrix_out = np.zeros((h*block_size,w*block_size,3), np.uint8)
    for row in range(h):
        for col in range(w):
            matrix_out[row*block_size:(row+1)*block_size,col*block_size:(col+1)*block_size]= matrix[row][col]
    return matrix_out


def check_death(cat_pos, matrix_out):
    for row in matrix_out:
        for block in row:
            if block != 128:
                return False
    if cat_pos != (191,190):
        return False
    return True
    
#PIL (no longer used)
def get_game_loc(game_loc, logo_temp):
    timeStamp_logo = time.time()
    logo_bound = (game_loc[1]-20,game_loc[0],game_loc[1]+100,game_loc[0]+20)
    logo_rgb = np.array(ImageGrab.grab(logo_bound))[:, :, ::-1]
    logo_gray = cv2.cvtColor(logo_rgb, cv2.COLOR_BGR2GRAY)
    timestamp = 0
    while(find_object(logo_gray,logo_temp)==[0,0]):
        logo_rgb = CaptureScreen()
        logo_gray = cv2.cvtColor(logo_rgb, cv2.COLOR_BGR2GRAY)
        game_loc = find_object(logo_gray,logo_temp)
        if (time.time()-timestamp>1):
            print("Finding game window..")
            timestamp = time.time()
        try:
            if keyboard.is_pressed('esc'):
                break
        except:
            pass
    #print(time.time()-timeStamp_logo)
    print("game loc: ",game_loc)
    return game_loc


#------------------Main--------------------

#load color from temp img, convert from BGR to HSV
CAT1_TEMP = cv2.imread('objects/cat1.jpg',0)
CAT2_TEMP = cv2.imread('objects/cat2.jpg',0)
BLACK = cv2.cvtColor(cv2.imread('colors/black.jpg',-1), cv2.COLOR_BGR2HSV)
SKYBLUE = cv2.cvtColor(cv2.imread('colors/skyblue.jpg',-1), cv2.COLOR_BGR2HSV)
BROWN = cv2.cvtColor(cv2.imread('colors/brown.jpg',-1), cv2.COLOR_BGR2HSV)
GRAY = cv2.cvtColor(cv2.imread('colors/gray.jpg',-1), cv2.COLOR_BGR2HSV)
GREENBLUE = cv2.cvtColor(cv2.imread('colors/greenblue.jpg',-1), cv2.COLOR_BGR2HSV)
QUESTION = cv2.cvtColor(cv2.imread('colors/question.jpg',-1), cv2.COLOR_BGR2HSV)
TUBE = cv2.cvtColor(cv2.imread('colors/tube.jpg',-1), cv2.COLOR_BGR2HSV)
HILL = cv2.cvtColor(cv2.imread('colors/hill.jpg',-1), cv2.COLOR_BGR2HSV)
RED = cv2.cvtColor(cv2.imread('colors/red.jpg',-1), cv2.COLOR_BGR2HSV)
WHITE = cv2.cvtColor(cv2.imread('colors/white.jpg',-1), cv2.COLOR_BGR2HSV)
BLOCK_COLORS = np.array([BLACK,SKYBLUE,HILL,BROWN,GRAY,GREENBLUE,QUESTION,TUBE,RED,WHITE])
PIX_COLORS = []
for pix_color in BLOCK_COLORS:
    PIX_COLORS.append(pix_color[0][0])

print_timestamp = 0
keyboard_timeStamp = 0
CAT_VIEW = [4,6,9,7] #[Left,top,right,bot] block units
block_size = 29
game_corners_0 = []
frame_timestamp = 0
cat_travel_dis = 0
while(1):
    start_time = time.time()

    game_bgr = capture_game()
    game_gray = cv2.cvtColor(game_bgr, cv2.COLOR_BGR2GRAY)

    cat_pos = find_object(game_gray,CAT1_TEMP)
    if cat_pos == (0,0):
        cat_pos = find_object(game_gray,CAT2_TEMP)
    if cat_pos != (0,0):
        # Calibrate cat pos to the unit block's top left corner, reverse the (Y,X) order to (X,Y)
        cat_pos = (cat_pos[1]-4,cat_pos[0]+4)  

        cat_view_bgr = get_cat_view(game_bgr,cat_pos)
        cat_view_gray = cv2.cvtColor(cat_view_bgr, cv2.COLOR_BGR2GRAY)
        game_corners = np.int0(cv2.goodFeaturesToTrack(cat_view_gray, 60, 0.01, 10))


        #initizlize the following outside of the main loop
        # frame_timestamp = 0
        # cat_travel_dis =0
        # game_corners_0 = []
        
        corner_travels = []
        if(time.time()- frame_timestamp > 0.05): #frame refresh time
            for corner in game_corners:
                x1,y1 = corner.ravel()
                x0,y0 = 0,0
                cv2.circle(cat_view_bgr,(x1,y1),3,255,-1)
                distance = [1000]
                dirs = [0]
                dx = [0]
                for corner_0 in game_corners_0:
                    x0,y0 = corner_0.ravel()
                    distance.append(math.sqrt((x1-x0)**2+(y1-y0)**2))
                    dx.append(abs(x1-x0))
                    if x1>x0:
                        dirs.append(-1)
                    else:
                        dirs.append(1)
                
                corner_travels.append(dx[distance.index(min(distance))]*dirs[distance.index(min(distance))])                
            game_corners_0 = game_corners.copy()
            corner_travels.sort()
            cat_dx = sum(corner_travels[int(len(corner_travels)/2)-5:int(len(corner_travels)/2)+5])/10
            cat_travel_dis += int(cat_dx)
            print("fitness:", cat_travel_dis)
            frame_timestamp = time.time()
        


        
        class_matrix = get_matrix_out(cat_view_bgr,CAT_VIEW,BLOCK_COLORS,PIX_COLORS)
        matrix_out = map_matrix(class_matrix, (6,4), 0, 3, 8)
        matrix_img = build_matrix_img(matrix_out, 29)

        death_out = check_death(cat_pos, matrix_out)

        cv2.rectangle(game_bgr,(cat_pos[0],cat_pos[1]), (cat_pos[0]+block_size,cat_pos[1]+block_size), (255,0,0), 1)
        cv2.imshow("AI",game_bgr)
        cv2.imshow("cat_view",cat_view_bgr)
        cv2.imshow("matrix_out",matrix_img)
        #cv2.imshow("corner",game_corner)
        cv2.waitKey(1)
    
    if time.time()- print_timestamp>0.5:
        print("fps:",int(1/(time.time()-start_time)))
        #print_matrix_val(matrix_out)
        #print_matrix_val(class_matrix)
        print_timestamp = time.time()
       
    try:
        if keyboard.is_pressed('esc'):
            break
    except:
        pass

