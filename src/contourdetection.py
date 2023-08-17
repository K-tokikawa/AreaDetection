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
    if True:

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
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # thresh = 255 - thresh
        mask = np.all(img[:,:,:] == [255, 255, 255], axis=-1)
        dst = cv2.cvtColor(thresh, cv2.COLOR_BGR2BGRA)
        dst[mask,3] = 0
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        img = cv2.add(dst, img)
        cv2.imwrite("dst.png", dst)

        # 輪郭を画像に書き込む
        output = cv2.drawContours(img, contours, -1, (0,255,0), 3)
        cv2.imwrite(f'.\\clear\\img_{index}.png', img)
        # cv2.imshow('window', img)
        # cv2.waitKey(0)
