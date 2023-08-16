import numpy as np
import cv2
import glob
# 画像を読み込む
classname = 0
clippingpath = f'.\\datasets\\images\\*.jpg'
clipping = glob.glob(clippingpath)
index = 0
for pathcl in clipping:
    index = index + 1
    if index == 1:

        img = cv2.imread(pathcl)

        img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_HSV = cv2.GaussianBlur(img_HSV, (9, 9), 3)

        # 白のHSV範囲
        lower_white = np.array([0,0,100])
        upper_white = np.array([180,45,255])
    
        # 白以外にマスク
        mask_white = cv2.inRange(img_HSV, lower_white, upper_white)
        res_white = cv2.bitwise_and(img,img, mask= mask_white)
    
        cv2.imshow('window', res_white)
        cv2.waitKey(0)
