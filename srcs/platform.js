const HORIZONTAL_MAX = 200
const JUMP_HIGHET = 20

class Platform {
  static minWidth = 100;
  static maxWidth = 200;
  static minHeight = 30;
  static maxHeight = 60;

  static platformNormalImg;
  static platformSpecialImg;
  static platformMagmaImg;

  static platformType = {
    NORMAL: "normal",
    GOOD: "good",
    BAD: "bad"
  }

  static platformImages;

  static platformWeights = {
    [this.platformType.NORMAL]: 7,
    [this.platformType.GOOD]: 2,
    [this.platformType.BAD]: 1
  }

  static platformOptions = [];

  static {
    this.platformOptions = [];
    for (let platformType in this.platformWeights) {
      for (let i = 0; i < this.platformWeights[platformType]; i++) {
        this.platformOptions.push(platformType);
      }
    }
  }

  static preload() {
    // Load platform images
    this.platformNormalImg = loadImage(IMG_PATH + "platform_normal.png");
    this.platformSpecialImg = loadImage(IMG_PATH + "platform_special.png");
    this.platformMagmaImg = loadImage(IMG_PATH + "platform_magma.png");

    this.platformImages = {
      [this.platformType.NORMAL]: this.platformNormalImg,
      [this.platformType.GOOD]: this.platformSpecialImg,
      [this.platformType.BAD]: this.platformMagmaImg
    }

    this.img3 = loadImage(IMG_PATH + "monster1.png");
    this.img4 = loadImage(IMG_PATH + "monster2.png");
    this.img5 = loadImage(IMG_PATH + "monster3.png");
    this.img6 = loadImage(IMG_PATH + "monster4.png");
  }

  constructor(x, y, w, h, platformType = undefined) {
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;

    // Randomly choose a monster image
    // this.selection = Math.floor(Math.random() * 4) + 1; // 1 to 4 inclusive
    // if (this.selection === 1) {
    // this.img3 = loadImage(IMG_PATH + "monster1.png");
    // } else if (this.selection === 2) {
    // this.img3 = loadImage(IMG_PATH + "monster2.png");
    // } else if (this.selection === 3) {
    // this.img3 = loadImage(IMG_PATH + "monster3.png");
    // } else if (this.selection === 4) {
    // this.img3 = loadImage(IMG_PATH + "monster4.png");
    // }

    this.platformType = this.choosePlatformType(platformType);
    this.text_display = "";
  }

  choosePlatformType(platformType) {
    if (platformType)
      return platformType;

    return Platform.platformOptions[Math.floor(Math.random() * Platform.platformOptions.length)];
  }

  display() {
    imageMode(CENTER);
    console.log("Platform.platformImages[this.platformType]: ", Platform.platformImages[this.platformType]);
    console.log(Platform.platformImages);
    image(Platform.platformImages[this.platformType], this.x, this.y, this.w, this.h);

    // // Display platform image based on its type
    // if (this.mark === 1) {
    //   image(this.img1, this.x, this.y, this.w, this.h); // Good platform
    // } else if (this.mark === 2) {
    //   image(this.img2, this.x, this.y, this.w, this.h); // Bad platform
    // image(
    //   this.img3,
    //   this.x,
    //   this.y - this.h / 2 - KING_SIZE / 2, // Position monster above platform
    //   KING_SIZE,
    //   KING_SIZE
    // );
    // } else {
    // image(this.img0, this.x, this.y, this.w, this.h); // Normal platform
    // }

    imageMode(CORNER);

    // Display score text
    if (this.text_display.length >= 3) {
      this.text_display = this.text_display.slice(0, -1); // Remove last character
      textAlign(CENTER);
      text(this.text_display, this.x, this.y);
    }
  }

  static createNewPlatform(previousPlatform, speed) {
    let width, height, xCoord, yCoord;
    let isPlatformValid = false;

    while (!isPlatformValid) {
      width = random(Platform.minWidth, Platform.maxWidth);
      height = random(Platform.minHeight, Platform.maxHeight);
      let randomXDistance = random(0.3 * Math.tanh(speed) * HORIZONTAL_MAX, 0.6 * Math.tanh(speed) * HORIZONTAL_MAX);
      let randomYDistance = random(2 * Math.tanh(speed) * JUMP_HIGHET, 3 * Math.tanh(speed) * JUMP_HIGHET);
      let newXCoordOnRight = previousPlatform.x + previousPlatform.w + randomXDistance;
      let newXCoordOnLeft = previousPlatform.x - randomXDistance - width;

      xCoord = random([newXCoordOnRight, newXCoordOnLeft]);
      yCoord = previousPlatform.y - randomYDistance - height;
      isPlatformValid = (windowWidth * 0.05 <= xCoord - width / 2 && xCoord + width / 2 <= windowWidth * 0.95);
      console.log("xCoord: ", xCoord, "yCoord: ", yCoord, "width: ", width, "height: ", height);
    }

    return new Platform(xCoord, yCoord, width, height);
  }
}
