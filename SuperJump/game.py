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
        self.speed = GAME_SPEED
        self.play = False
        self.king = King(RESX / 2, RESY - KING_SIZE/2, 3, KING_SIZE/2, RESY - KING_SIZE/2, 12, PATH + "/images/king0.png", PATH + "/images/king1.png", PATH + "/images/king0.png", PATH + "/images/king0.png")

        # decide a music
        # self.bg_music

        # back ground image managements
        self.imgnum = -1
        self.phase = -1
        self.bg_imgs = []
        for i in range(NUM_BG_IMGS):
            self.bg_imgs.append(
                loadImage(PATH + "/images/bg" + str(i) + ".png"))
        self.bg_num = 0
        self.y_position = - (self.bg_imgs[0].height - RESY)

        # multiple platform creations

        self.realplatforms = []
        self.midplatform = [RESX/2, RESY/2, 200, 100]
        self.realplatforms.append(Platform(self.midplatform[0], self.midplatform[1], self.midplatform[2], self.midplatform[3]))
        print("The", self.midplatform)
        for single_platform in self.realplatforms:
            print(single_platform.y)
            if single_platform.y >= -(self.bg_imgs[self.bg_num].height - RESY):
                self.create_one_real_platform()


        # magma
        self.magma_img = loadImage(PATH + '/images/magma.png')

        # clouds
        self.cloud_x = 0
        self.cloud_y = 0



    def startup(self):
        '''
        Display the startup screen
        '''

        image(loadImage(PATH + "/images/background.png"), 0, 0, width, height)
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
        image(loadImage(PATH + "/images/background.png"), 0, 0, width, height)
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
        img = loadImage(PATH + "/images/king10.png")
        image(img, KING_SIZE, RESY - KING_SIZE * 1.5, KING_SIZE * 1.5,
              KING_SIZE * 1.5, 0, 0, img.width, img.height)


    def create_one_real_platform(self):
        condition = True

        while condition:
            new_width = random.randint(100, 200)
            new_height = random.randint(50, 100)
            new_x_positive = self.midplatform[0] + self.midplatform[2]+ random.uniform(0.3*tanh(self.speed)*HORIZONTAL_MAX, 0.6*tanh(self.speed)*HORIZONTAL_MAX)
            new_x_negative = self.midplatform[0] - random.uniform(0.3*tanh(self.speed)*HORIZONTAL_MAX, 0.6*tanh(self.speed)*HORIZONTAL_MAX) - new_width
            new_x = random.choice([new_x_positive, new_x_negative])
            new_y = self.midplatform[1] - random.uniform(0.5*tanh(self.speed)*JUMP_HIGHET, 0.8*tanh(self.speed)*JUMP_HIGHET) - new_height

            if GAMEX_L <= new_x - new_width/2 and new_x + new_width/2 <= GAMEX_R:
                condition = False

        print("prevH", self.midplatform[1])
        print("nowH", new_y + new_height)

        self.midplatform[0] = new_x
        self.midplatform[1] = new_y
        self.midplatform[2] = new_width
        self.midplatform[3] = new_height
        print(self.midplatform)
        self.realplatforms.append(Platform(self.midplatform[0], self.midplatform[1], self.midplatform[2], self.midplatform[3]))


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

#         # 0. if the game is over
#         if not self.king.alive:
#             self.gameover()
#             return

        # 1. display the background
        self.y_position += self.speed
        # change to the new background image
        if self.y_position > 0:
            self.realplatforms = []
            self.midplatform = [RESX/2, RESY/2, 200, 100]
            self.realplatforms.append(Platform(self.midplatform[0], self.midplatform[1], self.midplatform[2], self.midplatform[3]))
            print("The", self.midplatform)
            for single_platform in self.realplatforms:
                print(single_platform.y)
                if single_platform.y >= -(self.bg_imgs[self.bg_num].height - RESY):
                    self.create_one_real_platform()
            self.king.reborn(self.realplatforms)
            self.bg_num = min([self.bg_num + 1, NUM_BG_IMGS - 1])
            self.y_position = - (self.bg_imgs[self.bg_num].height - RESY)
        image(self.bg_imgs[self.bg_num], 0, self.y_position, RESX, self.bg_imgs[self.bg_num].height)

        # side
        if self.bg_num == 2:
            cloud = loadImage(PATH + "/images/clouds.png")
            self.cloud_y += self.speed
            self.cloud_x += self.speed * 2
            image(cloud, self.cloud_x, self.cloud_y, cloud.width / 2, cloud.height / 2)

        # 3. display platforms
        # create random platforms
        # if new_phase:
        #     Game.createPlatforms()
        for single_platform in self.realplatforms:
            single_platform.y += self.speed
            single_platform.display()

        # 7. display the magma
        # self.magma_height += self.magma_speed
        image(self.magma_img, 0, RESY - MAGMA_H, RESX, self.magma_img.height)

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
        self.king.display(self.realplatforms)

        # 6. display the game timer
        time_passed = int(floor(time.time() - self.time))
        self.score = time_passed
        minutes = '0' + str(time_passed // 60)
        seconds = '0' + str(time_passed % 60)
        textAlign(LEFT, TOP)
        text(minutes[-2:] + ":" + seconds[-2:], 10, 10)
