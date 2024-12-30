// images
let IMG_PATH = "../assets/images/"
let imgBackground;
let speakerMuteImg;
let speakerUnmuteImg;
let speakerStatusImg;
let logoImg;
let kingLoadImg;

let SOUND_PATH = "../assets/sounds/"
let bgMusics = {};

let gameStarted = false;

function preload() {
  imgBackground = loadImage(IMG_PATH + "background.png");
  speakerUnmuteImg = loadImage(IMG_PATH + "speaker_unmute.png")
  speakerMuteImg = loadImage(IMG_PATH + "speaker_mute.png")
  speakerStatusImg = speakerMuteImg

  logoImg = loadImage(IMG_PATH + "logo.png");
  gameOverImg = loadImage(IMG_PATH + "gameover.png");
  kingLoadImg = loadImage(IMG_PATH + "king_normal.png");
  kingDeadImg = loadImage(IMG_PATH + "king_dead.png");

  // sounds
  bgMusics["bg_music"] = loadSound(SOUND_PATH + "bg_music.mp3");
  bgMusics["game_end"] = loadSound(SOUND_PATH + "game_end.mp3");
  bgMusics["jump"] = loadSound(SOUND_PATH + "jump.mp3");
  bgMusics["lose_life"] = loadSound(SOUND_PATH + "lose_life.mp3");
  bgMusics["jump_premotion"] = loadSound(SOUND_PATH + "jump_premotion.mp3");

  King.preload();
  Background.preload();
  Platform.preload();
  StaticObjects.preload();
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  // background(0);
}

function draw() {
  background(0);

  if (!gameStarted) {
    showStartScreen();
    game = new Game(bgMusics);
    console.log("game", game);
  } else {
    if (game?.play) {
      game.display();
    } else {
      showGameOverScreen(game.score);
    }
  }

  image(speakerStatusImg, 20, windowHeight - 100, 80, 80);
}

function displayScreen(background, logo, title, king, displayText) {
  imageMode(CORNER);
  image(background, 0, 0, width, height);

  imageMode(CENTER);
  image(logo, width / 2, height * 1 / 5, width * 5 / 6, (width * 5 / 6) * logo.height / logo.width)

  fill(255);
  textAlign(CENTER);
  textFont("3270SemiNarrow");

  //title
  text(title, width / 2, height * 2 / 5);
  text(displayText, width / 2, height * 4 / 5);

  let KING_SIZE = windowHeight / 6;
  imageMode(CENTER);
  image(king,  KING_SIZE, windowHeight - KING_SIZE, KING_SIZE, KING_SIZE);
}

function showStartScreen() {
  textSize(windowWidth * 0.02);
  let title = "How to Play"
  let displayText = "Click Anywhere to Start";
  displayScreen(imgBackground, logoImg, title, kingLoadImg, displayText);

  text("<- : left\n-> : right\nSPACE BAR : jump", width * 1 / 4, height / 2);
  text("Blue platforms: life + 1\nMonsters: life - 1\n(press: charging, release: start jump)", width * 2 / 3, height / 2);

  noLoop();
}

function showGameOverScreen(score) {
  // Stop music and play game end sound
  // Object.values(this.bgMusics).forEach(music => music.stop());
  // this.gameEnd.play();
  let displayText = "Click Anywhere to Restart";
  displayScreen(imgBackground, gameOverImg, "Game Over", kingDeadImg, displayText)

  text(score, width / 2, height * 3 / 5);
  noLoop();
}

function keyPressed() {
  game?.king?.handlingKeyEvent(keyCode);
}

function keyReleased() {
  game?.king?.handlingKeyEvent(keyCode);
}

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
  } else {
    if (!gameStarted) {
      console.log("Game start");
      gameStarted = true;
      game.play = true;
      loop();
    } else if (!game?.play) {
      gameStarted = false;
      loop();
    }
  }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}