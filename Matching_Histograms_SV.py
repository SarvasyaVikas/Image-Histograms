import argparse
import cv2
from matplotlib import pyplot as plt
from skimage import exposure

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", type = str, default = "X/Rogue.jpg")
ap.add_argument("-r", "--reference", type = str, default = "X/Trask.jpg")
ap.add_argument("-t", "--title", type = str, default = "Rogue_Light.jpg")
args = vars(ap.parse_args())

src = cv2.imread(args["source"])
ref = cv2.imread(args["reference"])

def channels(src):
	if src.shape[-1] > 1:
		return True
	else:
		return False

matched = exposure.match_histograms(src, ref, multichannel = channels(src))
cv2.imwrite("{}.jpg".format(args["title"]), matched)
cv2.imshow("Source", src)
cv2.imshow("Reference", ref)
cv2.imshow("Final", matched)
cv2.waitKey()
