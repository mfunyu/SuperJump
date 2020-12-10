from constants import *

class Platform():
    def __init__(self, x, y, w, h, mark, num_frames = 10):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.num_frames = num_frames
        
        
        self.img0 = loadImage(PATH + "/images/brick0.png")
        self.img1 = loadImage(PATH + "/images/brick1.png")
        self.img2 = loadImage(PATH + "/images/magma.png")
        self.frame = 0
        self.mark = mark

    def display(self): #syntax: image(img, x, y, width, height, x1, y1, x2, y2)
        imageMode(CENTER)
        if self.mark == 1:
            image(self.img1, self.x, self.y, self.w, self.h)
        elif self.mark == 2:
            image(self.img2, self.x, self.y, self.w, self.h)
        else:
            image(self.img0, self.x, self.y, self.w, self.h)
        imageMode(CORNER)
