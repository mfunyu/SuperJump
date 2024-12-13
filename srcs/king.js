const MaxJumpHeight = 500;

class King {
  static normalRightImg;
  static normalLeftImg;
  static moveRightImgs = [];
  static moveLeftImgs = [];
  static chargeImg;
  static jumpImg;

  static directoionType = {
    NORMAL: "normal",
    RIGHT: "right",
    LEFT: "left",
    CHARGE: "charge"
  };

  static preload() {
    for (let i = 0; i < 3; i++) {
      this.moveRightImgs.push(loadImage(IMG_PATH + `king_right${i}.png`));
      this.moveLeftImgs.push(loadImage(IMG_PATH + `king_left${i}.png`));
    }
    this.normalRightImg = loadImage(IMG_PATH + "king_normal.png");
    this.normalLeftImg = loadImage(IMG_PATH + "king_left.png");
    this.chargeImg = loadImage(IMG_PATH + "king_charge.png");
    this.jumpImg = loadImage(IMG_PATH + "king_jump.png");
  }

  constructor(life, speed, platform, bg_musics) {
    this.alive = true;

    this.life = life;
    this.bg_musics = bg_musics;
    this.radius = KING_SIZE / 2;

    this.calCoords(platform);
    this.speed = speed;
    this.y_speed = 0;
    this.jumpStartedPosition = 0;
    this.jumpHeight = 0;
    this.score = 0;

    // image
    this.imgCounter = {
      "type": King.directoionType.NORMAL,
      "count": 0
    };
    this.normalImg = King.normalRightImg;
    this.img = this.normalImg;


    // this.jumpImgCounter_right = 8;
    // this.jumpImgCounter_left = 16;

    this.keyHandler = {
      [King.directoionType.CHARGE]: false,
      [King.directoionType.RIGHT]: false,
      [King.directoionType.LEFT]: false
    };

    // States
    this.movingRight = false;
    this.movingLeft = false;
    this.isCharging = false;
    this.isJumping = false;
    this.isFalling = false;

    this.jumpFrameCounter = 1;
    // this.fallImgCounter_right = 9;
    // this.fallImgCounter_left = 17;
  }

  calCoords(platform) {
    this.x_position = platform.x;
    this.ground = platform.y - platform.h / 2;
    this.y_position = this.ground - this.radius;
    this.platform_now = platform;
  }

  calDistance(target) {
    return Math.sqrt(
    Math.pow(this.x_position - target.x, 2) +
      Math.pow(
      this.y_position -
        (target.y - target.h / 2 - KING_SIZE / 2),
      2
      )
    );
  }

  isInRange(target) {
    let leftSide = this.x_position - this.radius / 2;
    let rightSide = this.x_position + this.radius / 2;
    if (leftSide <= target.x + target.w / 2
        && target.x - target.w / 2 <= rightSide)
      return true;
    return false;
  }

  isAbove(targetTop) {
    let footPosition = this.y_position + this.radius;
    return footPosition < targetTop;
  }

  groundUpdate(platforms) {
    this.ground = windowHeight;
    for (let platform of platforms) {
      console.log(this.ground, platform.y)
      let platformTop = platform.y - platform.h / 2;
      if (this.isAbove(platformTop) && this.isInRange(platform)) {
        this.ground = platformTop;
        this.platform_now = platform;
      }
    }
  }

  reborn(platforms) {
    this.score -= 50;
    this.life -= 1;
    this.isFalling = false;

    for (let platform of platforms) {
      if (10 < platform.y && platform.y <= windowHeight
          && (platform.platformType === Platform.platformType.NORMAL
             || platform.platformType === Platform.platformType.REACHED)) {
        this.calCoords(platform)
        return;
      }
    }
  }

  isOnPlatform() {
    if (this.isAbove(this.ground))
      return false;

    if (!this.isInRange(this.platform_now))
      return false;

    return true;
  }

  handlingKeyEvent(keyCode) {
    if (keyCode === 32) {
      this.isCharging = !this.isCharging;
      if (!this.isCharging) {
        this.isJumping = true;
      }
    } if (keyCode === RIGHT_ARROW) {
      this.movingRight = !this.movingRight;
    } if (keyCode === LEFT_ARROW) {
      this.movingLeft = !this.movingLeft;
    }
  }

