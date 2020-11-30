"""
Main class Game to control all games

"""

from constants import *
from Creature import *
import random
import time


class Game():
    highest_score = 0

    def __init__(self):
        self.time = time.time()
        self.score = 0
        self.gravity = 0
        self.play = False
        # image mode Center
        self.king = King(RESX / 2, RESY - KING_SIZE/2, 3, KING_SIZE/2, RESY - KING_SIZE/2, 12, PATH + "/images/king0.png", PATH + "/images/king0.png", PATH + "/images/king0.png", PATH + "/images/king0.png")
        # termporal variable for king
        self.tmp = 0

        # decide a music
        # self.bg_music

        # back ground image managements
        self.imgnum = -1
        self.phase = -1
        self.bg_imgs = []
        for i in range(NUM_BG_IMGS):
            self.bg_imgs.append(
                loadImage(PATH + "/images/bg" + str(i) + ".png"))

        # platform creations
        self.platforms = []
        # Game.create_platforms(self)

    def startup(self):
        '''
        Display the startup screen
        '''

        image(loadImage(PATH + "/images/bg0.png"), 0, 0, width, height)
        imageMode(CENTER)
        logo = loadImage(PATH + "/images/logo.png")
        image(logo, width / 2, height * 2 / 5, width * 5 / 6,
              (width * 5 / 6) * logo.height / logo.width)
        imageMode(CORNER)
        fill(255)
        textAlign(CENTER)
        font = createFont("3270SemiNarrow", floor(RESX * 0.03))
        textFont(font)
        text("Click Anywhere to Start", width / 2, height * 3 / 4)
        img = loadImage(PATH + "/images/king0.png")
        image(img, KING_SIZE, RESY - KING_SIZE * 1.5, KING_SIZE * 1.5,
              KING_SIZE * 1.5, 0, 0, img.width, img.height)

    def gameover(self):
        '''
        Display the game over screen
        '''
        image(loadImage(PATH + "/images/bg0.png"), 0, 0, width, height)
        imageMode(CENTER)
        logo = loadImage(PATH + "/images/gameover.png")
        image(logo, width / 2, height * 1 / 5, width * 5 / 6,
              (width * 5 / 6) * logo.height / logo.width)
        imageMode(CORNER)
        fill(255)
        textAlign(CENTER)
        font = createFont("3270SemiNarrow", floor(RESX * 0.04))
        textFont(font)
        text("Your Score", width / 2, height * 2 / 5)
        textSize(floor(RESX * 0.03))
        text(str(self.score), width / 2, height * 3 / 5)
        img = loadImage(PATH + "/images/king7.png")
        image(img, KING_SIZE, RESY - KING_SIZE * 1.5, KING_SIZE * 1.5,
              KING_SIZE * 1.5, 0, 0, img.width, img.height)


    def new_phase(self):
        '''
        Calculate a num of bg_img and the phase
        Return if the bg_img has changed
        '''
        # calculate bg_img to display
        imgnum = self.king.x_position // RESX

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
        0. game over display
        1. display the background
        2. display side boundry
        3. display platform (call .display())
        4. display life left
        5. display king (call .display())
        6. display the game time
        '''

        # 0. if the game is over
        if not self.king.alive:
            self.gameover()
            return

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
            # display at the edge of the screen
            image(img, 0, bottom, GAMEX_L, GAMEX_L * img.height / img.width)
            image(img, GAMEX_R, bottom, GAMEX_L,
                  GAMEX_L * img.height / img.width)
            bottom += GAMEX_L * img.height / img.width

        # 3. display platforms
        # create random platforms
        # if new_phase:
        #     Game.create_platforms()
        # for platform in self.platforms:
        #   platform.display()

        # 4. display life left
        yposition = GAMEX_L * 0.5
        for life in range(self.king.life):
            heart = loadImage(PATH + "/images/heart.png")
            image(heart, GAMEX_R + (GAMEX_L * 0.2), yposition, GAMEX_L * 0.6,
                  GAMEX_L * 0.6)
            yposition += GAMEX_L

        # 5. display king (just a imgage for now)
        self.king.display()

        # 6. display the game time
        time_passed = int(floor(time.time() - self.time))
        minutes = '0' + str(time_passed // 60)
        seconds = '0' + str(time_passed % 60)
        textAlign(LEFT, TOP)
        text(minutes[-2:] + ":" + seconds[-2:], 10, 10)
