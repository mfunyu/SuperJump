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

    this.platform_now = platform;
    this.calCoords(platform);
    this.speed = speed;
    this.y_speed = 0;
    this.jump_start = 0;
    this.height = 0;
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

    // this.fallImgCounter_right = 9;
    // this.fallImgCounter_left = 17;
  }

  calCoords(platform) {
    this.x_position = platform.x;
    this.ground = platform.y - platform.h / 2;
    this.y_position = this.ground - this.radius;
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

  groundUpdate(platforms) {
    // Finding a ground to land on
    for (let i = platforms.length - 1; i >= 0; i--) {
    let p = platforms[i];
    if (
      this.y_position + this.radius <= p.y - p.h / 2 &&
      this.x_position >= p.x - p.w / 2 - this.radius &&
      this.x_position <= p.x + p.w / 2 + this.radius
    ) {
      this.ground = p.y - p.h / 2;
      this.platform_now = p;
      return;
    }
    }
    // If none, the bottom is the ground
    this.ground = windowHeight - MAGMA_H;
  }

  reborn(platforms) {
    // Reborn to the lowest platform after touching the magma
    for (let platform of platforms) {
    if (platform.y > 5 && platform.y <= windowHeight && platform.mark !== 1 && platform.mark !== 2) {
      this.x_position = platform.x;
      this.y_position = platform.y - platform.h / 2 - this.radius;
      this.platform_now = platform;
      return;
    }
    }
  }

  isOnPlatform() {
    if (this.y_position + this.radius < this.ground)
      return false;

    if (this.x_position + this.radius / 2 <
      this.platform_now.x - this.platform_now.w / 2 ||
    this.x_position - this.radius / 2 >
      this.platform_now.x + this.platform_now.w / 2
    ) {
      return false;
    }
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

  update(platforms) {
    this.onPlatform = this.isOnPlatform();
    if (this.onPlatform) {
      this.isFalling = false;
      this.isJumping = false;
    } else {
      if (!this.isJumping)
        this.isFalling = true;
    }
    /*
    if (this.platform_now.mark === 1 && this.onPlatform) {
    this.platform_now.mark = 0;
    this.life += 1;
    this.score += 20;
    this.platform_now.text_display = "+20";
    } else if (this.platform_now.mark === 2) {
    if (this.calDistance(this.platform_now) <= this.radius * 2) {
      this.bg_musics["lose_life"].play();
      this.platform_now.mark = 0;
      this.life -= 1;
      this.score -= 20;
      this.platform_now.text_display = "-20";
    }
    } else if (this.platform_now.mark !== 0 && this.onPlatform) {
    this.platform_now.mark = 0;
    this.score += 10;
    this.platform_now.text_display = "+10";
    }

    if (this.y_position + this.radius > windowHeight - MAGMA_H) {
    this.isFalling = false;
    this.life -= 1;
    this.bg_musics["lose_life"].play();
    this.score -= 50;
    this.reborn(platforms);
    }
    */

    // if (this.life <= 0) this.alive = false;

    if (!(this.isJumping || this.isCharging || this.isFalling)) {
      if (this.movingRight) {
        this.x_position += this.speed;
      } else if (this.movingLeft) {
        this.x_position -= this.speed;
      }
    }

    // if (!this.onPlatform) this.groundUpdate(platforms);
    // if (this.isFalling) this.fall();
  }

  display(platforms) {
    this.update(platforms);
    this.chooseImage();
    imageMode(CENTER);
    image(this.img, this.x_position, this.y_position, this.radius * 2, this.radius * 2);

    imageMode(CORNER);
  }

  fall() {
    this.y_speed += 2;
    this.y_position += this.y_speed;

    if (this.y_position + this.radius > this.ground) {
    this.y_position = this.ground - this.radius;
    this.isFalling = false;
    this.y_speed = 0;
    }
  }

  jump() {
    let radPerFrame = (2 * Math.PI) / frameRate();
    this.y_speed = -this.height * cos(radPerFrame * counter);

    if (this.y_speed > 0 && this.isJumping) {
    this.isFalling = true;
    fallstartFrame = frameCount;
    this.isJumping = false;
    counter = 1;
    this.y_speed = 0;
    this.height = 0;
    this.jump_start = 0;
    } else if (this.onPlatform || this.isJumping) {
    if (!this.jump_start) {
      this.bg_musics["charge"].play();
      this.jump_start = this.ground;
    }
    this.isJumping = true;
    this.y_position = -this.height * sin(radPerFrame * counter) + this.jump_start;
    counter++;
    }

    if (this.y_position + this.radius > this.ground) {
    this.y_position = this.ground - this.radius;
    }
  }
  }