  chooseImage() {
    if (this.movingRight) {
      if (this.imgCounter.type !== King.directoionType.RIGHT) {
        this.imgCounter.count = 0;
      }
      this.img = King.moveRightImgs[this.imgCounter.count++]
      this.imgCounter.type = King.directoionType.RIGHT;
      this.imgCounter.count %= 3;
    } else if (this.movingLeft) {
      if (this.imgCounter.type !== King.directoionType.LEFT) {
        this.imgCounter.count = 0;
      }
      this.img = King.moveLeftImgs[this.imgCounter.count++]
      this.imgCounter.type = King.directoionType.LEFT;
      this.imgCounter.count %= 3;
    } else {
      if (this.isCharging)
        this.img = King.chargeImg;
      else {
        if (this.imgCounter.type === King.directoionType.LEFT)
          this.normalImg = King.normalLeftImg;
        else if (this.imgCounter.type === King.directoionType.RIGHT)
          this.normalImg = King.normalRightImg;
        this.img = this.normalImg;
      }
      this.imgCounter.type = King.directoionType.NORMAL;
    }
  }

  move() {
    if (this.isFalling) {
      this.y_speed += 1;
      this.y_position += this.y_speed;
    } else if (this.isJumping) {
      this.jump();
    } else if (this.isCharging) {
      this.charge();
    } else {
      if (this.movingRight) {
        this.x_position += this.speed;
      } else if (this.movingLeft) {
        this.x_position -= this.speed;
      }
    }
  }

  update(platforms) {
    this.move();

    if (this.y_position > windowHeight) {
      this.reborn(platforms);
    } else if (this.isOnPlatform()) {
      if (!this.isAbove(this.ground))
        this.y_position = this.ground - this.radius;
      this.y_speed = 0;
      this.isFalling = false;
      this.addLandingScore();
    } else {
      if (!this.isJumping)
        this.isFalling = true;
      this.groundUpdate(platforms);
    }
  }

  displayEffects() {
    if (this.isCharging) {
      fill(150);
      stroke(150);
      let chargeBarWidth = this.radius * 1.8;
      rect(this.x_position - this.radius, this.y_position - this.radius * 1.3, chargeBarWidth, this.radius * 0.08);

      fill(255);
      stroke(255);
      let fillingWidth = (this.jumpHeight / MaxJumpHeight) * chargeBarWidth;
      rect(this.x_position - this.radius, this.y_position - this.radius * 1.3, fillingWidth, this.radius * 0.08);

      noFill();
    }
  }

  addLandingScore() {
    if (this.platform_now.platformType === Platform.platformType.GOOD) {
      this.life += 1;
      this.score += 20;
      this.platform_now.displayScore = 10;
    }
    else if (this.platform_now.platformType === Platform.platformType.BAD) {
      this.life -= 1;
      this.score -= 10;
      this.platform_now.displayScore = 10;
    }
    else if (this.platform_now.platformType === Platform.platformType.NORMAL) {
      this.score += 10;
      this.platform_now.displayScore = 10;
    }
  }

  display(platforms) {
    this.update(platforms);
    this.chooseImage();
    imageMode(CENTER);
    image(this.img, this.x_position, this.y_position, this.radius * 2, this.radius * 2);

    imageMode(CORNER);
    this.displayEffects();
  }

  charge() {
    if (this.jumpHeight < MaxJumpHeight)
      this.jumpHeight += 30
  }

  jump() {
    let radPerFrame = (2 * Math.PI) / frameRate();
    this.y_speed = -this.jumpHeight * cos(radPerFrame * this.jumpFrameCounter);

    if (this.y_speed > 0) {
      this.isJumping = false;
      this.y_speed = 0;
      this.jumpHeight = 0;
      this.jumpStartedPosition = 0;
      this.jumpFrameCounter = 1;

      this.isFalling = true;
      return;
    }

    if (!this.jumpStartedPosition) {
      this.jumpStartedPosition = this.ground;
    }
    this.y_position = -this.jumpHeight * sin(radPerFrame * this.jumpFrameCounter) + this.jumpStartedPosition;
    this.jumpFrameCounter++;
  }
}
