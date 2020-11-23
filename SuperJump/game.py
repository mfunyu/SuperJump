"""
Main class Game to control all games

"""

from constants import *

import random


class Game():

    def __init__(self):
        self.score = 0
        self.gravity = 0

        #self.king = King()
        self.p = 0

        # self.bg_music =

        #
        self.imgnum = -1
        self.bg_imgs = []
        for i in range(NUM_BG_IMGS):
            self.bg_imgs.append(loadImage(PATH + "/images/bg" + str(i) + ".png"))

        self.platforms = []

        # decide numbers of platforms
        # num_pl = random.randint(4,8)
        # append platform instance anonimously {num_pl} times
        # for i in range(num_pl):
            # self.platforms.append(Platform())


    def new_phase(self):
        # calculate phase
        phase = self.p // RESX

        # calculate bg_img to display
        imgnum = phase // NUM_IMG_DIV
        if imgnum > self.imgnum:
            # show last img for the exceeded part
            self.imgnum = min([imgnum, NUM_BG_IMGS - 1])
            print(self.imgnum)
            return True

        # imgpart = phase % NUM_IMG_DIV
        # imgpart
        # +---------------+
        # | {NUM_IMG_DIV} |
        # +---------------+
        # |  :            |
        # +---------------+
        # |  1            |
        # +---------------+
        # |  0            |
        # +---------------+

        return False

    def display(self):

        # find bg_imgs by the position of the king
        new_phase = Game.new_phase(self):

        # imgnum, imgpart = Game.decide_bg_imgs(self)

        # display back ground images (at the very back)
        img = self.bg_imgs[self.imgnum]

        # imgstart = (img.height / NUM_IMG_DIV) * (NUM_IMG_DIV -1 - imgpart)
        # imgend = imgstart + (img.height / NUM_IMG_DIV)
        # image(img, 0, 0, width, height, 0, imgstart, img.width, imgend)
        image(img, 0, 0, width, height)

        # display king (for now circle)
        fill(255)
        circle(100, RESY - self.p % RESX, 20)

        # create random platforms
        if new_phase:
            
