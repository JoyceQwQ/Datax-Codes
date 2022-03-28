import csv
import cv2
import os

circleColour = None
lineColour = None

def colourChange(keep):
    global circleColour, lineColour
    if keep:
        circleColour = (0, 255, 0)
        lineColour = (0, 255, 0)
    else:
        circleColour = (0, 0, 0)
        lineColour = (0, 0, 0)

with open('points.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)
    for row in csv_reader:
        polygons = row[-1]
        polygons = eval(polygons)
        imagename = row[0]
        image = cv2.imread(imagename)
        for polygon in polygons:
            points, keep = polygon
            colourChange(keep)
            for point in points:
                cv2.circle(image, point, 5, circleColour, -1)
            if len(points) > 1:
                for i in range(len(points)):
                    if i == len(points) - 1:
                        cv2.line(image, points[i], points[0], lineColour, 2)
                    else:
                        cv2.line(image, points[i], points[i+1], lineColour, 2)
            if not os.path.isdir("Output"):
                os.makedirs("Output")
            cv2.imwrite("Output/" + imagename, image)
