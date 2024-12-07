# Pac-Man Game in Python with Pygame

This project recreates the classic Pac-Man game using the Pygame library in Python. It includes all the essential features of Pac-Man, including player movement, ghost AI, power-ups, and collision detection.

## Features

- Classic Pac-Man gameplay
- Player movement in four directions
- Ghost AI with different behaviors for each ghost
- Power-ups that make ghosts vulnerable
- Collision detection between player, ghosts, and dots
- Score tracking and lives system
- Game over and victory conditions

## Installation

1. Clone the repository to your local machine:
    ```sh
    git clone https://github.com/yourusername/pacman-python.git
    ```

2. Navigate to the project directory:
    ```sh
    cd pacman-python
    ```

3. Install the required dependencies:
    ```sh
    pip install pygame
    ```

4. Ensure the `assets` directory contains the necessary images for the player and ghosts.

## Usage

1. Run the game:
    ```sh
    python pacman.py
    ```

2. Use the arrow keys to move Pac-Man:
    - Right arrow: Move right
    - Left arrow: Move left
    - Up arrow: Move up
    - Down arrow: Move down

3. Collect all the dots to win the game. Avoid the ghosts unless you have a power-up, which allows you to eat the ghosts for extra points.

4. If you lose all your lives, the game is over. Press the space bar to restart the game.

## File Structure

- `pacman.py`: Main game file containing the game logic and Pygame loop.
- `assets/`: Directory containing images for the player and ghosts.
- `board.py`: Contains the level layout for the game.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please create a pull request or open an issue.

## Acknowledgements

- Inspired by the classic Pac-Man game.
- Built using the Pygame library.

Enjoy playing Pac-Man!
