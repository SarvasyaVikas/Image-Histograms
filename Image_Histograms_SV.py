import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt

ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", type=str, default = "X/Kitty.jpg")

args = vars(ap.parse_args())

image = cv2.imread(args["image"])
(h, w) = image.shape[:2]

def histogram(image, masked):
	channels = cv2.split(image)
	colors = ("b", "g", "r")
	plt.figure()
	plt.title("Image Histogram")
	plt.xlabel("Bins")
	plt.ylabel("Number of Pixels")
	
	for (channel, color) in zip(channels, colors):
		histogram = cv2.calcHist([channel], [0], mask, [256], [0, 256])
		plt.plot(histogram, color = color)
		plt.xlim([0, 256])


blank = np.zeros(image.shape[:2], dtype = "uint8")
mask = cv2.circle(blank, ( h // 2, w // 2), 200, 255, -1)
masked = cv2.bitwise_and(image, image, mask = mask)
histogram(image, mask)
plt.show()
plt.pause(1)
plt.close()
cv2.imshow("Masked Region", masked)
cv2.waitKey(1000)
