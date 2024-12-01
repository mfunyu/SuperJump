class King {
  loadImages() {
    this.rightMove_img = loadImage(IMG_PATH + "king1.png");
    this.leftMove_img = loadImage(IMG_PATH + "king0.png");
    this.jump_img = loadImage(IMG_PATH + "king8.png");
    this.charging_img = loadImage(IMG_PATH + "king7.png");
    this.normal_img = loadImage(IMG_PATH + "king0.png");
  }

  constructor(x_position, y_position, life, speed, realplatform, bg_musics) {
    this.alive = true;

    this.x_position = x_position;
    this.y_position = y_position;
    this.life = life;
    this.bg_musics = bg_musics;
    this.radius = KING_SIZE / 2;
    this.ground = this.y_position + this.radius;
    this.platform_now = realplatform;
    this.speed = speed;
    this.y_speed = 0;
    this.jump_start = 0;
    this.height = 0;
    this.score = 0;

    this.rightImgCounter = 0;
    this.leftImgCounter = 3;
    this.jumpImgCounter_right = 8;
    this.jumpImgCounter_left = 16;
    this.loadImages();
    this.img = this.normal_img;

    this.key_handler = { jump: false, right: false, left: false };

    this.isJumping = false;
    this.isFalling = false;
    this.fallImgCounter_right = 9;
    this.fallImgCounter_left = 17;
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

  check_onPlatform() {
    if (this.y_position + this.radius < this.ground) return false;

    if (
    this.x_position + this.radius / 2 <
      this.platform_now.x - this.platform_now.w / 2 ||
    this.x_position - this.radius / 2 >
      this.platform_now.x + this.platform_now.w / 2
    ) {
    if (!this.isJumping) {
      this.isFalling = true;
      fallstartFrame = frameCount;
    }
    return false;
    }

    this.isFalling = false;
    return true;
  }

  update(platforms) {
    this.onPlatform = this.check_onPlatform();

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

    if (this.life <= 0) this.alive = false;

    if (this.isJumping) this.key_handler["jump"] = false;

    if (this.key_handler["right"] && !this.key_handler["jump"]) {
    this.rightImgCounter++;
    this.rightMove_img = loadImage(
      PATH + "/images/king" + this.rightImgCounter + ".png"
    );
    if (!this.isFalling && !this.isJumping) this.img = this.rightMove_img;
    if (this.rightImgCounter === 3 || !this.key_handler["right"])
      this.rightImgCounter = 0;

    this.x_position += this.speed;
    } else if (this.key_handler["left"] && !this.key_handler["jump"]) {
    this.leftImgCounter++;
    this.leftMove_img = loadImage(
      PATH + "/images/king" + this.leftImgCounter + ".png"
    );
    if (!this.isFalling && !this.isJumping) this.img = this.leftMove_img;
    if (this.leftImgCounter === 6 || !this.key_handler["left"])
      this.leftImgCounter = 3;

    this.x_position -= this.speed;
    } else if (this.key_handler["jump"] && this.onPlatform) {
    this.img = this.charging_img;
    } else {
    this.img = this.normal_img;
    }

    if (!this.onPlatform) this.groundUpdate(platforms);
    if (this.isFalling) this.fall();
  }

  display(platforms) {
    this.update(platforms);
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
      this.bg_musics["jump"].play();
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
