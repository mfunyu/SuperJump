from math import *
from constants import *
from platforms import *

counter = 1
MAXHEIGHT = RESY / 2


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


    def calDistance(self, target):
        return ((self.x_position - target.x_position)**2 + (self.y_position - target.y_position)**2)**0.5


    def groundUpdate(self, platforms):
        '''
        Finding a ground to land on
        Not working for going down
        '''
        # check from the highers platform
        for p in reversed(platforms):
            # if platform is lower than the king
            if (self.y_position + self.radius <= p.y - p.h / 2
                    and p.x - p.w / 2 - self.radius <= self.x_position <= p.x + p.w / 2 + self.radius):
                self.ground = p.y - p.h / 2
                self.platform_now = p

                return
        # if none, the bottom is the ground
        self.y_position = RESY - MAGMA_H - self.radius
        self.ground = RESY - MAGMA_H


    def reborn(self, platforms):
        # platforms = Platforms() <- list of platforms that is displayed in the game now
        for platform in platforms:

            if platform.x in range(RESX * 1/3, RESX * 2/3) and platform.y in range(RESX * 1/3, RESX * 2/3):
                self.x_position = platform.x
                self.y_position = platform.y - platform.h / 2 - self.radius
                self.platform_now = platform
                return
        else:
            print("No Platform")


    def onPlatfrom(self):
        if self.y_position + self.radius < self.ground:
            return False
        # out of x-range in platform
        if (self.x_position + self.radius / 2 < self.platform_now.x - self.platform_now.w / 2
                or self.platform_now.x + self.platform_now.w / 2 < self.x_position - self.radius / 2):
            print("Fall")
            return False
        return True

    def update(self, platforms):

        # condition lose life
        if self.y_position + self.radius > RESY - MAGMA_H:
            self.life -= 1
            self.bg_musics["lose_life"].play()
            self.reborn(platforms)

        # condition die
        if self.life <= 0:
            self.alive = False

        # if calDistance(self, target) <= (self.radius + target.radius):

        # if in the air, up arrow key does not work
        if self.isJumping:
            self.key_handler['jump'] == False


        # right left movements
        if self.key_handler['right'] and not self.key_handler['jump']:
            if not self.isJumping:
                self.rightImgCounter += 1
                self.rightMove_img = loadImage(PATH + '/images/king' + str(self.rightImgCounter) + '.png')
                self.img = self.rightMove_img
                if self.rightImgCounter == 3 or not self.key_handler['right']:
                    self.rightImgCounter = 0
            self.x_position += self.speed
        elif self.key_handler['left'] and not self.key_handler['jump']:
            if not self.isJumping:
                self.leftImgCounter += 1
                self.rightMove_img = loadImage(PATH + '/images/king' + str(self.leftImgCounter) + '.png')
                self.img = self.rightMove_img
                if self.leftImgCounter == 6 or not self.key_handler['left']:
                    self.leftImgCounter = 3
            self.x_position -= self.speed
        elif self.key_handler['jump'] and self.onPlatfrom():
            self.img = self.charging_img
        else:
            self.img = self.normal_img

        # movement while jumping
        if self.isJumping and self.key_handler['right']:
            self.jump_img = loadImage(PATH + '/images/king' + str(self.jumpImgCounter_right) + '.png')
        elif self.isJumping and self.key_handler['left']:
            self.jump_img = loadImage(PATH + '/images/king' + str(self.jumpImgCounter_left) + '.png')

        # calc jump height
        if self.onPlatfrom() and self.key_handler['jump']:
            if self.height < MAXHEIGHT:
                self.height += 10
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
            self.jump()
            if (self.height != 0
                    and -self.height * sin(radPerFrame*(counter-2)) + self.ground > self.y_position
                    and self.y_position < -self.height * sin(radPerFrame*counter) + self.ground):
                self.jumpImgCounter_right = 9
            if self.jumpImgCounter_right < 14:
                self.jumpImgCounter_right += 1
            if self.jumpImgCounter_right == 10:
                self.jumpImgCounter_right = 11
            self.img = self.jump_img
        elif self.isJumping and self.height != 0 and self.key_handler['left']:
            self.jump()
            if (self.height != 0
                    and -self.height * sin(radPerFrame*(counter-2)) + self.ground > self.y_position
                    and self.y_position < -self.height * sin(radPerFrame*counter) + self.ground):
                self.jumpImgCounter_left = 17
            if self.jumpImgCounter_left < 21:
                self.jumpImgCounter_left += 1
            self.img = self.jump_img
        elif self.isJumping and self.height != 0:
            self.jump()
            if (self.height != 0
                    and -self.height * sin(radPerFrame*(counter-2)) + self.ground > self.y_position
                    and self.y_position < -self.height * sin(radPerFrame*counter) + self.ground):
                self.jumpImgCounter_left = 17
            if self.jumpImgCounter_left < 21:
                self.jumpImgCounter_left += 1
            self.img = self.jump_img
        # right after done charging for jump
        elif not self.key_handler['jump'] and self.height > 0:
            self.jumpImgCounter_right = 8
            self.jumpImgCounter_left = 16
            self.img = self.jump_img
            self.jump()

        # updating a ground
        if not self.onPlatfrom():
            self.groundUpdate(platforms)


    def display(self, platforms):

        self.update(platforms)
        fill(0,0,255)
        circle(self.x_position, self.ground, 5)

        # Displaying the image by width and height of its radius
        imageMode(CENTER)
        image(self.img, self.x_position, self.y_position, 2 * self.radius, 2 * self.radius)
        imageMode(CORNER)



    def jump(self):
        global radPerFrame
        radPerFrame = 2*pi/frameRate # radian per frame
        global counter        # framecount while jumping

        # end of the jump
        if self.onPlatfrom() and self.isJumping:
            self.isJumping = False
            counter = 1
            self.y_speed = 0
            self.height = 0
            self.jump_start = 0
        # in the air or start of the jump
        elif self.onPlatfrom() or self.isJumping:
            if not self.jump_start:
                self.jump_start = self.ground
            self.isJumping = True
            self.y_position = - self.height * sin(radPerFrame*counter) + self.jump_start
            self.y_speed = - self.height * cos(radPerFrame*counter)
            print("sp", self.y_speed)
            counter += 1
        # prevent king from sinking
        if self.y_position + self.radius > self.ground:
            self.y_position = self.ground - self.radius
