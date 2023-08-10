import glob
import cv2
import random
import classes.annotation as annotation
import showimage
classname = 0
clippingpath = f'.\\clipping\\{classname}\\*.jpg'
clipping = glob.glob(clippingpath)
backgroundpath = '.\\image\\*.jpg'
background = glob.glob(backgroundpath)

def overlay(fore_img, back_img, shift):
 
    '''
    fore_img：合成する画像
    back_img：背景画像
    shift：左上を原点としたときの移動量(x, y)
    '''
 
    shift_x, shift_y = shift
 
    fore_h, fore_w = fore_img.shape[:2]
    fore_x_min, fore_x_max = 0, fore_w
    fore_y_min, fore_y_max = 0, fore_h
 
    back_h, back_w = back_img.shape[:2]
    back_x_min, back_x_max = shift_x, shift_x+fore_w
    back_y_min, back_y_max = shift_y, shift_y+fore_h

 
    if back_x_min < 0:
        fore_x_min = fore_x_min - back_x_min
        back_x_min = 0
         
    if back_x_max > back_w:
        fore_x_max = fore_x_max - (back_x_max - back_w)
        back_x_max = back_w
 
    if back_y_min < 0:
        fore_y_min = fore_y_min - back_y_min
        back_y_min = 0
         
    if back_y_max > back_h:
        fore_y_max = fore_y_max - (back_y_max - back_h)
        back_y_max = back_h
 
    back_img[back_y_min:back_y_max, back_x_min:back_x_max] = fore_img[fore_y_min:fore_y_max, fore_x_min:fore_x_max]
 
    return back_img
index = 0
if classname == 1:
    index = 300
for pathcl in clipping:
    index += 1
    imgcl = cv2.imread(pathcl)
    pathback = random.choice(background)
    imgback = cv2.imread(pathback)

    shift_x = random.randint(0, round(imgback.shape[1] - imgcl.shape[1]))
    shift_y = random.randint(0, round(imgback.shape[0] - imgcl.shape[0]))

    imgback = overlay(imgcl, imgback, (shift_x, shift_y))
    height       = imgback.shape[0]
    width        = imgback.shape[1]
    Yheight      = imgcl.shape[0]
    Xwidth       = imgcl.shape[1]
    anchorheight = '{:.6f}'.format(Yheight / height)
    anchorwidth  = '{:.6f}'.format(Xwidth / width)
    x            = shift_x + Xwidth / 2
    y            = shift_y + Yheight / 2
    anchorY      = '{:.6f}'.format(y / height)
    anchorX      = '{:.6f}'.format(x / width)
    imgannotation = annotation.Annotation(
        1, "", anchorX, anchorY, anchorwidth, anchorheight)
    filename = f"{index}"
    txtfilepath = f'.\\synthesis\\label\\img_{filename}.txt'
    imgannotation.OutputTxt(txtfilepath)

    imgfilepath = f'.\\synthesis\\image\\img_{filename}.jpg'
    cv2.imwrite(imgfilepath, imgback)

    showimage.sircleAndrectangle(
        imgback, round(x), round(y), shift_x, shift_y, shift_x + Xwidth, shift_y + Yheight, filename)
    # print(imgback.shape)
    # cv2.imshow('img',imgback)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
