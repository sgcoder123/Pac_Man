const canvas = document.getElementById('gameCanvas'); // Get the canvas element by its ID
const ctx = canvas.getContext('2d'); // Get the 2D drawing context for the canvas

let pacMan = {
    x: 400, // Initial x-coordinate of Pac-Man
    y: 550, // Initial y-coordinate of Pac-Man
    radius: 15, // Radius of Pac-Man
    speed: 2.5, // Speed at which Pac-Man moves
    direction: 'right' // Initial direction of Pac-Man
};

document.addEventListener('keydown', (event) => { // Add an event listener for keydown events
    switch(event.key) { // Change Pac-Man's direction based on the key pressed
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

function checkCollision(x, y) {
    return terrain.some(wall => 
        x + pacMan.radius > wall.x && 
        x - pacMan.radius < wall.x + wall.width && 
        y + pacMan.radius > wall.y && 
        y - pacMan.radius < wall.y + wall.height
    );
}

function update() {
    let newX = pacMan.x;
    let newY = pacMan.y;

    switch(pacMan.direction) { // Update Pac-Man's position based on the direction
        case 'up':
            newY -= pacMan.speed;
            break;
        case 'down':
            newY += pacMan.speed;
            break;
        case 'left':
            newX -= pacMan.speed;
            break;
        case 'right':
            newX += pacMan.speed;
            break;
    }

    // Boundary checks to keep Pac-Man within the canvas
    if (newX - pacMan.radius < 0 || newX + pacMan.radius > canvas.width || 
        newY - pacMan.radius < 0 || newY + pacMan.radius > canvas.height || 
        checkCollision(newX, newY)) {
        return; // Prevent movement if it would result in a collision
    }

    pacMan.x = newX;
    pacMan.y = newY;
}

let mouthOpen = true; // Boolean to track if Pac-Man's mouth is open
let mouthToggleCounter = 0; // Counter to control the speed of mouth opening and closing

const squareSize = 20; // Size of each square in the grid
const margin = 15; // Margin between lines

const terrain = [
    // Vertical walls
    { x: 100, y: 100, width: squareSize, height: 200 },
    { x: 200, y: 300, width: squareSize, height: 200 },
    { x: 300, y: 100, width: squareSize, height: 200 },
    { x: 400, y: 300, width: squareSize, height: 200 },
    { x: 500, y: 100, width: squareSize, height: 200 },
    { x: 600, y: 300, width: squareSize, height: 200 },
    // Curved walls
    { x: 150, y: 150, width: 100, height: squareSize },
    { x: 150, y: 150, width: squareSize, height: 100 },
    { x: 450, y: 150, width: 100, height: squareSize },
    { x: 450, y: 150, width: squareSize, height: 100 },
    { x: 150, y: 450, width: 100, height: squareSize },
    { x: 150, y: 450, width: squareSize, height: 100 },
    { x: 450, y: 450, width: 100, height: squareSize },
    { x: 450, y: 450, width: squareSize, height: 100 }
];

function drawTerrain() {
    ctx.fillStyle = 'black';
    for (let x = 0; x < canvas.width; x += squareSize) {
        for (let y = 0; y < canvas.height; y += squareSize) {
            ctx.fillRect(x, y, squareSize, squareSize);
        }
    }
}

function drawSetTerrain() {
    ctx.fillStyle = 'blue';
    terrain.forEach(wall => {
        ctx.fillRect(wall.x, wall.y, wall.width, wall.height);
    });
}

function drawBorder() {
    ctx.fillStyle = 'blue';
    for (let x = 0; x < canvas.width; x += squareSize) {
        ctx.fillRect(x, 0, squareSize, squareSize); // Top border
        ctx.fillRect(x, canvas.height - squareSize, squareSize, squareSize); // Bottom border
    }
    for (let y = 0; y < canvas.height; y += squareSize) {
        ctx.fillRect(0, y, squareSize, squareSize); // Left border
        ctx.fillRect(canvas.width - squareSize, y, squareSize, squareSize); // Right border
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
    drawTerrain(); // Draw the terrain
    drawSetTerrain(); // Draw the set terrain
    drawBorder(); // Draw the border
    ctx.save(); // Save the current drawing state
    ctx.translate(pacMan.x, pacMan.y); // Move the origin to Pac-Man's position

    let startAngle, endAngle;
    switch(pacMan.direction) { // Set the angles for Pac-Man's mouth based on the direction
        case 'up':
            startAngle = mouthOpen ? 1.75 * Math.PI : 0;
            endAngle = mouthOpen ? 1.25 * Math.PI : 2 * Math.PI;
            break;
        case 'down':
            startAngle = mouthOpen ? 0.75 * Math.PI : 0;
            endAngle = mouthOpen ? 0.25 * Math.PI : 2 * Math.PI;
            break;
        case 'left':
            startAngle = mouthOpen ? 1.25 * Math.PI : 0;
            endAngle = mouthOpen ? 0.75 * Math.PI : 2 * Math.PI;
            break;
        case 'right':
        default:
            startAngle = mouthOpen ? 0.25 * Math.PI : 0;
            endAngle = mouthOpen ? 1.75 * Math.PI : 2 * Math.PI;
            break;
    }

    // Draw Pac-Man's face
    ctx.beginPath();
    ctx.arc(0, 0, pacMan.radius, startAngle, endAngle);
    ctx.lineTo(0, 0);
    ctx.fillStyle = 'yellow';
    ctx.fill();
    ctx.closePath();

    ctx.restore(); // Restore the previous drawing state

    mouthToggleCounter++; // Increment the mouth toggle counter
    if (mouthToggleCounter >= 15) { // Toggle mouth open/close every 15 frames
        mouthOpen = !mouthOpen;
        mouthToggleCounter = 0;
    }
}

function gameLoop() {
    update(); // Update Pac-Man's position
    draw(); // Draw Pac-Man
    requestAnimationFrame(gameLoop); // Request the next frame
}

gameLoop(); // Start the game loop
