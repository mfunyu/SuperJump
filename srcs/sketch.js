let img;
let RESX = 800;
let RESY = RESX * 2/3;

function preload() {
  imgBackground = loadImage("images/background.png");
  // let loadStatus = NOT_STARTED;
}

function setup() {
    createCanvas(RESX, RESY);
    background(0);
}

function draw() {
    background(0); // Clear the canvas
    // if (loadStatus === NOT_STARTED) {
    startupScreen("Loading ... ");
    //     loadStatus = LOADING;
    // } else if (loadStatus === LOADING && !game) {
    //     game = new Game(bgMusics);
    // } else if (game && game.play) {
    //     game.display();
    // } else if (game && game.king.alive) {
    //     startupScreen("Click Anywhere to Start");
    //     loadStatus = LOADED;
    // } else if (game) {
    //     game.gameover();
    // }
    image(speakerImg, 10, RESY - 100, 80, 80); // Display speaker icon
}

function startupScreen(displayText) {
    // Display the startup screen
    image(imgBackground, 0, 0, width, height);
    imageMode(CENTER);

    fill(255);
    textAlign(CENTER);
    textSize(RESX * 0.03);
    textFont("3270SemiNarrow");
    text("How to Play", width / 2, height * 2 / 5);
    text("<- : left\n-> : right\nSPACE BAR : jump", width * 1 / 4, height / 2);
    text("Blue platforms: life + 1\nMonsters: life - 1\n(press: charging, release: start jump)", width * 2 / 3, height / 2);
    text(displayText, width / 2, height * 4 / 5);
}

function keyPressed() {
    // Handle key presses
    if (game && game.king) {
        if (keyCode === LEFT_ARROW) game.king.keyHandler['left'] = true;
        if (keyCode === RIGHT_ARROW) game.king.keyHandler['right'] = true;
        if (key === ' ') game.king.keyHandler['jump'] = true;
    }
}

function keyReleased() {
    // Handle key releases
    if (game && game.king) {
        if (keyCode === LEFT_ARROW) game.king.keyHandler['left'] = false;
        if (keyCode === RIGHT_ARROW) game.king.keyHandler['right'] = false;
        if (key === ' ') game.king.keyHandler['jump'] = false;
    }
}

function mousePressed() {
    // Mute/unmute or start/restart game
    if (mouseX >= 0 && mouseX <= 100 && mouseY >= RESY - 100 && mouseY <= RESY) {
        // Toggle mute
        for (let music in bgMusics) {
            if (bgMusics[music].isPlaying()) {
                bgMusics[music].stop();
                speakerImg = muteImg;
            } else {
                bgMusics[music].play();
                speakerImg = unmuteImg;
            }
        }
    } else if (loadStatus === LOADED && !game.king.alive) {
        // Restart game
        loadStatus = NOT_STARTED;
        game = null;
    } else if (loadStatus === LOADED && !game.play) {
        // Start game
        game.play = true;
        game.time = millis();
    }
}