"""
Main class Game to control all games

"""

from constants import *
from Creature import *
from platforms import *
import random
import time


class Game():
    highest_score = 0

    def __init__(self):
        self.time = time.time()
        self.score = 0
        self.speed = 1
        self.play = False
        self.king = King(RESX / 2, RESY - KING_SIZE/2, 3, KING_SIZE/2, RESY - KING_SIZE/2, 12, PATH + "/images/king0.png", PATH + "/images/king1.png", PATH + "/images/king0.png", PATH + "/images/king0.png")

        # decide a music
        # self.bg_music

        # back ground image managements
        self.imgnum = -1
        self.phase = -1
        # self.bg_imgs = []
        # for i in range(NUM_BG_IMGS):
        #     self.bg_imgs.append(
        #         loadImage(PATH + "/images/bg" + str(i) + ".png"))

        self.bg_img = loadImage(PATH + "/images/bg_long.png")
        self.y_position = - (self.bg_img.height - RESY)
        # platform creations
        Game.createPlatforms(self)

        # magma
        self.magma_img = loadImage(PATH + '/images/magma.png')
        self.magma_height = 10
        self.magma_speed = 1


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


    def check_new_platform(self, now, prev):
        '''
        Just make it working for now,
        but the logic needs to be improved
        (more development with Line's logic probably)
        '''

        # restrict them inside the game width
        if (now.x - now.w / 2 < GAMEX_L or now.x + now.w / 2 > GAMEX_R):
            return False

        DistanceX = abs(prev.x - now.x)
        DistanceY = (prev.y - prev.h / 2) - (now.y - now.h / 2)
        if 0 < DistanceX < RESX / 2 and 0 < DistanceY < RESY / 2:
            print(now.x, now.y, now.w, now.h)
            return True

        # level = 1
        # if (0.3 * tanh(level) * RESX < DistanceX < 0.6 * tanh(level) * RESX
        #         and 0.3 * tanh(level) * RESX/2 < DistanceX < 0.6 * tanh(level) * RESX/2):
        #     return True
        return False


    def createPlatforms(self):
        '''
        Creating a whole set of platform
        needs improvement in random.randint() as it takes a long time
        '''

        self.platforms = []
        prev_y = RESY

        for num in range(5): #question: gap determined on player location or platform location?

            CONDITION_METS = False

            # until it creates a appropriate platform
            while not CONDITION_METS:
                # in the game range
                x = random.randint(GAMEX_L, GAMEX_R)
                # higher y position than the previous one
                y = random.randint(prev_y - 100, prev_y)
                w = random.randint(50, 200)
                h = random.randint(20, 50)
                # instantiate Platform class
                newPlatform = Platform(x, y, w, h)

                # condition check
                # if the first platform
                if not self.platforms:
                    CONDITION_METS = True
                # else, check with the previous one
                else:
                    CONDITION_METS = self.check_new_platform(newPlatform, self.platforms[-1])

            # store the previous y position
            prev_y = y
            # append appropriate platform to the platform list
            self.platforms.append(newPlatform)


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
        self.y_position += self.speed
        image(self.bg_img, 0, self.y_position, RESX, self.bg_img.height)

        # 3. display platforms
        # create random platforms
        # if new_phase:
        #     Game.createPlatforms()
        for platform in self.platforms:
            platform.y += self.speed
            platform.display()

        # 7. display the magma
        # self.magma_height += self.magma_speed
        image(self.magma_img, 0, RESY - self.magma_height, RESX, RESY - self.magma_height)

        # 2. displaying side boundries
        bottom = 0
        while bottom < RESY:
            img = loadImage(PATH + "/images/sidebrick0.png")
            # display at the edge of the screen
            image(img, 0, bottom, GAMEX_L, GAMEX_L * img.height / img.width)
            image(img, GAMEX_R, bottom, GAMEX_L,
                  GAMEX_L * img.height / img.width)
            bottom += GAMEX_L * img.height / img.width

        # 4. display life left
        yposition = GAMEX_L * 0.5
        for life in range(self.king.life):
            heart = loadImage(PATH + "/images/heart.png")
            image(heart, GAMEX_R + (GAMEX_L * 0.2), yposition, GAMEX_L * 0.6,
                  GAMEX_L * 0.6)
            yposition += GAMEX_L

        # 5. display the king
        self.king.y_position += self.speed
        self.king.display(self.platforms)

        # 6. display the game timer
        time_passed = int(floor(time.time() - self.time))
        minutes = '0' + str(time_passed // 60)
        seconds = '0' + str(time_passed % 60)
        textAlign(LEFT, TOP)
        text(minutes[-2:] + ":" + seconds[-2:], 10, 10)
