// images
let IMG_PATH = "../assets/images/"
let imgBackground;
let speakerMuteImg;
let speakerUnmuteImg;
let speakerStatusImg;
let logoImg;
let kingLoadimg;

let SOUND_PATH = "../assets/sounds/"
let bgMusics = {};


function preload() {
  imgBackground = loadImage(IMG_PATH + "background.png");
  speakerUnmuteImg = loadImage(IMG_PATH + "speaker_unmute.png")
  speakerMuteImg = loadImage(IMG_PATH + "speaker_mute.png")
  speakerStatusImg = speakerMuteImg

  logoImg = loadImage(IMG_PATH + "logo.png");
  kingLoadimg = loadImage(IMG_PATH + "king_loading.png");

  // sounds
  bgMusics["bg_music"] = loadSound(SOUND_PATH + "bg_music.mp3");
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  // background(0);
}

function draw() {
  background(0); // Clear the canvas
  // if (loadStatus === NOT_STARTED) {
        startupScreen("Loading ... ");
    //     loadStatus = LOADING;
    // } else if (loadStatus === LOADING && !game) {
    //     game = new Game(bgMusics);
    // } else if (game && game.play) {
    //     game.display();
    // } else if (game && game.king.alive) {
    //     startupScreen("Click Anywhere to Start");
    //     loadStatus = LOADED;
    // } else if (game) {
    //     game.gameover();
    // }
    image(speakerStatusImg, 20, windowHeight - 100, 80, 80); // Display speaker icon
}

function startupScreen(displayText) {
  image(imgBackground, 0, 0, width, height);
  imageMode(CENTER);

  fill(255);
  image(logoImg, width / 2, height * 1 / 5,
    width * 5 / 6, (width * 5 / 6) * logoImg.height / logoImg.width)
  imageMode(CENTER);

  textAlign(CENTER);
  textSize(windowHeight * 0.03);
  textFont("3270SemiNarrow");
  text("How to Play", width / 2, height * 2 / 5);
  text("<- : left\n-> : right\nSPACE BAR : jump", width * 1 / 4, height / 2);
  text("Blue platforms: life + 1\nMonsters: life - 1\n(press: charging, release: start jump)", width * 2 / 3, height / 2);
  text(displayText, width / 2, height * 4 / 5);

  let KING_SIZE = windowHeight / 5;
  image(kingLoadimg, KING_SIZE, windowHeight - KING_SIZE, KING_SIZE, KING_SIZE);
  imageMode(CORNER);
}
/*
function keyPressed() {
    // Handle key presses
    if (game && game.king) {
        if (keyCode === LEFT_ARROW) game.king.keyHandler['left'] = true;
        if (keyCode === RIGHT_ARROW) game.king.keyHandler['right'] = true;
        if (key === ' ') game.king.keyHandler['jump'] = true;
    }
}

function keyReleased() {
    // Handle key releases
    if (game && game.king) {
        if (keyCode === LEFT_ARROW) game.king.keyHandler['left'] = false;
        if (keyCode === RIGHT_ARROW) game.king.keyHandler['right'] = false;
        if (key === ' ') game.king.keyHandler['jump'] = false;
    }
}
*/

function mousePressed() {
    // Mute/unmute or start/restart game
    if (mouseX >= 0 && mouseX <= 100 && mouseY >= windowHeight - 100 && mouseY <= windowHeight) {
        // Toggle mute
        for (let music in bgMusics) {
            if (!bgMusics[music].isPlaying()) {
                bgMusics[music].play();
                speakerStatusImg = speakerUnmuteImg;
            } else {
                bgMusics[music].pause();
                speakerStatusImg = speakerMuteImg;
            }
        }
    }
    // } else if (loadStatus === LOADED && !game.king.alive) {
    //     // Restart game
    //     loadStatus = NOT_STARTED;
    //     game = null;
    // } else if (loadStatus === LOADED && !game.play) {
    //     // Start game
    //     game.play = true;
    //     game.time = millis();
    // }
}