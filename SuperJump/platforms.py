from game import Game
game = Game()

class Platforms():
    def __init__(self, x, y, w, h, img, num_frames):
        self.x = x
        self.y = y
        #note that these are the cordinates when they are born, not when
        self.w = w
        self.h = h
        self.img = loadImage(path + "/images/brick0.png" + img)
        self.num_frames = num_frames
        
        self.vy = 0
        self.frame = 0
        #self.dir = RIGHT??
        
    def drop(self):#set difficulty
        self.vy = game.level
        
        #make the creature land on a platform?
        
    def update(self):
        self.drop()
        self.y += self.vy
    
    def display(self):
        self.update()
        
        #syntax: image(img, x, y, width, height, x1, y1, x2, y2)
        imageMode(CENTER)
        image(self.img, self.x, self.y, self.w, self.h)
        

    
        # set distance in relation to the last board
        last_distance = self.platforms.pop().y_position
        distance = JUMP_HIGHET - last_distance

        # append platform instance anonimously
        last_y = 0
        while last_y > JUMP_HIGHET:
            # choose x position of the platform
            # might be too far to jump on
            center_x = random.randint(GAMEX_L, GAMEX_R)

            # choose y position of the platform
            # upper_bound: king should be visible in all sceans
            upper_bound = max([last_y - distance, KING_SIZE])
            # lower_bound: platform should be higher than the last one
            lower_bound = last_y
            center_y = random.randint(upper_bound, lower_bound)

            # instanciate Platform(x, y)
            self.platforms.append(Platform(center_x, center_y))

            # update variables
            last_y = center_y
            distance = JUMP_HEIGHT
