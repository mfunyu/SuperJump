from constants import *
import random

class Platform():
    def __init__(self, x, y, w, h, mark, num_frames = 10):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.num_frames = num_frames


        self.img0 = loadImage(PATH + "/images/brick0.png")
        self.img1 = loadImage(PATH + "/images/brick1.png")
        self.img2 = loadImage(PATH + "/images/magma_platform.png")

        self.selection = random.randint(1, 4)
        if self.selection == 1:
            self.img3 = loadImage(PATH + "/images/monster1.png")
        elif self.selection == 2:
            self.img3 = loadImage(PATH + "/images/monster2.png")
        elif self.selection == 3:
            self.img3 = loadImage(PATH + "/images/monster3.png")
        elif self.selection == 4:
            self.img3 = loadImage(PATH + "/images/monster4.png")

        self.frame = 0
        self.mark = mark

    def display(self): #syntax: image(img, x, y, width, height, x1, y1, x2, y2)
        imageMode(CENTER)
        if self.mark == 1:
            image(self.img1, self.x, self.y, self.w, self.h)
        elif self.mark == 2:
            image(self.img2, self.x, self.y, self.w, self.h)
            image(self.img3, self.x, self.y - self.h/2 - 40, 80, 80)

        else:
            image(self.img0, self.x, self.y, self.w, self.h)
        imageMode(CORNER)

