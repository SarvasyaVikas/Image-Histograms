import argparse
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type = str, default = "X/Kitty.jpg")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

def gamma_correction(image, gamma):
	invGamma = 1.0 / gamma
	
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in range(0, 256)]).astype("uint8")
	
	return cv2.LUT(image, table)

red = (0, 0, 255)

while True:

	gamma = 0.1

	while gamma <= 3.0:
		adjusted = gamma_correction(image, gamma)
		cv2.putText(adjusted, "Gamma = {}".format(gamma), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, red, 3)
		cv2.imshow("Images", np.hstack([image, adjusted]))
		cv2.waitKey(100)
		gamma += 0.1
		gamma = round(gamma, 1)
		
	gamma = 3.0

	while gamma > 0:
		adjusted = gamma_correction(image, gamma)
		cv2.putText(adjusted, "Gamma = {}".format(gamma), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, red, 3)
		cv2.imshow("Images", np.hstack([image, adjusted]))
		cv2.waitKey(100)
		gamma -= 0.1
		gamma = round(gamma, 1)
