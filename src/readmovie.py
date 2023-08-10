import cv2
import numpy as np
import tensorflow as tf
import time
class ReadMovie:
    def __init__(self, path, sizerate):
        self.path = path
        self.video = cv2.VideoCapture(path)
        self.flamecount = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.WIDTH  = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.HEIGHT = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.size = sizerate
    def readvideo(self):
        index = 0
        flames = []
        while True:
            ret, flame = self.video.read()

            if ret:
                if self.size != None:
                    flame = cv2.resize(flame, (432, 324))
                flames.append( flame)
                if index == 1:
                    mergeImg = np.hstack((flame, flames[index]))
                index = index + 1
            else :
                break
        flames = np.array(flames)
        return flames