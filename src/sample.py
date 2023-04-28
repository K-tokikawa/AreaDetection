import numpy as np
import cv2
import matplotlib.pyplot as plt
from copy import deepcopy
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import readmovie
import os

## 画像取得
datapath = '.\\data.npy'
with tf.device('/cpu:0'):
    if (os.path.exists(datapath)):
        flames = np.load(datapath)
        print('VideoData Load')
    else:
        moviepath = '.\\1321799717.mp4'
        movie = readmovie.ReadMovie(moviepath, 0.3)
        flames = movie.readvideo()
        print(type(flames))
        print(type(flames[0]))
        np.save(datapath, flames)
        print('VideoData Save')

index = 0
for flame in flames:
    index = index + 1
    image = cv2.imread(".\\img\\1949318870.jpg")
    image = flame
    
    ## 事前処理 

    # 色を中和
    if image.dtype == 'uint16':
        image = (image/256).astype('uint8')
    shifted = cv2.pyrMeanShiftFiltering(image, 21, 41)
    # モノクロ変換
    gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255,
                        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


    # 確認用にモノクロ画像を3chに変換
    thresh = np.stack((thresh,)*3, -1)

    ## 背景が白か黒か取得

    ## 背景が白なら'0'、黒なら'255'
    obj = np.where(thresh == 0)

    ## 物体が存在するであろう範囲の上下左右の最大値を取得
    bottom = round(np.max(obj[0]) * 1.1)
    head   = round(np.min(obj[0]) * 0.9)
    right  = round(np.max(obj[1]) * 1.1)
    left   = round(np.min(obj[1]) * 0.9)

    # アノテーションを算出
    height = image.shape[0]
    width = image.shape[1]
    Yheight = bottom - head
    Xwidth = right - left
    anchorheight = '{:.2f}'.format(Yheight / height)
    anchorwidth = '{:.2f}'.format(Xwidth / width)
    x = (right + left) / 2
    y = (bottom + head) / 2
    anchorY = '{:.2f}'.format(y / height)
    anchorX = '{:.2f}'.format(x / width)

    ## 矩形を描画
    cv2.circle(image, (round(width * float(anchorX)), round(height * float(anchorY))), 10, (255, 255, 255),
               thickness=3, lineType=cv2.LINE_AA)
    cv2.rectangle(image, (left, head), (right, bottom),(255, 255, 0))
    cv2.imshow('Image', image)
    cv2.waitKey()

    ## 確認用 モノクロ画像と並べて表示
    if index % 30 == 0:
        mergeImg = np.hstack((image, thresh))
        path = '.\\sample\\{:d}.jpg'.format(index)
        cv2.imwrite(path, mergeImg)
