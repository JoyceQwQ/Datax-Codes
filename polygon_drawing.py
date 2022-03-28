# import the necessary packages
import argparse
import cv2
import os
import csv
import tkinter as tk

# initialize the list of reference points and boolean indicating
refPt = []
pts_keep = []
keep = None
circleColour = None
lineColour = None

def getText():
    # Top level window
    frame = tk.Tk()
    frame.title("Keep or Remove?")
    frame.geometry('300x200')
    # Function for getting Input
    # from textbox and printing it 
    # at label widget
    def printInput():
        global keep
        inp = inputtxt.get(1.0, "end-1c").strip()
        if (len(inp)) > 0:
            if inp.isdigit():
                if int(inp) == 0 or int(inp) == 1:
                    frame.destroy()
                    keep = int(inp)
                else:
                    lbl.config(text = "Please enter 0 / 1")
            else:
                lbl.config(text = "Please enter 0 / 1")
    
    # TextBox Creation
    inputtxt = tk.Text(frame,
                    height = 5,
                    width = 20)

    def callback(event):
        global keep
        inp = inputtxt.get(1.0, "end-1c").strip()
        if (len(inp)) > 0:
            if inp.isdigit():
                if int(inp) == 0 or int(inp) == 1:
                    frame.destroy()
                    keep = int(inp)
                else:
                    lbl.config(text = "Please enter 0 / 1")
            else:
                lbl.config(text = "Please enter 0 / 1")

    frame.bind('<Return>', callback)

    label = tk.Label(frame, text="Please enter 0 / 1: (0 = removed, 1= keep) ")
    label.pack()
    
    inputtxt.pack()

    lbl = tk.Label(frame, text="")
    lbl.pack()
    
    # Button Creation
    printButton = tk.Button(frame,
                            text = "OK", 
                            command = printInput)
    printButton.pack()
    
    # Label Creation
    lbl = tk.Label(frame, text = "")
    lbl.pack()
    frame.mainloop()

def colourChange(keep):
    global circleColour, lineColour
    if keep:
        circleColour = (0, 255, 0)
        lineColour = (0, 255, 0)
    else:
        circleColour = (0, 0, 0)
        lineColour = (0, 0, 0)

def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
    global refPt
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        if not refPt:
            getText()
            colourChange(keep)
        refPt.append((x, y))
        cv2.circle(image, (x, y), 5, circleColour, -1)
        if len(refPt) > 1:
            cv2.line(image, refPt[-2], refPt[-1], lineColour, 2)
	# check to see if the left mouse button was released
    if event == cv2.EVENT_RBUTTONDOWN:
        if len(refPt) > 1:
            cv2.line(image, refPt[-1], refPt[0], lineColour, 2)
        pts_keep.append((refPt, keep))
        refPt = []
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
        header = ['Image name', 'List of (Coordinates, Keep)']
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
        if len(pts_keep) > 0:
            with open('points.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                row = [args["image"], pts_keep]
                writer.writerow(row)
        break

# close all open windows
cv2.destroyAllWindows()
