import csv
import cv2
import os

with open('points.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)
    for row in csv_reader:
        points = row[-1]
        points = eval(points)
        imagename = row[0]
        image = cv2.imread(imagename)
        for point in points:
            cv2.circle(image, point, 5, (255, 255, 255), -1)
        if len(points) > 1:
            for i in range(len(points)):
                if i == len(points) - 1:
                    cv2.line(image, points[i], points[0], (0, 0, 0), 2)
                else:
                    cv2.line(image, points[i], points[i+1], (0, 0, 0), 2)
        if not os.path.isdir("Output"):
            os.makedirs("Output")
        cv2.imwrite("Output/" + imagename, image)