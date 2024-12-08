class StaticObjects {
  static magmaImg;

  static objectType = {
    MAGMA: "magma",
    BRICKS: "bricks",
    LIFE: "life"
  }

  static objectImages;

  static preload() {
    this.magmaImg = loadImage(IMG_PATH + "magma.png");
    this.brickImg = loadImage(IMG_PATH + "sidebrick.png");
    this.lifeImg = loadImage(IMG_PATH + "heart.png");

    this.objectImages = {
      [this.objectType.MAGMA]: this.magmaImg,
      [this.objectType.BRICKS]: this.brickImg,
      [this.objectType.LIFE]: this.lifeImg
    }
  }

  constructor(type, propotion, padding = 0) {
    this.type = type;
    this.image = StaticObjects.objectImages[type];
    this.propotion = propotion;
    this.padding = padding;
  }

  displayMagma() {
    let magmaHeight = windowHeight * this.propotion;
    image(this.image, 0, windowHeight - magmaHeight, windowWidth, this.image.height);
  }

  displayBricks() {
    let y = 0;
    let bricksWidth = windowWidth * this.propotion;
    let bricksHeight =  bricksWidth * this.image.height / this.image.width;
    while (y < windowHeight) {
      image(this.image, 0, y, bricksWidth, bricksHeight);
      image(this.image, windowWidth - bricksWidth, y, bricksWidth, bricksHeight);
      y += bricksHeight;
    }
  }

  displayLife(count) {
    let lifeSize = windowWidth * this.propotion;
    let lifeDisplaySize = lifeSize * (1 - this.padding);
    let x = windowWidth - lifeSize * (1 - this.padding / 2);
    let y = lifeDisplaySize;
    for (let i = 0; i < count; i++) {
      image(this.image, x , y, lifeDisplaySize, lifeDisplaySize);
      y += lifeSize;
    }
  }

  display(count = 0) {
    if (this.type == StaticObjects.objectType.MAGMA) {
      this.displayMagma();
    }
    else if (this.type == StaticObjects.objectType.BRICKS) {
      this.displayBricks();
    }
    else if (this.type == StaticObjects.objectType.LIFE) {
      this.displayLife(count);
    }
  }
}