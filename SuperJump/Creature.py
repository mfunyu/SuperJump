from math import *
from constants import *
from platforms import *

counter = 1
MAXHEIGHT = RESY / 2

class King():
    def __init__(self, x_position, y_position, life, radius, ground, speed, normal_img, rightMove_img, leftMove_img, jump_img):

        self.alive = True

        self.life = life
        self.x_position = RESX / 2
        self.y_position = RESY - KING_SIZE/2
        self.radius = KING_SIZE / 2
        self.ground = RESY
        self.speed = speed
        self.img = loadImage(normal_img)
        self.height = 0
        # self.distance = distance

        self.rightImgCounter = 0
        self.leftImgCounter = 3
        self.jumpImgCounter = 0
        self.rightMove_img = loadImage(rightMove_img)
        self.leftMove_img = loadImage(leftMove_img)
        self.jump_img = loadImage(jump_img)
        self.normal_img = loadImage(normal_img)

        self.key_handler = {'jump':False, 'right':False, 'left':False}

        self.canJump = True
        self.isJumping = False
        self.frames = 0


    def calDistance(self, target):
        return ((self.x_position - target.x_position)**2 + (self.y_position - target.y_position)**2)**0.5


    def newGround(self, platforms):
        '''
        Finding a ground to land on
        Not working for going down
        '''
        # check from the highers platform
        for p in reversed(platforms):
            # if platform is lower than the king
            if (self.y_position + self.radius < p.y - p.h / 2
                    and p.x - p.w / 2 - self.radius <= self.x_position <= p.x + p.w / 2 + self.radius):
                self.ground = p.y - p.h / 2
                return
        # if none, the bottom is the ground
        self.ground = RESY

    
    def reBorn(self):
        '''
        Randomly finding the background to reborn
        '''
    
    def loseLife(self):
        '''
        Life loosing condition
        '''
        return False
    
    def update(self, platforms):

        if self.loseLife():
            self.life -= 1

        if self.life != 0:
            self.alive = True
        else:
            self.alive = False
            # gameOver()

        # if calDistance(self, target) <= (self.radius + target.radius):

        # when its in the air (cant jump)
        if self.y_position + self.radius < self.ground:
            self.canJump = False
            self.frames = 0
        else:
            self.canJump = True

        # right left movements
        if self.key_handler['right']:
            self.rightImgCounter += 1
            self.rightMove_img = loadImage(PATH + '/images/king' + str(self.rightImgCounter) + '.png')
            self.img = self.rightMove_img
            self.x_position += self.speed
            if self.rightImgCounter == 3 or not self.key_handler['right']:
                self.rightImgCounter = 0
        elif self.key_handler['left']:
            self.leftImgCounter += 1
            self.rightMove_img = loadImage(PATH + '/images/king' + str(self.leftImgCounter) + '.png')
            self.img = self.rightMove_img
            self.x_position -= self.speed
            if self.leftImgCounter == 6 or not self.key_handler['left']:
                self.leftImgCounter = 3
        else:
            self.img = self.normal_img


        # calc jump height
        if self.key_handler['jump']:
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

        if self.isJumping:
            self.jump()
        elif not self.key_handler['jump'] and self.height > 0:
            self.img = self.jump_img
            self.jump()

        # updating a ground
        self.newGround(platforms)



    def display(self, platforms):

        self.update(platforms)

        # Displaying the image by width and height of its radius
        imageMode(CENTER)
        image(self.img, self.x_position, self.y_position, 2 * self.radius, 2 * self.radius)
        imageMode(CORNER)


    def jump(self):

        radPerFrame = 2*pi/frameRate # radian per frame
        global counter        # framecount while jumping

        if self.canJump and self.isJumping:
            self.isJumping = False
            counter = 1
            self.height = 0
        elif self.canJump or self.isJumping:
            self.y_position = - self.height * sin(radPerFrame*counter) + self.ground
            counter += 1
            self.isJumping = True
        # prevent king from sinking
        if self.y_position + self.radius > self.ground:
            self.y_position = self.ground - self.radius
