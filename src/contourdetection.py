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
        img_ = cv2.cvtColor(res_white, cv2.COLOR_HSV2BGR)

        gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
        ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
        thresh = 255 - thresh
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 輪郭を画像に書き込む
        output = cv2.drawContours(img, contours, -1, (0,255,0), 3)

        cv2.imshow('window', output)
        cv2.waitKey(0)
        # # 画像のグレースケール化
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # # 画像の白黒2値化
        # ret, thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)

        # # 輪郭を抽出する
        # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # # 輪郭を画像に書き込む
        # output = cv2.drawContours(img, contours, -1, (0,255,0), 2)
        # cv2.imshow('window', output)
        # cv2.waitKey(0)