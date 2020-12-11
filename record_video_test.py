" this code is for recording steering inputs together with camera inputs while following a predefined path"

import cozmo
import numpy as np
import os, sys, time
from PIL import Image
from cozmo.util import degrees
import json
from flask import Blueprint, request

# Choose whether you are recording training or validation data
data_dir = 'data_train'
#data_dir = 'data_val'



def run(sdk_conn):
	robot = sdk_conn.wait_for_robot()
	robot.camera.image_stream_enabled = True
	robot.camera.color_image_enabled = True
	# Lift arm and look down
	robot.set_lift_height(1.0, in_parallel=True).wait_for_completed()
	robot.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE + degrees(5)).wait_for_completed()
	robot.set_head_light(True)

	images = list()
	steer = list()
	imgSize = (66, 200, 3) # h, w, channels
# -------- Main Program Loop -----------
run = True
recording = False
print("Not recording, press joystick button to start. Cozmo's lights will turn red while recording.")

# Save images and steering input
# if len(images) > 0:
# 	print('Saving images')
# 	img_arr = np.zeros((len(images), imgSize[0], imgSize[1], imgSize[2]), dtype=np.float16)
# 	steer_arr = np.zeros(len(steer), dtype=np.float32)
# 	for i in range(0, len(images)):
# 		img_arr[i] = np.array(images[i], dtype=np.float16) / 255.
# 		steer[i] = steer[i]

# 		timestr = time.strftime("%Y%m%d-%H%M%S")

# 		if not os.path.exists(data_dir):
# 			os.mkdir(data_dir)
# 		np.savez(f'{data_dir}/{timestr}-images.npz', img_arr=img_arr)
# 		np.savez(f'{data_dir}/{timestr}-steer.npz', steer_arr=steer_arr)
# print('Done')






if __name__ == "__main__":
	# pygame.init()
	cozmo.setup_basic_logging()
	try:
		cozmo.connect_with_tkviewer(run)
	except KeyboardInterrupt as e:
		pass
	except cozmo.ConnectionError as e:
		sys.exit("A connection error occurred: %s" % e)