import numpy as np
import cv2
import matplotlib.pyplot as plt
from copy import deepcopy
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import readmovie
import os
import classes.annotation as annotation
import glob
import showimage

global g_x, g_y
g_x, g_y = 0, 0
def onMouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(flames.shape)
        global g_x, g_y
        g_x, g_y = x, y
        print(x, y)
        print(flames[0][y][x])

## 画像取得
datapath = '.\\data.npy'
with tf.device('/cpu:0'):
    if (os.path.exists(datapath)):
        flames = np.load(datapath)
        print('VideoData Load')
    else:
        moviefoledapath = '.\\video\\*.mp4'
        movies = glob.glob(moviefoledapath)
        flames = []
        for moviepath in movies:
            movie = readmovie.ReadMovie(moviepath, 0.3)
            if len(flames) == 0:
                flames = movie.readvideo()
            else:
                moveis = movie.readvideo()
                flames = np.concatenate([flames, moveis])
        flames = np.array(flames)
        np.save(datapath, flames)
        print('VideoData Save')

# cv2.imshow('Select Color', flames[0])
# cv2.setMouseCallback('Select Color', onMouse)
# cv2.waitKey()
print(g_x, g_y)

index = 300

np.random.shuffle(flames)
for flame in flames:
    index = index + 1
    if (index == 601):
        break

    image = flame
    # 学習データとして画像を保存
    path = f'.\\datasets\\images\\img_{index}.jpg'
    cv2.imwrite(path, flame)
    ## 事前処理 
    if image.dtype == 'uint16':
        image = (image/256).astype('uint8')

    # 色を中和
    shifted = cv2.pyrMeanShiftFiltering(image, 21, 41)

    cv2.imwrite('.\\check\\{:d}.jpg'.format(index), shifted)
    # モノクロ変換
    gray   = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('.\\check\\{:d}_gray.jpg'.format(index), gray)
    thresh = cv2.threshold(gray, 0, 255,
                        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # 確認用にモノクロ画像を3chに変換
    thresh = np.stack((thresh,)*3, -1)

    ## 背景が白か黒か取得

    ## 背景が白なら'0'、黒なら'255'
    obj = np.where(thresh == 0)

    ## 物体が存在するであろう範囲の上下左右の最大値を取得
    bottom = round(np.max(obj[0]))
    head   = round(np.min(obj[0]))
    right  = round(np.max(obj[1]))
    left   = round(np.min(obj[1]))

    # アノテーションを算出
    height       = image.shape[0]
    width        = image.shape[1]
    Yheight      = bottom - head
    Xwidth       = right - left
    anchorheight = '{:.6f}'.format(Yheight / height)
    anchorwidth  = '{:.6f}'.format(Xwidth / width)
    x            = (right + left) / 2
    y            = (bottom + head) / 2
    anchorY      = '{:.6f}'.format(y / height)
    anchorX      = '{:.6f}'.format(x / width)
    # 入力値もしくは画像の名前とかにする
    classname = 'suzuka'

    imgannotation = annotation.Annotation(
        1, classname, anchorX, anchorY, anchorwidth, anchorheight)
    name = f'img_{index}'
    filepath = (f'.\\datasets\\labels\\{name}.txt')
    imgannotation.OutputTxt(filepath)
    showimage.sircleAndrectangle(
        image, round(x), round(y), left, head, right, bottom, name)
