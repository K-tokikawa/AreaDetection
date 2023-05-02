import cv2
import numpy as np
# ## 矩形を描画


def sircleAndrectangle(image, x, y, left, head, right, bottom):
    cv2.circle(image, (x, y), 10, (255, 255, 255),
            thickness=3, lineType=cv2.LINE_AA)
    cv2.rectangle(image, (left, head), (right, bottom), (255, 255, 0))
    cv2.imshow('Image', image)
    cv2.waitKey()


# 確認用 モノクロ画像と並べて表示
def lineup_grayAndoriginal(image, thresh):
    mergeImg = np.hstack((image, thresh))
    cv2.imshow('Image', mergeImg)
