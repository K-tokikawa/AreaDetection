import glob
import shutil

textpath = '.\\datasets\\labelimg\\*.txt'
files = glob.glob(textpath)
slectfile = []
for file in files:
    aryfilepath = file.split("\\")
    filename = aryfilepath[len(aryfilepath) - 1].replace('.txt', '')
    imagepath = '.\\datasets\\images\\{}.jpg'.format(filename)
    movepath = '.\\datasets\\image'
    try:
        shutil.move(imagepath, movepath)
    except:
        pass
    slectfile.append(filename)
