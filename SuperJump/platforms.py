from constants import *

class Platform():
    def __init__(self, x, y, w, h, num_frames = 10):
        self.x = x
        self.y = y
        #note that these are the cordinates when they are born, not when
        self.w = w
        self.h = h
        self.img = loadImage(PATH + "/images/brick0.png")
        self.num_frames = num_frames

        self.vy = 0
        self.frame = 0
        self.level = 0
        #self.dir = RIGHT??

    def drop(self):#set difficulty
        self.vy = self.level
        self.level += 1

        #make the creature land on a platform?

    def update(self):
        self.drop()
        self.y += self.vy

    def display(self):
        # coment out for now
        # self.update()

        #syntax: image(img, x, y, width, height, x1, y1, x2, y2)
        imageMode(CENTER)
        image(self.img, self.x, self.y, self.w, self.h)
        imageMode(CORNER)
