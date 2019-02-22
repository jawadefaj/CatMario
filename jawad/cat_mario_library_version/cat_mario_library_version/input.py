from cv_capture_unit.capture_cat_mario import capture_cat_mario


def capture_input(program_name):
	game_bgr, cat_view_bgr, input_matrix, matrix_img, img_obj_corners, cat_is_dead = \
	capture_cat_mario(program_name)

	monitor(game_bgr, cat_view_bgr, matrix_img)

	return input_matrix, img_obj_corners, cat_is_dead


def monitor(game_bgr, cat_view_bgr, matrix_img):
	cv2.rectangle(game_bgr, (cat_pos[0],cat_pos[1]), (cat_pos[0]+block_size,cat_pos[1]+block_size), (255,0,0), 1)

	cv2.imshow("AI", game_bgr)
	cv2.imshow("cat_view", cat_view_bgr)
	cv2.imshow("matrix_out", matrix_img)

	cv2.waitKey(1)