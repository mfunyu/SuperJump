from constants import *

class Platform():
    def __init__(self, x, y, w, h, num_frames = 10):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.num_frames = num_frames

        self.img = loadImage(PATH + "/images/brick0.png")
        self.frame = 0

    def display(self): #syntax: image(img, x, y, width, height, x1, y1, x2, y2)
        imageMode(CENTER)
        image(self.img, self.x, self.y, self.w, self.h)
        imageMode(CORNER)
