class Background {
  static GAME_SPEED = 3;
  static NUM_BG_IMGS = 5;
  static images = [];

  static preload() {
    for (let i = 0; i < this.NUM_BG_IMGS; i++) {
      this.images.push(loadImage(IMG_PATH + `bg${i}.png`));
    }
  }

  constructor() {
    this.altitude = 0;
    this.image_index = 0;
    this.total_img_height = Background.images[this.image_index].height;

    this.speed = Background.GAME_SPEED;
  }

  display() {
    while (this.total_img_height < this.altitude) {
      this.image_index++;
      this.total_img_height += Background.images[this.image_index].height;
    }

    let visible_img_height = 0;
    for (let i = 0; windowHeight > visible_img_height; i++) {
      let image_index = Math.min(this.image_index + i, Background.NUM_BG_IMGS);
      let current_img = Background.images[image_index];

      if (i == 0)
        visible_img_height = this.total_img_height - this.altitude;
      else
        visible_img_height += current_img.height;

      let y_coordinate = windowHeight - visible_img_height
      image(current_img, 0, y_coordinate, windowWidth, current_img.height);
    }
    this.scroll();
  }

  scroll() {
    this.altitude += this.speed * 0.5;
  }
}