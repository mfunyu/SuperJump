from math import *
from constants import *
from platforms import *

counter = 1
MAXHEIGHT = RESY / 2
fallstartFrame = 0


class King():
    def __init__(self, x_position, y_position, life, speed, realplatform, bg_musics):

        self.alive = True

        self.x_position = x_position
        self.y_position = y_position
        self.life = life
        self.bg_musics = bg_musics
        self.radius = KING_SIZE / 2
        self.ground = self.y_position + self.radius
        self.platform_now = realplatform
        self.speed = speed
        self.y_speed = 0
        self.jump_start = 0
        self.height = 0
        self.score = 0
        # self.distance = distance

        self.rightImgCounter = 0
        self.leftImgCounter = 3
        self.jumpImgCounter_right = 8
        self.jumpImgCounter_left = 16
        self.rightMove_img = loadImage(PATH + "/images/king1.png")
        self.leftMove_img = loadImage(PATH + "/images/king0.png")
        self.jump_img = loadImage(PATH + "/images/king8.png")
        self.charging_img = loadImage(PATH + "/images/king7.png")
        self.normal_img = loadImage(PATH + "/images/king0.png")
        self.img = self.normal_img

        self.key_handler = {'jump':False, 'right':False, 'left':False}

        self.isJumping = False
        self.isFalling = False
        self.fallImgCounter_right = 9
        self.fallImgCounter_left = 17



    def calDistance(self, target):
        return ((self.x_position - target.x)**2 + (self.y_position - (target.y - (target.h / 2) - (KING_SIZE / 2)))**2)**0.5


    def groundUpdate(self, platforms):
        '''
        Finding a grounself.d to land on
        Not working for going d   '''
        # check frotarget.y_positionhers platform
        for p in reversed(platforms):
            # if platform is lower than the king
            if (self.y_position + self.radius <= p.y - p.h / 2
                    and p.x - p.w / 2 - self.radius <= self.x_position <= p.x + p.w / 2 + self.radius):
                self.ground = p.y - p.h / 2
                self.platform_now = p

                return
        # if none, the bottom is the ground
        self.ground = RESY - MAGMA_H


    def reborn(self, platforms):
        '''
        Reborn to the lowerst platform after touching the magma
        '''
        for platform in platforms:
            # find the closest platform
            if 5 < platform.y <= RESY and platform.mark != 1 and platform.mark != 2:
                self.x_position = platform.x
                self.y_position = platform.y - platform.h / 2 - self.radius
                self.platform_now = platform
                return


    def check_onPlatform(self):
        # if king is in the air
        if self.y_position + self.radius < self.ground:
            return False

        # out of x-range in platform
        if (self.x_position + self.radius / 2 < self.platform_now.x - self.platform_now.w / 2
                or self.platform_now.x + self.platform_now.w / 2 < self.x_position - self.radius / 2):
            # start falling
            if not self.isJumping:
                self.isFalling = True
                global fallstartFrame
                fallstartFrame = frameCount
            return False

        self.isFalling = False
        return True


    def update(self, platforms):

        self.onPlatform = self.check_onPlatform()

        # add life and score when landing on a good platform
        if self.platform_now.mark == 1 and self.onPlatform:
            self.platform_now.mark = 0
            self.life += 1
            self.score += 20
            self.platform_now.text_display = "+20   "
        # reduce life and score when landing on a bad platform
        elif self.platform_now.mark == 2: #platform is bad
            if self.calDistance(self.platform_now) <= self.radius * 2:
                self.bg_musics["lose_life"].play()
                self.bg_musics["lose_life"].rewind()
                self.platform_now.mark = 0
                self.life -= 1
                self.score -= 20
                self.platform_now.text_display = "-20   "
        # add score when landing on a normal platform
        elif self.platform_now.mark != 0 and self.onPlatform:
            self.platform_now.mark = 0
            self.score += 10
            self.platform_now.text_display = "+10   "

        # condition lose life
        if self.y_position + self.radius > RESY - MAGMA_H:
            self.isFalling = False
            self.life -= 1
            self.bg_musics["lose_life"].play()
            self.bg_musics["lose_life"].rewind()
            self.score -= 50
            self.reborn(platforms)


        # condition die
        if self.life <= 0:
            self.alive = False


        # if in the air, up arrow key does not work
        if self.isJumping:
            self.key_handler['jump'] == False


        # right left movements
        if self.key_handler['right'] and not self.key_handler['jump']:
            if not self.isJumping:
                self.rightImgCounter += 1
                self.rightMove_img = loadImage(PATH + '/images/king' + str(self.rightImgCounter) + '.png')
                if not self.isFalling and not self.isJumping:
                    self.img = self.rightMove_img
                if self.rightImgCounter == 3 or not self.key_handler['right']:
                    self.rightImgCounter = 0
            self.x_position += self.speed
        elif self.key_handler['left'] and not self.key_handler['jump']:
            if not self.isJumping:
                self.leftImgCounter += 1
                self.leftMove_img = loadImage(PATH + '/images/king' + str(self.leftImgCounter) + '.png')
                if not self.isFalling and not self.isJumping:
                    self.img = self.leftMove_img
                if self.leftImgCounter == 6 or not self.key_handler['left']:
                    self.leftImgCounter = 3
            self.x_position -= self.speed
        elif self.key_handler['jump'] and self.onPlatform:
            self.img = self.charging_img
        else:
            self.img = self.normal_img

        # movement while jumping
        if self.isJumping and self.key_handler['right']:
            self.jump_img = loadImage(PATH + '/images/king' + str(self.jumpImgCounter_right) + '.png')
        elif self.isJumping and self.key_handler['left']:
            self.jump_img = loadImage(PATH + '/images/king' + str(self.jumpImgCounter_left) + '.png')

        # calc jump height
        if self.onPlatform and self.key_handler['jump']:
            # charging sound start
            if not self.height:
                self.bg_musics["preparing_jump"].rewind()
                self.bg_musics["preparing_jump"].play()
            if self.height < MAXHEIGHT:
                self.height += 30
            # displaying the charge bar
            stroke(150)
            fill(150)
            kingwidth = self.radius * 1.8
            rectWidth = kingwidth * self.height / MAXHEIGHT
            rect(self.x_position - self.radius, self.y_position - self.radius*1.3, kingwidth, self.radius*0.08)
            fill(255)
            stroke(255)
            rect(self.x_position - self.radius, self.y_position - self.radius*1.3, rectWidth, self.radius*0.08)
            noFill()



        # jumping in the air
        if self.isJumping and self.height != 0 and self.key_handler['right']:
            self.jumpImgCounter_right = 9
        elif self.isJumping and self.height != 0 and self.key_handler['left']:
            self.jumpImgCounter_left = 17
        elif self.isJumping and self.height != 0:
            if (self.height != 0
                    and -self.height * sin(radPerFrame*(counter-2)) + self.ground > self.y_position
                    and self.y_position < -self.height * sin(radPerFrame*counter) + self.ground):
                self.jumpImgCounter_left = 17
            if self.jumpImgCounter_left < 21:
                self.jumpImgCounter_left += 1
            self.img = self.jump_img
        # right after done charging for jump
        if not self.key_handler['jump'] and self.height > 0:
            self.jumpImgCounter_right = 8
            self.jumpImgCounter_left = 16
            self.img = self.jump_img
            self.jump()

        elif self.isJumping:
            self.jump()


        # preventing king from going out of side boundaries
        if self.x_position - self.radius < GAMEX_L:
            self.x_position = GAMEX_L + self.radius
        if self.x_position + self.radius > GAMEX_R:
            self.x_position = GAMEX_R - self.radius

        # updating a ground
        if not self.onPlatform:
            self.groundUpdate(platforms)

        if self.isFalling:
            self.fall()


    def display(self, platforms):

        self.update(platforms)


        # Displaying the image by width and height of its radius
        imageMode(CENTER)
        image(self.img, self.x_position, self.y_position, 2 * self.radius, 2 * self.radius)
        imageMode(CORNER)


    def fall(self):

        # gravity constant speed -> incement
        self.y_speed += 2
        self.y_position += self.y_speed
        # stop falling
        if self.y_position + self.radius > self.ground:
            self.y_position = self.ground - self.radius
            self.isFalling = False
            self.y_speed = 0
        if self.key_handler['right']:
            if self.fallImgCounter_right < 11:
                self.fallImgCounter_right += 1
                self.fallImgCounter_left += 1
            if self.fallImgCounter_right == 10:
                self.fallImgCounter_right = 11
            if fallstartFrame > frameCount - 6:
                self.fallImgCounter_right = 9
            if self.fallImgCounter_right > 11:
                self.fallImgCounter_right = 11
            self.img = loadImage(PATH + "/images/king" + str(self.fallImgCounter_right) + ".png")
        elif self.key_handler['left']:
            if self.fallImgCounter_left < 18:
                self.fallImgCounter_left += 1
                self.fallImgCounter_right += 1
            if fallstartFrame > frameCount - 6:
                self.fallImgCounter_left = 17
            if self.fallImgCounter_left > 18:
                self.fallImgCounter_left = 18
            self.img = loadImage(PATH + "/images/king" + str(self.fallImgCounter_left) + ".png")

        if self.onPlatform:
            self.isFalling = False
            self.fallImgCounter_right = 8
            self.fallImgCounter_left = 16
            if self.key_handler['right']:
                self.img = loadImage(PATH + "/images/king0.png")
            elif self.key_handler['left']:
                self.img = loadImage(PATH + "/images/king22.png")


    def jump(self):
        global radPerFrame
        radPerFrame = 2*pi/frameRate # radian per frame
        global counter        # framecount while jumping

        self.y_speed = - self.height * cos(radPerFrame*counter)
        # end of the jump
        if self.y_speed > 0 and self.isJumping:
            self.isFalling = True
            global fallstartFrame
            fallstartFrame = frameCount
            self.isJumping = False
            counter = 1
            self.y_speed = 0
            self.height = 0
            self.jump_start = 0
        # in the air or start of the jump
        elif self.onPlatform or self.isJumping:
            if not self.jump_start:
                self.bg_musics["preparing_jump"].pause()
                self.jump_start = self.ground
                self.bg_musics["jump"].play()
                self.bg_musics["jump"].rewind()
            self.isJumping = True
            self.y_position = - self.height * sin(radPerFrame*counter) + self.jump_start
            counter += 1
        # prevent king from sinking
        if self.y_position + self.radius > self.ground:
            self.y_position = self.ground - self.radius
