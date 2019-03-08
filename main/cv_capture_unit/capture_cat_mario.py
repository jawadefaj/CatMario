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

import cv2, time, keyboard
import numpy as np
from PIL import ImageGrab
import win32gui, win32ui, win32con

def capture_cat_mario(program_name):
    
    def capture_game():
        #text = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        #os.startfile("SyobonAction\OpenSyobonAction.exe")
        try:
            #modified from: https://www.programcreek.com/python/example/89821/win32gui.GetWindowDC (Example 8)
            hwnd = win32gui.FindWindow(None, program_name)  #The "???????" are actually Japanese char
            #hwnd = win32gui.FindWindow(None, "Syobon Action (??????????)")
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
            #cv2.imshow("AI", crop_img)
            #cv2.waitKey(1)
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
        res = cv2.matchTemplate(game_gray,object_temp, cv2.TM_CCOEFF_NORMED)#cv2.)
        object_loc = (0,0)
        try:
            loc = np.where( res >= 0.4)
            object_loc = (loc[0][0],loc[1][0])
            return object_loc
        except:
            pass
        #print(time.time()-time_start)
        return object_loc

    def get_matrix_out(cat_view_hsv, CAT_VIEW, BLOCK_COLORS, PIX_COLORS):
        timeStamp_low_res = time.time()
        matrix = []
        for row in range(CAT_VIEW[0] + CAT_VIEW[2]):
            matrix_row = []
            for col in range(CAT_VIEW[1] + CAT_VIEW[3]):
                # row = 7
                # col = 4
                img_block = np.array(cat_view_hsv[row * 29 + 4:(row + 1) * 29 - 4:3, col * 29 + 4:(col + 1) * 29 - 4:3])
                block_type = classify_block(img_block, BLOCK_COLORS)
                # block_type = classify_block2(img_block,PIX_COLORS)
                matrix_row.append(block_type)
            matrix.append(matrix_row)
        # print(time.time() - timeStamp_low_res)
        return matrix

    def classify_block(img_block, BLOCK_COLORS):
        errors = []

        for i in range(len(BLOCK_COLORS)):
            error_block = np.sum(abs(img_block - BLOCK_COLORS[i]))
            # if error_block < 500:
            #    return i
            errors.append(error_block)
        # print(errors)
        blocktype = errors.index(min(errors))

        if blocktype <= 1:
            hostile_pix_cnt = 0

            for i in range(7):
                if img_block[i][1][0] == 0 and img_block[i][1][2] == 255:
                    hostile_pix_cnt += 1
            for i in range(7):
                if img_block[i][5][0] == 0 and img_block[i][5][2] == 255:
                    hostile_pix_cnt += 1
            if hostile_pix_cnt > 2:
                return blocktype
            errors[0] = 10000000
            errors[1] = 10000000
        return errors.index(min(errors))

    def get_matrix_out2(cat_view_hsv, PIX_COLORS):
        matrix = []
        res = 29
        for row in range(13):
            matrix_row = []
            for col in range(13):
                # row = 6
                # col = 4
                img_block = np.array(cat_view_hsv[row * res:(row + 1) * res:4, col * res:(col + 1) * res:4])
                matrix_row.append(classify_block2(img_block, PIX_COLORS))
            matrix.append(matrix_row)
        return matrix

    def classify_block2(img_block, PIX_COLORS):
        # print(img_block)
        for row in img_block:
            for pix in row:
                for i in range(10):
                    # i=3
                    # print("---------------------------")
                    # print(pix)
                    # print(PIX_COLORS[i])
                    if pix[0] == PIX_COLORS[i][0] and \
                            pix[1] == PIX_COLORS[i][1] and \
                            pix[2] == PIX_COLORS[i][2]:
                        # print("Match!!!!",i)
                        if i <= 1:
                            return 0
                        if i > 1 and i < 8:
                            return 2
                        if i >= 8:
                            return 8
        return 8

        
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


    def map_matrix(matrix, cat_pos, enemy_val, platform_val, backgound_val):
        #print(matrix[3][0])
        #PIX_COLORS = [WHITE, RED, BROWN, QUESTION, TUBE, GREENBLUE, GRAY, SKYBLUE, BLACK, HILL]
        #Enemy = 0-1
        #Platform = 2-6
        #background = 7-8
        new_matrix=[]
        for row in range(len(matrix)):
            row_list = []
            for col in range(len(matrix[0])):
                val = matrix[row][col]
                if val <= 1:
                    row_list.append(enemy_val)
                if val >= 2 and val <= 6:
                    # row_list.append(255)
                    row_list.append(platform_val)
                if val >= 7:
                    row_list.append(backgound_val)
            new_matrix.append(row_list)
        new_matrix[cat_pos[0]][cat_pos[1]] = backgound_val
        return new_matrix


    def build_matrix_img(matrix, block_size):
        h = len(matrix)
        w = len(matrix[0])
        matrix_out = np.zeros((h*block_size,w*block_size,3), np.uint8)
        for row in range(h):
            for col in range(w):
                matrix_out[row*block_size:(row+1)*block_size, col*block_size:(col+1)*block_size] = matrix[row][col]
        return matrix_out


    def check_death(cat_pos, matrix_out, backgound_val):
        if cat_pos[0]<185 or cat_pos[0]>195 or cat_pos[1] < 185 or cat_pos[1]>195:
             return False
        for row in matrix_out:
            for block in row:
                if block != backgound_val:
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
    size = 7
    #load color from temp img, convert from BGR to HSV
    time_stamp = time.time()

    CAT1_TEMP = cv2.imread('objects/cat1.jpg', 0)
    CAT2_TEMP = cv2.imread('objects/cat2.jpg', 0)
    CAT_TEMP = cv2.imread('objects/cat_merged.jpg', 0)

    #BLACK = cv2.cvtColor(cv2.imread('colors/black.jpg', -1), cv2.COLOR_BGR2HSV)
    '''
    SKYBLUE = cv2.cvtColor(cv2.imread('colors/skyblue.jpg', -1), cv2.COLOR_BGR2HSV)
    BROWN = cv2.cvtColor(cv2.imread('colors/brown.jpg', -1), cv2.COLOR_BGR2HSV)
    GRAY = cv2.cvtColor(cv2.imread('colors/gray.jpg', -1), cv2.COLOR_BGR2HSV)
    GREENBLUE = cv2.cvtColor(cv2.imread('colors/greenblue.jpg', -1), cv2.COLOR_BGR2HSV)
    QUESTION = cv2.cvtColor(cv2.imread('colors/question.jpg', -1), cv2.COLOR_BGR2HSV)
    TUBE = cv2.cvtColor(cv2.imread('colors/tube.jpg', -1), cv2.COLOR_BGR2HSV)
    HILL = cv2.cvtColor(cv2.imread('colors/hill.jpg', -1), cv2.COLOR_BGR2HSV)
    RED = cv2.cvtColor(cv2.imread('colors/red.jpg', -1), cv2.COLOR_BGR2HSV)
    WHITE = cv2.cvtColor(cv2.imread('colors/white.jpg', -1), cv2.COLOR_BGR2HSV)
    '''
    time_stamp_load = time.time()
    WHITE = [0, 0, 255]
    RED = [0, 255, 204]
    BROWN = [15, 170, 153]
    QUESTION = [30, 128, 204]
    TUBE = [60, 255, 230]
    GREENBLUE = [90, 255, 104]
    GRAY = [165, 3, 192]
    SKYBLUE = [113, 91, 249]
    BLACK = [0, 0, 0]
    HILL = [60, 255, 204]
    BLOCK_COLORS = []
    for pix_color in [WHITE, RED, BROWN, QUESTION, TUBE, GREENBLUE, GRAY, SKYBLUE, BLACK, HILL]:
        for row in range(7):
            list = []
            for col in range(7):
                list.append(pix_color)
        BLOCK_COLORS.append(list)
    PIX_COLORS = [WHITE, RED, BROWN, QUESTION, TUBE, GREENBLUE, GRAY, SKYBLUE, BLACK, HILL]
    #print((time.time() - time_stamp_load)*1000)
    #print("-------------------------------")
    #for pix_color in BLOCK_COLORS:
    #    PIX_COLORS.append(pix_color[0][0])

        #print(pix_color[0][0])
    #print((time.time() - time_stamp)*1000)

    CAT_VIEW = [4,6,9,7] #[Left,top,right,bot] block units
    block_size = 29
    #game_corners_0 = []
    #frame_timestamp = 0
    #cat_travel_dis = 0


    start_time = time.time()

    game_bgr = capture_game()

    game_gray = cv2.cvtColor(game_bgr, cv2.COLOR_BGR2GRAY)

    time_stamp_cat = time.time()
    cat_pos = find_object(game_gray, CAT1_TEMP)
    #if cat_pos == (0, 0):
    #    cat_pos = find_object(game_gray,CAT2_TEMP)
    if cat_pos == (0, 0):
        cat_pos = (188, 188)

    #print((time.time()-time_stamp_cat)*1000)
    # Calibrate cat pos to the unit block's top left corner, reverse the (Y,X) order to (X,Y)
    cat_pos = (cat_pos[1]-4,cat_pos[0]+6)

    cat_view_bgr = get_cat_view(game_bgr,cat_pos)
    cat_view_gray = cv2.cvtColor(cat_view_bgr, cv2.COLOR_BGR2GRAY)
    cat_view_hsv = cv2.cvtColor(cat_view_bgr, cv2.cv2.COLOR_BGR2HSV)

    time_stamp_corner = time.time()
    game_corners = np.int0(cv2.goodFeaturesToTrack(cat_view_gray, 30, 0.01, 10))
    #print((time.time() - time_stamp_corner) * 1000)

    class_matrix = get_matrix_out(cat_view_hsv,CAT_VIEW,BLOCK_COLORS,PIX_COLORS)

    matrix_out = map_matrix(class_matrix, (6,4),0,255,128)
    #print_matrix_val(matrix_out)
    matrix_img = build_matrix_img(matrix_out, 29)

    death_out = check_death(cat_pos, matrix_out,128)

    #print(time.time() - time_stamp)
    return game_bgr, cat_view_bgr, matrix_out, matrix_img, game_corners, death_out


