"""
Main class Game to control all games

"""

from constants import *

import random


class Game():
    highest_score = 0

    def __init__(self):
        self.score = 0
        self.gravity = 0
        self.play = False

        #self.king = King()
        # termporal variable for king
        self.tmp = 0

        # decide a music
        # self.bg_music

        # back ground image managements
        self.imgnum = -1
        self.phase = -1
        self.bg_imgs = []
        for i in range(NUM_BG_IMGS):
            self.bg_imgs.append(loadImage(PATH + "/images/bg" + str(i) + ".png"))

        # platform creations
        self.platforms = []
        Game.create_platforms(self)


    def startup(self):
        '''
        Display the startup screen
        '''
        image(loadImage(PATH + "/images/bg0.png"), 0, 0, width, height)
        imageMode(CENTER)
        logo = loadImage(PATH + "/images/logo.png")
        image(logo, width / 2, height * 2/5, width * 5/6, (width * 5/6)*logo.height / logo.width)
        imageMode(CORNER)
        fill(255)
        textAlign(CENTER)
        textSize(20)
        text("Click Anywhere to Start", width / 2 , height * 3/4)
        img = loadImage(PATH + "/images/king0.png")
        image(img, 20, 500, KING_SIZE * 1.5, KING_SIZE * 1.5, 0, 0, img.width, img.height)


    def create_platforms(self):
        '''
        Create a new set of platforms
        '''

        # decide numbers of platforms
        num_pl = random.randint(4, 8)
        # append platform instance anonimously {num_pl} times
        # for i in range(num_pl):
        #     random.randint()
        #     # Platform(x, y)
        #     self.platforms.append(Platform())


    def new_phase(self):
        '''
        Calculate a num of bg_img and the phase
        Return if the bg_img has changed
        '''
        # calculate bg_img to display
        imgnum = self.tmp // RESX

        # show the last img for the exceeded part
        self.imgnum = min([imgnum, NUM_BG_IMGS - 1])
        # calculate a phase
        self.phase = self.imgnum // NUM_PHASE

        # if the bg_img needs to be changed
        if imgnum > self.imgnum:
            return True

        return False

    def display(self):
        '''
        1. display the background
        2. display side boundry
        3. display platform (call .display())
        4. display king (call .display())
        '''

        # 1. display the background
        # check if the bg_img changed
        new_phase = Game.new_phase(self)
        # display back ground image of the current phase(at the very back)
        img = self.bg_imgs[self.imgnum]
        image(img, 0, 0, width, height)

        # 2. displaying side boundries
        bottom = 0
        while bottom < RESY:
            img = loadImage(PATH + "/images/sidebrick0.png")
            image(img, 0, bottom, img.width / 4, img.height / 4)
            image(img, RESX - img.width / 4, bottom, img.width / 4, img.height / 4)
            bottom += img.height / 4

        # 3. display platforms
        # create random platforms
        # if new_phase:
        #     Game.create_platforms()
        # for platform in self.platforms:
        #   platform.display()

        # 4. display king (just a imgage for now)
        # self.king.diplay()
        img = loadImage(PATH + "/images/king0.png")
        image(img, 20, RESY - self.tmp % RESX, KING_SIZE, KING_SIZE, 0, 0, img.width, img.height)
