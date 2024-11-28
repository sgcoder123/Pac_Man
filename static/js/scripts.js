const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let pacMan = {
    x: 50,
    y: 50,
    radius: 15,
    speed: 2.5,
    direction: 'right'
};

document.addEventListener('keydown', (event) => {
    switch(event.key) {
        case 'ArrowUp':
        case 'w':
            pacMan.direction = 'up';
            break;
        case 'ArrowDown':
        case 's':
            pacMan.direction = 'down';
            break;
        case 'ArrowLeft':
        case 'a':
            pacMan.direction = 'left';
            break;
        case 'ArrowRight':
        case 'd':
            pacMan.direction = 'right';
            break;
    }
});

function update() {
    switch(pacMan.direction) {
        case 'up':
            pacMan.y -= pacMan.speed;
            break;
        case 'down':
            pacMan.y += pacMan.speed;
            break;
        case 'left':
            pacMan.x -= pacMan.speed;
            break;
        case 'right':
            pacMan.x += pacMan.speed;
            break;
    }

    // Boundary checks
    if (pacMan.x - pacMan.radius < 0) {
        pacMan.x = pacMan.radius;
    }
    if (pacMan.x + pacMan.radius > canvas.width) {
        pacMan.x = canvas.width - pacMan.radius;
    }
    if (pacMan.y - pacMan.radius < 0) {
        pacMan.y = pacMan.radius;
    }
    if (pacMan.y + pacMan.radius > canvas.height) {
        pacMan.y = canvas.height - pacMan.radius;
    }
}

let mouthOpen = true;
let mouthToggleCounter = 0;

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(pacMan.x, pacMan.y);

    let startAngle, endAngle, eyeX, eyeY;
    if (mouthOpen) {
        switch(pacMan.direction) {
            case 'up':
                startAngle = 1.75 * Math.PI;
                endAngle = 1.25 * Math.PI;
                break;
            case 'down':
                startAngle = 0.75 * Math.PI;
                endAngle = 0.25 * Math.PI;
                break;
            case 'left':
                startAngle = 1.25 * Math.PI;
                endAngle = 0.75 * Math.PI;
                break;
            case 'right':
            default:
                startAngle = 0.25 * Math.PI;
                endAngle = 1.75 * Math.PI;
                break;
        }
    } else {
        startAngle = 0;
        endAngle = 2 * Math.PI;
    }
    //Pac-Man face
    ctx.beginPath();
    ctx.arc(0, 0, pacMan.radius, startAngle, endAngle);
    ctx.lineTo(0, 0);
    ctx.fillStyle = 'yellow';
    ctx.fill();
    ctx.closePath();

    // Draw Pac-Man's eye
    ctx.beginPath();
    ctx.arc(-pacMan.radius / 3, -pacMan.radius / 2, pacMan.radius / 5, 0, 2 * Math.PI);
    ctx.fillStyle = 'black';
    ctx.fill();
    ctx.closePath();

    ctx.restore();

    mouthToggleCounter++;
    if (mouthToggleCounter >= 10) { // Adjust this value to control the speed
        mouthOpen = !mouthOpen;
        mouthToggleCounter = 0;
    }
}

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

gameLoop();
