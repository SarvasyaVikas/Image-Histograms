import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type = str, default = "X/Kitty.jpg")
ap.add_argument("-c", "--clip", type = float, default = 2.0)
ap.add_argument("-tY", "--tile_Y", type = int, default = 8)
ap.add_argument("-tX", "--tile_X", type = int, default = 8)
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

clahe = cv2.createCLAHE(clipLimit = args["clip"], tileGridSize = (args["tile_Y"], args["tile_X"]))
equalized = clahe.apply(gray)

cv2.imshow("Original Image", gray)
cv2.imshow("Modified Image", equalized)
cv2.waitKey()

while True:

	tile = 4

	while tile <= 10:
		clahe = cv2.createCLAHE(clipLimit = args["clip"], tileGridSize = (tile, tile))
		equalized = clahe.apply(gray)

		cv2.imshow("Original Image", gray)
		cv2.imshow("Modified Image", equalized)
		cv2.waitKey(40)

	tile = 10

	while tile >= 4:
		clahe = cv2.createCLAHE(clipLimit = args["clip"], tileGridSize = (tile, tile))
		equalized = clahe.apply(gray)

		cv2.imshow("Original Image", gray)
		cv2.imshow("Modified Image", equalized)
		cv2.waitKey(40)
