const GAME_SPEED = 3

class Background {
  constructor(background_images) {
    this.coord_y_first = 0; // y position
    this.coord_y_second = 0; // y position
    this.speed = GAME_SPEED;


    this.images = background_images;

    this.altitude = 0;
    this.image_index = 0;
    this.total_img_height = this.images[this.image_index].height;
  }

  display() {
    while (this.total_img_height < this.altitude) {
      this.image_index++;
      this.total_img_height += this.images[this.image_index].height;
    }

    let visible_img_size = 0;
    for (let i = 0; windowHeight > visible_img_size; i++) {
      let image_index = Math.min(this.image_index + i, this.images.length - 1);
      let current_img = this.images[image_index];

      if (i == 0)
        visible_img_size = this.total_img_height - this.altitude;
      else
        visible_img_size += current_img.height;

      let y_coordinate = windowHeight - visible_img_size
      image(current_img, 0, y_coordinate, windowWidth, current_img.height);
    }
    this.scroll();
  }

  scroll() {
    this.altitude += this.speed * 0.5;
  }
}