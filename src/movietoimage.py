import numpy as np
import cv2
from copy import deepcopy
import tensorflow as tf
import readmovie
import classes.annotation as annotation
import glob

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
with tf.device('/cpu:0'):
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
    print('VideoData Save')

index = 0
for flame in flames:
    index = index + 1
    if (index == 601):
        break

    image = flame
    # 学習データとして画像を保存
    path = f'.\\image\\img_{index}.jpg'
    cv2.imwrite(path, flame)