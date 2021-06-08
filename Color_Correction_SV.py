import argparse
import cv2
import numpy as np
import imutils
from skimage import exposure
from imutils.perspective import four_point_transform

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", type = str, default = "Augmented_Reality/examples/input_01.jpg")
ap.add_argument("-r", "--reference", type = str, default = "Augmented_Reality/reference.jpg")
args = vars(ap.parse_args())

src = cv2.imread(args["source"])
ref = cv2.imread(args["reference"])

def find_color_card(image):
	arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
	arucoParameters = cv2.aruco.DetectorParameters_create()
	(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters = arucoParameters)
	
	global id_lst
	id_lst = ids.flatten()
	
	lst = []
	
	for (MarkerID) in zip(id_lst):
		lst.append(MarkerID)
	
	return lst
	
def focus_card(image):
	arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
	arucoParameters = cv2.aruco.DetectorParameters_create()
	(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters = arucoParameters)
	
	i = np.squeeze(np.where(id_lst == 923))
	topLeft = np.squeeze(corners[i])[0]
	
	i = np.squeeze(np.where(id_lst == 1001))
	topRight = np.squeeze(corners[i])[1]
	
	i = np.squeeze(np.where(id_lst == 241))
	bottomRight = np.squeeze(corners[i])[2]
	
	i = np.squeeze(np.where(id_lst == 1007))
	bottomLeft = np.squeeze(corners[i])[3]
	
	cardCoordinates = np.array([topLeft, topRight, bottomRight, bottomLeft])
	card = four_point_transform(image, cardCoordinates)

	return card

def mark_card(image):
	arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
	arucoParameters = cv2.aruco.DetectorParameters_create()
	(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters = arucoParameters)
	
	lst = []
	
	for (MarkerCorner, MarkerID) in zip(corners, id_lst):
		corners = MarkerCorner.reshape((4,2))
		(tl, tr, br, bl) = corners
		
		topLeft = (int(tl[0]), int(tl[1]))
		topRight = (int(tr[0]), int(tr[1]))
		bottomLeft = (int(bl[0]), int(bl[1]))
		bottomRight = (int(br[0]), int(br[1]))
		
		cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
		cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
		cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
		cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
		
		cX = int((topLeft[0] + bottomRight[0]) / 2.0)
		cY = int((topLeft[1] + bottomRight[1]) / 2.0)
		cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
		
		cv2.putText(image, str(MarkerID), (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
	
	return image

print(find_color_card(src))
inpt = imutils.resize(src, width = 600)
info = imutils.resize(ref, width = 600)
outpt = focus_card(inpt)
ref_final = focus_card(info)
final = mark_card(inpt)

matched = exposure.match_histograms(final, info, multichannel = True)

cv2.imshow("Detected Image", outpt)
cv2.imshow("Detected Markers", final)
cv2.imshow("Final Image", matched)
cv2.waitKey()
