from math import *
from constants import *

counter = 1
MAXHEIGHT = RESY / 2

class King():
    def __init__(self, x_position, y_position, life, radius, ground, speed, imgName, rightMove_img, leftMove_img, jump_img):
    
        self.alive = True
    
        self.life = life
        self.x_position = x_position
        self.y_position = y_position
        self.radius = radius
        self.ground = ground
        self.speed = speed
        self.img = loadImage(imgName)
        self.height = 0
        # self.distance = distance
        
        self.rightMove_img = loadImage(rightMove_img)
        self.leftMove_img = loadImage(leftMove_img)
        self.jump_img = loadImage(jump_img)
        
        self.key_handler = {'jump':False, 'right':False, 'left':False}
        
        self.canJump = True
        self.isJumping = False
        self.frames = 0
        
        
        
    def calDistance(self, target):
        return ((self.x_position - target.x_position)**2 + (self.y_position - target.y_position)**2)**0.5
        
        
    def update(self, loseLife, newGround):
        
        if loseLife:
            self.life -= 1
        
        if self.life != 0:
            self.alive = True
        else:
            self.alive = False
            # gameOver()
            
        # if calDistance(self, target) <= (self.radius + target.radius):
    
        # when its in the air (cant jump)
        if self.y_position < self.ground:
            self.canJump = False
            self.frames = 0
        else:
            self.canJump = True
        
        # right left movements
        if self.key_handler['right']:
            self.img = self.rightMove_img
            self.x_position += self.speed
            # self.ground = newGround
        elif self.key_handler['left']:
            self.img = self.leftMove_img
            self.x_position -= self.speed
            # self.ground = newGround
        
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
        
        
    
    def display(self):
        
        self.update(False, 700-self.radius)
        
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
        if self.y_position > self.ground:
            self.y_position = self.ground
