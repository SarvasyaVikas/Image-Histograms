import argparse
import imutils
import cv2
import numpy as np
from skimage.exposure import is_low_contrast

ap = argparse.ArgumentParser()
ap.add_argument("-I", "--source1", type = str, default = "examples/01.jpg")
ap.add_argument("-II", "--source2", type = str, default = "examples/02.jpg")
ap.add_argument("-III", "--source3", type = str, default = "examples/03.jpg")
args = vars(ap.parse_args())

src1 = cv2.imread(args["source1"])
src1 = imutils.resize(src1, width = 450)
src2 = cv2.imread(args["source2"])
src2 = imutils.resize(src2, width = 450)
src3 = cv2.imread(args["source3"])
src3 = imutils.resize(src3, width = 450)

def gamma_correction(image, gamma):
	invGamma = 1.0 / gamma
	
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in range(0, 256)]).astype("uint8")
	
	return cv2.LUT(image, table)

def contrast_value(src):
	if is_low_contrast(src, fraction_threshold = 0.2):
		adjusted = gamma_correction(src, 2.0)
		return adjusted
	elif is_low_contrast(src, fraction_threshold = 0.3):
		adjusted = gamma_correction(src, 1.5)
		return adjusted
	elif is_low_contrast(src, fraction_threshold = 0.4):
		adjusted = gamma_correction(src, 1.0)
		return adjusted	
	elif is_low_contrast(src, fraction_threshold = 0.5):
		adjusted = gamma_correction(src, 0.5)
		return adjusted

def contrast_define(src):
	if is_low_contrast(src, fraction_threshold = 0.2):
		return 2.0
	elif is_low_contrast(src, fraction_threshold = 0.3):
		return 1.5
	elif is_low_contrast(src, fraction_threshold = 0.4):
		return 1.0	
	elif is_low_contrast(src, fraction_threshold = 0.5):
		return 0.5

def putText(src, adjusted):
	category = contrast_define(src)
	cv2.putText(adjusted, "Gamma = {}".format(category), (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
	return adjusted

cv2.imshow("Source 1", putText(src1, contrast_value(src1)))
cv2.imshow("Source 2", putText(src2, contrast_value(src2)))
cv2.imshow("Source 3", putText(src3, contrast_value(src3)))
cv2.waitKey()
