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

const Status = {
  NOT_STARTED: 0,
  LOADING: 1,
  WAITING: 2,
  STARTED: 3
}
let phase = Status.NOT_STARTED;

function preload() {
  imgBackground = loadImage(IMG_PATH + "background.png");
  speakerUnmuteImg = loadImage(IMG_PATH + "speaker_unmute.png")
  speakerMuteImg = loadImage(IMG_PATH + "speaker_mute.png")
  speakerStatusImg = speakerMuteImg

  logoImg = loadImage(IMG_PATH + "logo.png");
  kingLoadimg = loadImage(IMG_PATH + "king0.png");

  // sounds
  bgMusics["bg_music"] = loadSound(SOUND_PATH + "bg_music.mp3");
  bgMusics["game_end"] = loadSound(SOUND_PATH + "game_end.mp3");
  bgMusics["jump"] = loadSound(SOUND_PATH + "jump.mp3");
  bgMusics["lose_life"] = loadSound(SOUND_PATH + "lose_life.mp3");
  bgMusics["jump_premotion"] = loadSound(SOUND_PATH + "jump_premotion.mp3");
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  // background(0);
}

function draw() {
  background(0);
  switch (phase) {
    case Status.NOT_STARTED:
      startupScreen("Loading ... ");
      phase = Status.LOADING;
      break;
    case Status.LOADING:
      game = new Game(bgMusics);
      phase = Status.WAITING;
      break;
    case Status.WAITING:
      startupScreen("Click Anywhere to Start");
      break;
    case Status.STARTED:
      if (!game)
        break;
      if (game.play) {
        game.display();
      } else {
        game.gameOver();
      }
    }

    image(speakerStatusImg, 20, windowHeight - 100, 80, 80);
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
    } else if (phase === Status.WAITING) {
      phase = Status.STARTED;
      console.log("Game start");
      game.play = true;
    } else if (phase === Status.STARTED) {
      if (!game?.king?.alive) {
        phase = Status.NOT_STARTED;
        game = null;
      }
    }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}