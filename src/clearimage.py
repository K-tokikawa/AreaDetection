import glob
import cv2
import random
import classes.annotation as annotation
import showimage
import numpy as np
import statistics
from PIL import Image, ImageTk, ImageDraw
import tkinter
from tkinter import messagebox
import colorsys

# ドラッグ開始した時のイベント - - - - - - - - - - - - - - - - - - - - - - - - - - 
def start_point_get(event):
    global start_x, start_y # グローバル変数に書き込みを行なうため宣言
    canvas1.delete("rect1")  # すでに"rect1"タグの図形があれば削除
    # canvas1上に四角形を描画（rectangleは矩形の意味）
    canvas1.create_rectangle(event.x,
                            event.y,
                            event.x + 1,
                            event.y + 1,
                            outline="red",
                            tag="rect1")
    # グローバル変数に座標を格納
    start_x, start_y = event.x, event.y

# ドラッグ中のイベント - - - - - - - - - - - - - - - - - - - - - - - - - - 
def rect_drawing(event):
    # ドラッグ中のマウスポインタが領域外に出た時の処理
    if event.x < 0:
        end_x = 0
    else:
        end_x = min(img.width, event.x)
    if event.y < 0:
        end_y = 0
    else:
        end_y = min(img.height, event.y)
    canvas1.coords("rect1", start_x, start_y, end_x, end_y)

def release_action(event):
    # "rect1"タグの画像の座標を元の縮尺に戻して取得
    global start_x, start_y, end_x, end_y
    start_x, start_y, end_x, end_y = [
        round(n) for n in canvas1.coords("rect1")
    ]
    ret = messagebox.askyesno('確認', '処理を開始しますか？')
    if ret:
        canvas1.destroy()
        root.destroy()
def animate():
    global k
    k = 1 - k
    root.after(200, animate)
def OutputTxt(value, filepath):
    f = open(filepath, 'a')
    with f:
        f.write(value+'\n')
color = None
classname = 0
clippingpath = f'.\\clipping\\{classname}\\*.jpg'
clipping = glob.glob(clippingpath)
index = 0
for pathcl in clipping:
    index = index + 1
    if index == 1:
        k = 0
        root = tkinter.Tk()
        root.geometry("1400x1000")
        img_org = Image.open(pathcl)
        img = img_org.resize(size=(int(img_org.width * 5),
                            int(img_org.height * 5)),
                        resample=Image.BILINEAR)
        img_tk = ImageTk.PhotoImage(img)
        canvas1 =  tkinter.Canvas(root, width=img.width, height=img.height)
        img_can = canvas1.create_image(0, 0, image=img_tk, anchor=tkinter.NW)
        # Canvasウィジェットを配置し、各種イベントを設定
        canvas1.grid()
        canvas1.bind("<ButtonPress-1>", start_point_get)
        canvas1.bind("<Button1-Motion>", rect_drawing)
        canvas1.bind("<ButtonRelease-1>", release_action)
        root.after(200, animate)
        canvas1.mainloop()
        global start_x, start_y, end_x, end_y
        widthrange = range(int(start_x), int(end_x))
        heightrange = range(int(start_y), int(end_y))
        imgcl = cv2.imread(pathcl)
        imgcl = cv2.resize(imgcl, (img.width, img.height))

        target_colors = []
        for x in widthrange:
            for y in heightrange:
                B,G,R=imgcl[y,x,:]
                hsv = colorsys.rgb_to_hsv(B/255, G/255, R/255)
                target_colors.append(hsv)
        print(len(target_colors))
        target_colors = set(target_colors)
        print(len(target_colors))
        for color in target_colors:
            color = (int(color[0]), int(color[1]), int(color[2]))

        cv2.imshow('window', imgcl)
        cv2.waitKey(0)