# import the necessary packages
import argparse
import cv2
import os
import csv
# initialize the list of reference points and boolean indicating
refPt = []
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
    global refPt
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))
        cv2.circle(image, (x, y), 5, (255, 255, 255), -1)
        if len(refPt) > 1:
            cv2.line(image, refPt[-2], refPt[-1], (0, 0, 0), 2)
	# check to see if the left mouse button was released
    if event == cv2.EVENT_RBUTTONDOWN:
        if len(refPt) > 1:
            cv2.line(image, refPt[-1], refPt[0], (0, 0, 0), 2)
        with open('points.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            row = [args["image"], len(refPt), refPt]
            writer.writerow(row)
    cv2.imshow("image", image)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
# keep looping until the 'q' key is pressed
if not os.path.isfile('points.csv'):
    with open('points.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        header = ['Image name', 'Num of Points', 'Coordinates']
        writer.writerow(header)
while True:
	# display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF
	# if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        image = clone.copy()
	# if the 'q' key is pressed, break from the loop
    elif key == ord("q"):
        imagename = os.path.split(args["image"])[-1]
        cv2.imwrite("Output/" + imagename, image)
        break

# close all open windows
cv2.destroyAllWindows()