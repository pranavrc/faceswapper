from cv import *
from PIL import *
from PIL import Image, ImageFilter
from random import choice
from os import remove

targetImage = LoadImage('sample.jpg')
haarCascade = Load('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
storage = CreateMemStorage()
Faces = HaarDetectObjects(targetImage, haarCascade, storage, min_neighbors = 3)
count = 0
coordsList = []

if Faces:
	for face in Faces:
		#Rectangle(targetImage, (face[0][0], face[0][1]), (face[0][0] + face[0][2], face[0][1] + face[0][3]), RGB(155, 255, 25), 2)
		SetImageROI(targetImage, face[0])
		regionImage = CreateImage(GetSize(targetImage), targetImage.depth, targetImage.nChannels)
		Copy(targetImage, regionImage, None)
		ResetImageROI(targetImage)
		SetImageROI(targetImage, Faces[count][0])
		targetRegion = CreateImage(GetSize(targetImage), targetImage.depth, targetImage.nChannels)
		Copy(targetImage, targetRegion, None)
		ResetImageROI(targetImage)
		SaveImage(str(count) + ".jpg", targetRegion)
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
WaitKey()
