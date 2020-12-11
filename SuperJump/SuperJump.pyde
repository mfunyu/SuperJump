#import global variables
add_library('minim')
from constants import *
# import class Game
from game import Game
import time

player = Minim(this)

unmute = loadImage(PATH + "/images/unmute.png")
mute = loadImage(PATH + "/images/mute.png")
speaker = unmute

# instanciate game obj
bg_musics = {}
bg_musics['bg_music'] = player.loadFile(PATH + "/sounds/bg_music.mp3")
bg_musics['game_end'] = player.loadFile(PATH + "/sounds/game_end.mp3")
bg_musics['jump'] = player.loadFile(PATH + "/sounds/jump.mp3")
bg_musics['lose_life'] = player.loadFile(PATH + "/sounds/lose_life.mp3")
bg_musics['preparing_jump'] = player.loadFile(PATH + "/sounds/preparing_jump.mp3")

load_status = NOT_STARTED

game = ""

def startup(displaytext):
    '''
    Display the startup screen
    '''

    image(loadImage(PATH + "/images/background.png"), 0, 0, width, height)
    imageMode(CENTER)
    logo = loadImage(PATH + "/images/logo.png")
    image(logo, width / 2, height * 1 / 3,
          width * 5 / 6, (width * 5 / 6) * logo.height / logo.width)
    imageMode(CORNER)
    fill(255)
    textAlign(CENTER)
    font = createFont("3270SemiNarrow", floor(RESX * 0.03))
    textFont(font)
    text(displaytext, width / 2, height * 3 / 4)
    img = loadImage(PATH + "/images/king0.png")
    image(img, KING_SIZE, RESY - KING_SIZE * 1.5, KING_SIZE * 1.5,
        KING_SIZE * 1.5, 0, 0, img.width, img.height)

def setup():
    size(RESX, RESY)
    background(0)

def draw():
    global load_status, game, bg_musics
    # need to instantiate game
    if load_status == NOT_STARTED:
        # show the image for loading
        startup("Loading ... ")
        load_status = LOADING
    # ready to instanciate game
    elif load_status == LOADING and not game:
        game = Game(bg_musics)
    elif game.play:
        game.display()
    elif game.king.alive:
        startup("Click Anywhere to Start")
        load_status = LOADED
    else:
        game.gameover()
    image(speaker, 10, RESY - 100, 80, 80)


def keyPressed():
    global game

    if keyCode == LEFT:
        game.king.key_handler['left'] = True
    elif keyCode == RIGHT:
        game.king.key_handler['right'] = True
    if key == ' ':
        game.king.key_handler['jump'] = True


def keyReleased():
    global game

    if keyCode == LEFT:
        game.king.key_handler['left'] = False
    elif keyCode == RIGHT:
        game.king.key_handler['right'] = False
    if key == ' ':
        game.king.key_handler['jump'] = False


def mousePressed():
    global game, bg_musics, speaker, load_status
    
    # mute or unmute the music
    if ( 0 <= mouseX <= 100
        and RESY - 100 <= mouseY <= RESY):
        for music in bg_musics:
            if bg_musics[music].isMuted():
                bg_musics[music].unmute()
                speaker = unmute
            else:
                bg_musics[music].mute()
                speaker = mute
    # start the game
    elif load_status == LOADED and not game.king.alive:
        load_status = NOT_STARTED
        game = ""
    elif load_status == LOADED and not game.play:
        print(load_status)
        game.play = True
        game.time = time.time()

        
