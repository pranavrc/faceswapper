import cv
from PIL import Image, ImageFilter
from random import choice
from os import remove

targetImage = cv.LoadImage('sample.jpg')
haarCascade = cv.Load('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
storage = cv.CreateMemStorage()
Faces = cv.HaarDetectObjects(targetImage, haarCascade, storage, min_neighbors = 3)
count = 0
coordsList = []

if Faces:
	for face in Faces:
		#cv.Rectangle(targetImage, (face[0][0], face[0][1]), (face[0][0] + face[0][2], face[0][1] + face[0][3]), RGB(155, 255, 25), 2)
		cv.SetImageROI(targetImage, face[0])
		regionImage = cv.CreateImage(cv.GetSize(targetImage), targetImage.depth, targetImage.nChannels)
		cv.Copy(targetImage, regionImage, None)
		cv.ResetImageROI(targetImage)
		cv.SetImageROI(targetImage, Faces[count][0])
		targetRegion = cv.CreateImage(cv.GetSize(targetImage), targetImage.depth, targetImage.nChannels)
		cv.Copy(targetImage, targetRegion, None)
		cv.ResetImageROI(targetImage)
		cv.SaveImage(str(count) + ".jpg", targetRegion)
		count += 1
		coordsList.append((face[0][0], face[0][1]))

parentImage = Image.open("sample.jpg")

for i in range(count):
	tempList = coordsList[:i] + coordsList[i+1:]
	coords = choice(tempList)
	parentImage.paste(Image.open(str(i) + ".jpg"), coords)
	coordsList.remove(coords)
	remove(str(i) + ".jpg")
	
parentImage.save("swapped.jpg", "JPEG")

#NamedWindow('Face Detection', CV_WINDOW_NORMAL)
#ShowImage('Face Detection', targetImage) 
#cv.WaitKey()
