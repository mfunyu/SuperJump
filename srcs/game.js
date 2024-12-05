

const GAME_SPEED = 3
const HORIZONTAL_MAX = 200
const JUMP_HIGHET = 20

const NUM_IMG_DIV = 1
const NUM_PHASE = 1

let KING_SIZE;
let GAMEX_L;
let GAMEX_R;
let GAMEX_U;
let GAMEX_D;
let MAGMA_H;

class Game {
  static highestScore = 0;


  constructor(bgMusics) {
    KING_SIZE = windowHeight / 8;
    GAMEX_L = windowWidth * 0.05
    GAMEX_R = windowWidth * 0.95
    GAMEX_U = windowHeight * 0.05
    GAMEX_D = windowHeight * 0.95
    MAGMA_H = windowWidth * 0.02

    this.startTime = millis();
    this.score = 0;
    this.speed = GAME_SPEED;
    this.speedStore = GAME_SPEED;
    this.play = false;

    // Background music and sounds
    this.bgMusics = bgMusics;
    this.bgMusic = bgMusics['bg_music'];
    this.gameEnd = bgMusics['game_end'];
    this.bgMusic.loop();

    this.background = new Background();

    // Platforms
    this.realPlatforms = [];
    this.midPlatform = [windowWidth / 2, windowHeight / 2, 150, 50];
    this.realPlatforms.push(new Platform(this.midPlatform[0], this.midPlatform[1], this.midPlatform[2], this.midPlatform[3], 0));
    // while (this.realPlatforms[this.realPlatforms.length - 1]?.y >= -(this.bgImgs[0].height - windowHeight) - 10000) {
    //   this.createOneRealPlatform();
    // }

    // King
    this.king = new King(windowWidth / 2, this.realPlatforms[0].y - this.realPlatforms[0].h / 2 - KING_SIZE / 2, 3, 12, this.realPlatforms[0], bgMusics);

    // Magma
    this.magmaImg = loadImage(IMG_PATH + "magma.png");

    // Clouds
    this.cloudX = 0;
    this.cloudY = 0;
  }

  gameOver() {
    // Stop music and play game end sound
    Object.values(this.bgMusics).forEach(music => music.stop());
    this.gameEnd.play();

    // Display game over screen
    image(loadImage(IMG_PATH + "background.png"), 0, 0, width, height);
    imageMode(CENTER);
    let logo = loadImage(IMG_PATH + "gameover.png");
    image(logo, width / 2, height / 5, width * 5 / 6, (width * 5 / 6) * logo.height / logo.width);
    imageMode(CORNER);
    fill(255);
    textAlign(CENTER);
    textSize(windowWidth * 0.04);
    text("Your Score", width / 2, height * 2 / 5);
    textSize(windowWidth * 0.03);
    text(this.score, width / 2, height * 3 / 5);
    text("Click Anywhere to Restart", width / 2, height * 4 / 5);
    let img = loadImage(IMG_PATH + "king10.png");
    image(img, KING_SIZE, windowHeight - KING_SIZE * 1.5, KING_SIZE * 1.5, KING_SIZE * 1.5);
  }

  createOneRealPlatform() {
    let condition = true;
    let newX, newY, newWidth, newHeight;

    // Generate platform within constraints
    while (condition) {
      newWidth = random(100, 200);
      newHeight = random(30, 60);
      let newXPositive = this.midPlatform[0] + this.midPlatform[2] + random(0.3 * Math.tanh(this.speed) * HORIZONTAL_MAX, 0.6 * Math.tanh(this.speed) * HORIZONTAL_MAX);
      let newXNegative = this.midPlatform[0] - random(0.3 * Math.tanh(this.speed) * HORIZONTAL_MAX, 0.6 * Math.tanh(this.speed) * HORIZONTAL_MAX) - newWidth;
      newX = random([newXPositive, newXNegative]);
      newY = this.midPlatform[1] - random(2 * Math.tanh(this.speed) * JUMP_HIGHET, 3 * Math.tanh(this.speed) * JUMP_HIGHET) - newHeight;

      if (GAMEX_L <= newX - newWidth / 2 && newX + newWidth / 2 <= GAMEX_R) {
        condition = false;
      }
    }

    // Add platform
    this.midPlatform = [newX, newY, newWidth, newHeight];
    this.realPlatforms.push(new Platform(newX, newY, newWidth, newHeight, int(random(1, 7))));
  }

  display() {
    // Check if the game is over
    if (!this.king.alive) {
      this.play = false;
      return;
    }

    this.background.display();

    // Clouds
    if (this.bgNum > 1) {
      let cloud = loadImage(IMG_PATH + "clouds.png");
      this.cloudY += this.speed;
      this.cloudX += this.speed * 2;
      image(cloud, this.cloudX, this.cloudY, cloud.width / 2, cloud.height / 2);
    }

    // Platforms
    for (let platform of this.realPlatforms) {
      platform.y += this.speed;
      platform.display();
    }

    // Magma
    image(this.magmaImg, 0, windowHeight - MAGMA_H, windowWidth, this.magmaImg.height);

    // Side boundaries
    let bottom = 0;
    while (bottom < windowHeight) {
      let img = loadImage(IMG_PATH + "sidebrick0.png");
      image(img, 0, bottom, GAMEX_L, GAMEX_L * img.height / img.width);
      image(img, GAMEX_R, bottom, GAMEX_L, GAMEX_L * img.height / img.width);
      bottom += GAMEX_L * img.height / img.width;
    }

    // Life display
    let yPosition = GAMEX_L * 0.5;
    for (let i = 0; i < this.king.life; i++) {
      let heart = loadImage(IMG_PATH + "heart.png");
      image(heart, GAMEX_R + (GAMEX_L * 0.2), yPosition, GAMEX_L * 0.6, GAMEX_L * 0.6);
      yPosition += GAMEX_L;
    }

    // King
    this.king.yPosition += this.speed;
    this.king.ground += this.speed;
    this.king.display(this.realPlatforms);

    if (this.king.yPosition - this.king.radius < 20) {
      this.speed += 6;
    } else {
      this.speed = this.speedStore;
    }

    // Timer and score
    let timePassed = int((millis() - this.startTime) / 1000);
    this.score = timePassed + this.king.score;
    let minutes = nf(floor(timePassed / 60), 2);
    let seconds = nf(timePassed % 60, 2);
    fill(255);
    textAlign(LEFT, TOP);
    text(`${minutes}:${seconds}`, 10, 10);
    text(`Score: ${this.score}`, 10, 40);
  }
}
