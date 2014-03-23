#!/usr/bin/env python

"""
Swaps frontal faces in an image.
Pranav Ravichandran <me@onloop.net>
"""

usage = "Usage: python faceswapper.py <source_image> <image_to_write_to>"

import cv
from PIL import Image, ImageFilter
from random import choice

import os
import sys

class FaceSwapper:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.source_cv = cv.LoadImage(source)
        self.source_pil = Image.open(source)
        self.coords_list = []
        self.count = 0

    def extract_faces(self):
        ''' Load Haar cascade, detect faces and save them to individual images. '''
        haar_cascade = cv.Load('./haarcascade_frontalface_alt.xml')
        storage = cv.CreateMemStorage()
        faces = cv.HaarDetectObjects(self.source_cv, haar_cascade, storage, min_neighbors = 3)
        if faces:
            for face in faces:
                cv.SetImageROI(self.source_cv, face[0])
                region_image = cv.CreateImage(cv.GetSize(self.source_cv),
                                              self.source_cv.depth, self.source_cv.nChannels)
                cv.ResetImageROI(self.source_cv)

                cv.SetImageROI(self.source_cv, faces[self.count][0])
                target_region = cv.CreateImage(cv.GetSize(self.source_cv),
                                               self.source_cv.depth, self.source_cv.nChannels)

                cv.Copy(self.source_cv, target_region, None)
                cv.ResetImageROI(self.source_cv)

                cv.SaveImage(str(self.count) + ".jpg", target_region)
                self.count += 1

                self.coords_list.append((face[0][0], face[0][1]))

    def swap_images(self):
        ''' Overlay saved faces randomly on the positions of the faces on the source image. '''
        for face_count in range(self.count):
            temp_list = self.coords_list[:face_count] + self.coords_list[face_count+1:]
            coords = choice(temp_list)
            self.source_pil.paste(Image.open(str(face_count) + ".jpg"), coords)
            os.remove(str(face_count) + ".jpg")

    def save_final(self):
        ''' Save the final, faceswapped image. '''
        self.source_pil.save(self.target, "JPEG")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print usage
        sys.exit()

    image_to_read_from = str(sys.argv[1])
    image_to_write_to = str(sys.argv[2])

    faceswapper_obj = FaceSwapper(image_to_read_from, image_to_write_to)
    faceswapper_obj.extract_faces()
    faceswapper_obj.swap_images()
    faceswapper_obj.save_final()
