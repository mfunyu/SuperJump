class Platform {
  constructor(x, y, w, h, mark, num_frames = 10) {
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
    this.num_frames = num_frames;

    this.img0 = loadImage(IMG_PATH + "brick0.png");
    this.img1 = loadImage(IMG_PATH + "brick1.png");
    this.img2 = loadImage(IMG_PATH + "magma_platform.png");

    // Randomly choose a monster image
    this.selection = Math.floor(Math.random() * 4) + 1; // 1 to 4 inclusive
    if (this.selection === 1) {
    this.img3 = loadImage(IMG_PATH + "monster1.png");
    } else if (this.selection === 2) {
    this.img3 = loadImage(IMG_PATH + "monster2.png");
    } else if (this.selection === 3) {
    this.img3 = loadImage(IMG_PATH + "monster3.png");
    } else if (this.selection === 4) {
    this.img3 = loadImage(IMG_PATH + "monster4.png");
    }

    this.frame = 0;
    this.mark = mark; // Indicates platform type: good, bad, or normal
    this.text_display = "";
  }

  display() {
    imageMode(CENTER);

    // Display platform image based on its type
    if (this.mark === 1) {
    image(this.img1, this.x, this.y, this.w, this.h); // Good platform
    } else if (this.mark === 2) {
    image(this.img2, this.x, this.y, this.w, this.h); // Bad platform
    image(
      this.img3,
      this.x,
      this.y - this.h / 2 - KING_SIZE / 2, // Position monster above platform
      KING_SIZE,
      KING_SIZE
    );
    } else {
    image(this.img0, this.x, this.y, this.w, this.h); // Normal platform
    }

    imageMode(CORNER);

    // Display score text
    if (this.text_display.length >= 3) {
    this.text_display = this.text_display.slice(0, -1); // Remove last character
    textAlign(CENTER);
    text(this.text_display, this.x, this.y);
    }
  }
}
