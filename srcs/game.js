

const GAME_SPEED = 3

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
    this.platform = new Platform(windowWidth / 2, windowHeight / 2, 150, 50, Platform.platformType.REACHED);
    this.platforms = [this.platform];

    let previousPlatform = this.platform;
    while (previousPlatform.y >= -windowHeight - 10000) {
      previousPlatform = Platform.createNewPlatform(previousPlatform, this.speed);
      this.platforms.push(previousPlatform);
    }

    // King
    this.king = new King(3, 12, this.platform, bgMusics);

    // Clouds
    this.cloudX = 0;
    this.cloudY = 0;

    this.magma = new StaticObjects(StaticObjects.objectType.MAGMA, 0.02);
    this.sideBricks = new StaticObjects(StaticObjects.objectType.BRICKS, 0.05);
    this.lifes = new StaticObjects(StaticObjects.objectType.LIFE, 0.05, 0.4);
  }

  display() {
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
    for (let platform of this.platforms) {
      platform.y += this.speed;
      platform.display();
    }

    // King
    this.king.y_position += this.speed;
    this.king.ground += this.speed;
    this.king.display(this.platforms);

    if (this.king.yPosition - this.king.radius < 20) {
      this.speed += 6;
    } else {
      this.speed = this.speedStore;
    }

    this.magma.display();
    this.sideBricks.display();
    this.lifes.display(this.king.life);

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
