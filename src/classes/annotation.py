class Annotation:
    def __init__(self, classname, anchorX, anchorY, anchorwidth, anchorheight) -> None:
        self.classNo = 0
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

    def OutputTxt(self, filename):
        filepath = ('.\\datasets\\labels\\{}.txt').format(filename)
        f = open(filepath, 'x')
        with f:
            value = '{0} {1} {2} {3} {4}'.format(
                self.classNo, self.anchorX, self.anchorY, self.anchorwidth, self.anchorheight)
            f.write(value)
