class Annotation:
    def __init__(self, classno, classname, anchorX, anchorY, anchorwidth, anchorheight) -> None:
        self.classNo = classno
        self.classname = classname
        self.anchorX = anchorX
        self.anchorY = anchorY
        self.anchorwidth = anchorwidth
        self.anchorheight = anchorheight

    def Classname(self):
        return self.classname

    def AnchorX(self):
        return self.anchorX

    def AnchorY(self):
        return self.anchorY

    def Anchorwidth(self):
        return self.anchorwidth

    def Anchorheight(self):
        return self.anchorheight

    def OutputTxt(self, filepath):
        f = open(filepath, 'x')
        with f:
            value = f'{self.classNo} {self.anchorX} {self.anchorY} {self.anchorwidth} {self.anchorheight}\n'
            f.write(value)
