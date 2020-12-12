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

    def __init__(self, bg_musics):
        self.time = time.time()
        self.score = 0
        self.speed = GAME_SPEED
        self.speedstore = GAME_SPEED
        self.play = False
        # decide a music
        self.bg_musics = bg_musics
        self.bg_music = bg_musics['bg_music']
        self.game_end = bg_musics['game_end']
        self.bg_music.loop()
        # bg_image managements
        self.bg_num = 0
        self.bg_imgs = []
        for i in range(NUM_BG_IMGS):
            self.bg_imgs.append(loadImage(PATH + "/images/bg" + str(i) + ".png"))

        self.y_position = [- (self.bg_imgs[0].height - RESY), 0]

        # multiple platform creations
        self.realplatforms = []
        self.midplatform = [RESX/2, RESY/2, 150, 50]
        self.realplatforms.append(Platform(self.midplatform[0], self.midplatform[1], self.midplatform[2], self.midplatform[3], 0))
        for single_platform in self.realplatforms:
            if single_platform.y >= -(self.bg_imgs[self.bg_num].height - RESY) - 10000:
                self.create_one_real_platform()

        self.king = King(RESX / 2, self.realplatforms[0].y - self.realplatforms[0].h / 2 - KING_SIZE/2, 3, 12, self.realplatforms[0], bg_musics)

        # magma
        self.magma_img = loadImage(PATH + '/images/magma.png')

        # clouds
        self.cloud_x = 0
        self.cloud_y = 0


    def gameover(self):
        '''
        Display the game over screen
        '''
        for bg_music in self.bg_musics:
            self.bg_musics[bg_music].pause()
        self.game_end.play()
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
        text("Click Anywhere to Restart", width / 2, height * 4 / 5)
        img = loadImage(PATH + "/images/king10.png")
        image(img, KING_SIZE, RESY - KING_SIZE * 1.5, KING_SIZE * 1.5,
              KING_SIZE * 1.5, 0, 0, img.width, img.height)



    def create_one_real_platform(self):
        condition = True

        # check if random platform is in the required range
        while condition:
            new_width = random.randint(100, 200)
            new_height = random.randint(30, 60)
            new_x_positive = self.midplatform[0] + self.midplatform[2]+ random.uniform(0.3*tanh(self.speed)*HORIZONTAL_MAX, 0.6*tanh(self.speed)*HORIZONTAL_MAX)
            new_x_negative = self.midplatform[0] - random.uniform(0.3*tanh(self.speed)*HORIZONTAL_MAX, 0.6*tanh(self.speed)*HORIZONTAL_MAX) - new_width
            new_x = random.choice([new_x_positive, new_x_negative])
            new_y = self.midplatform[1] - random.uniform(2*tanh(self.speed)*JUMP_HIGHET, 3*tanh(self.speed)*JUMP_HIGHET) - new_height

            if GAMEX_L <= new_x - new_width/2 and new_x + new_width/2 <= GAMEX_R:
                condition = False

        # adding platfrom that meets requirement to the real platforms
        self.midplatform[0] = new_x
        self.midplatform[1] = new_y
        self.midplatform[2] = new_width
        self.midplatform[3] = new_height
        self.realplatforms.append(Platform(self.midplatform[0], self.midplatform[1], self.midplatform[2], self.midplatform[3], random.randint(1, 7)))


    def display(self):

        # 0. if the game is over
        if not self.king.alive:
            self.play = False
            return

        # 1. display the background
        self.y_position[0] += self.speed * 0.5

        # when the previous image dissapears (only 1 image is displayed)
        # the previous image sinks below the screen bottom
        if self.y_position[0] > RESY:
            self.y_position[0] = self.y_position[1]
            self.y_position[1] = 0
            self.bg_num = min([self.bg_num + 1, NUM_BG_IMGS - 1])
            # increasing the game speed when new bg
            self.speed += 1
            self.speedstore += 1
            self.king.score += 100
        image(self.bg_imgs[self.bg_num], 0, self.y_position[0], RESX, self.bg_imgs[self.bg_num].height)

        # when start displaying next image (2 images are displayed)
        if -5 <= self.y_position[0] < RESY:
            second_bg_num = min([self.bg_num + 1, NUM_BG_IMGS - 1])
            # create second image if not exist
            if not self.y_position[1]:
                self.y_position[1] = -1 * (self.bg_imgs[second_bg_num].height)
            image(self.bg_imgs[second_bg_num], 0, self.y_position[1], RESX, self.bg_imgs[second_bg_num].height)
            self.y_position[1] += self.speed * 0.5


        # side moving clouds
        if self.bg_num > 1:
            cloud = loadImage(PATH + "/images/clouds.png")
            self.cloud_y += self.speed
            self.cloud_x += self.speed * 2
            image(cloud, self.cloud_x, self.cloud_y, cloud.width / 2, cloud.height / 2)

        # 3. display platforms
        # create random platforms
        for single_platform in self.realplatforms:
            single_platform.y += self.speed
            single_platform.display()

        # 4. display the magma
        image(self.magma_img, 0, RESY - MAGMA_H, RESX, self.magma_img.height)

        # 5. displaying side boundries
        bottom = 0
        while bottom < RESY:
            img = loadImage(PATH + "/images/sidebrick0.png")
            # display at the edge of the screen
            image(img, 0, bottom, GAMEX_L, GAMEX_L * img.height / img.width)
            image(img, GAMEX_R, bottom, GAMEX_L,
                  GAMEX_L * img.height / img.width)
            bottom += GAMEX_L * img.height / img.width

        # 6. display life left
        yposition = GAMEX_L * 0.5
        for life in range(self.king.life):
            heart = loadImage(PATH + "/images/heart.png")
            image(heart, GAMEX_R + (GAMEX_L * 0.2), yposition, GAMEX_L * 0.6,
                  GAMEX_L * 0.6)
            yposition += GAMEX_L

        # 7. display the king
        self.king.y_position += self.speed
        self.king.ground += self.speed
        self.king.display(self.realplatforms)
        # when king frames out increase the speed
        if self.king.y_position - self.king.radius < 20:
            self.speed += 6
        # set the speed back to normal
        else:
            self.speed = self.speedstore

        # 8. display the game timer
        time_passed = int(floor(time.time() - self.time))
        self.score = time_passed + self.king.score
        minutes = '0' + str(time_passed // 60)
        seconds = '0' + str(time_passed % 60)
        fill(255)
        textAlign(LEFT, TOP)
        text(minutes[-2:] + ":" + seconds[-2:], 10, 10)
        text("score " + str(self.score), 10, 40)
