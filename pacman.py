import pygame  # Import the pygame library
from board import boards  # Import the boards from the board module
import math  # Import the math library
pygame.init()  # Initialize pygame

width = 900  # Set the width of the screen
height = 950  # Set the height of the screen

screen = pygame.display.set_mode((width, height))  # Set the screen size
timer = pygame.time.Clock()  # Create a clock object to manage the frame rate
fps = 60  # Set the frames per second
font = pygame.font.Font("freesansbold.ttf", 20)  # Set the font and size
level = boards  # Set the level layout from the boards module
color = ('blue')  # Set the color for drawing
pi = math.pi  # Set the value of pi
player_images = []  # Create a list to store player images
for i in range(1, 5):  # Loop to load and scale Pac-Man images for animation
    player_images.append(pygame.transform.scale(pygame.image.load(f"images/pacman{i}.png"), (45, 45)))
blinky_img = pygame.transform.scale(pygame.image.load(f"images/red.png"), (45,45)) 
pinky_img = pygame.transform.scale(pygame.image.load(f"images/pink.png"), (45,45)) 
inky_img = pygame.transform.scale(pygame.image.load(f"images/blue.png"), (45,45))  
clyde_img = pygame.transform.scale(pygame.image.load(f"images/orange.png"), (45,45))  
spooky_img = pygame.transform.scale(pygame.image.load(f"images/powerup.png"), (45,45)) 
dead_img = pygame.transform.scale(pygame.image.load(f"images/dead.png"), (45,45))  
player_x = 450  # Initial player x-position
player_y = 663  # Initial player y-position
direction = 0  # Initial direction (0=right, 1=left, 2=up, 3=down)
blinky_x = 56  # Initial Blinky x-position
blinky_y = 58  # Initial Blinky y-position
blinky_direction=0
pinky_x = 440  # Initial Pinky x-position
pinky_y = 438  # Initial Pinky y-position
pinky_direction=2
inky_x = 440  # Initial Inky x-position
inky_y = 388  # Initial Inky y-position
inky_direction=2
clyde_x = 440  # Initial Clyde x-position
clyde_y = 438  # Initial Clyde y-position
clyde_direction=2
counter = 0  # Counter for animation
flicker = False  # Flicker status
valid_turns = [False, False, False, False]  # Valid turns (Right, Left, Up, Down)
direction_command = 0  # Direction command
player_speed = 2  # Speed of player movement
score = 0  # Player score
powerup = False  # Power-up status
eaten_ghosts = [False, False, False, False]  # Ghosts eaten status
targets=[(player_x,player_y), (player_x,player_y), (player_x,player_y), (player_x,player_y)]  # Target for Ghosts
blinky_dead=False  # Blinky dead status
pinky_dead=False  # Pinky dead status
inky_dead=False  # Inky dead status
clyde_dead=False  # Clyde dead status
blinky_box=False  # Blinky box status
pinky_box=False  # Pinky box status
inky_box=False  # Inky box status
clyde_box=False  # Clyde box status
power_count = 0  # Power-up timer
start_counter = 0  # Start counter
moving = False  # Start moving status
ghost_speed=2  # Speed of ghosts
lives = 3  # Number of lives

class Ghost:  # Class for the ghosts
    def __init__(self, x_co, y_co, target, speed, img, direct, dead, box, id):
        self.x_pos = x_co  # Set x-coordinate
        self.y_pos = y_co  # Set y-coordinate
        self.center_x=self.x_pos+22  # Set center x-coordinate
        self.center_y=self.y_pos+22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collsions()
        self.rect=self.draw()

    def draw(self):  # Function to draw the ghost on the screen
        if (not powerup and not self.dead) or (eaten_ghosts[self.id] and powerup and not self.dead):  # If power-up is not active and ghost is not dead or power-up is active and ghost is dead
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghosts[self.id]:  # If power-up is active and ghost is not dead
            screen.blit(spooky_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos)) # Draw the dead ghost
        ghost_rect=pygame.Rect(int(self.center_x-18), int(self.center_y-18), 36, 36) # Create a rectangle around the ghost as a hitbox
        return ghost_rect  # Return the ghost rectangle
    
    def check_collsions(self):  # Function to check for collisions with walls
        num1 = (height - 50) // 32
        num2 = width // 30
        num3 = 15
        self.turns = [False, False, False, False]
        if self.center_x // 30 < 29: # Check if center x is within the board
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 or level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (self.in_box or self.dead): # Check right
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 or level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (self.in_box or self.dead): # Check left
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][(self.center_x + num3) // num2] < 3 or level[self.center_y // num1][self.center_x // num2] == 9 and (self.in_box or self.dead): #  Check up
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][(self.center_x - num3) // num2] < 3 or level[self.center_y // num1][self.center_x // num2] == 9 and (self.in_box or self.dead): # Check down
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3: # If direction is up or down
                if 12 <= self.center_x % num2 <= 18: # Check if center x is within a valid range
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 or level[self.center_y // num1][self.center_x // num2] == 9 and (self.in_box or self.dead): # Check up
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 or level[self.center_y // num1][self.center_x // num2] == 9 and (self.in_box or self.dead): # Check down
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18: # Check if center y is within a valid range
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 or level[self.center_y // num1][self.center_x // num2] == 9 and (self.in_box or self.dead): # Check left
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 or level[self.center_y // num1][self.center_x // num2] == 9 and (self.in_box or self.dead): # Check right
                        self.turns[0] = True
        return self.turns, self.in_box  # Return the valid turns and in box status
    
def draw_board():  # Function to render the game board based on the level layout
    num1 = ((height - 50) // 32)  # Height of each cell
    num2 = (width // 30)  # Width of each cell
    for i in range(len(level)):  # Loop through rows of the level
        for j in range(len(level[i])):  # Loop through columns of the level
            if level[i][j] == 1:  # If cell value is 1, draw a small dot
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            elif level[i][j] == 2 and not flicker:  # If cell value is 2 and not flickering, draw a big dot
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            elif level[i][j] == 3:  # If cell value is 3, draw a vertical line
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            elif level[i][j] == 4:  # If cell value is 4, draw a horizontal line
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            elif level[i][j] == 5:  # If cell value is 5, draw a top right arc
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1], 0, pi / 2, 3)
            elif level[i][j] == 6:  # If cell value is 6, draw a top left arc
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], pi / 2, pi, 3)
            elif level[i][j] == 7:  # If cell value is 7, draw a bottom left arc
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], pi, 3 * pi / 2, 3)
            elif level[i][j] == 8:  # If cell value is 8, draw a bottom right arc
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * pi / 2, 2 * pi, 3)
            elif level[i][j] == 9:  # If cell value is 9, draw a white horizontal line
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

def draw_player():  # Function to render Pac-Man on the screen based on the direction and position
    if direction == 0:  # If direction is right
        screen.blit(player_images[counter // 5], (player_x, player_y))  # Draw the player image
    elif direction == 1:  # If direction is left
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))  # Flip the image horizontally
    elif direction == 2:  # If direction is up
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))  # Rotate the image 90 degrees
    elif direction == 3:  # If direction is down
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))  # Rotate the image 270 degrees

def check_position(centerx, centery):  # Function to determine valid turns based on Pac-Man's current position and direction
    turns = [False, False, False, False]  # Initialize valid turns (Right, Left, Up, Down)
    num1 = (height - 50) // 32  # Height of each cell
    num2 = (width // 30)  # Width of each cell
    num3 = 15  # Fudge number for collision detection
    if centerx // 30 < 29:  # Check if center x is within the board
        if direction == 0:  # If direction is right
            if level[centery // num1][(centerx - num3) // num2] < 3:  # Check right
                turns[1] = True  # Set left turn as valid
        if direction == 1:  # If direction is left
            if level[centery // num1][(centerx + num3) // num2] < 3:  # Check left
                turns[0] = True  # Set right turn as valid
        if direction == 2:  # If direction is up
            if level[(centery + num3) // num1][centerx // num2] < 3:  # Check up
                turns[3] = True  # Set down turn as valid
        if direction == 3:  # If direction is down
            if level[(centery - num3) // num1][centerx // num2] < 3:  # Check down
                turns[2] = True  # Set up turn as valid

        if direction == 2 or direction == 3:  # If direction is up or down
            if 12 <= centerx % num2 <= 18:  # Check if center x is within a valid range
                if level[(centery + num3) // num1][centerx // num2] < 3:  # Check up
                    turns[3] = True  # Set down turn as valid
                if level[(centery - num3) // num1][centerx // num2] < 3:  # Check down
                    turns[2] = True  # Set up turn as valid
            if 12 <= centery % num1 <= 18:  # Check if center y is within a valid range
                if level[centery // num1][(centerx - num2) // num2] < 3:  # Check left
                    turns[1] = True  # Set left turn as valid
                if level[centery // num1][(centerx + num2) // num2] < 3:  # Check right
                    turns[0] = True  # Set right turn as valid
        if direction == 0 or direction == 1:  # If direction is right or left
            if 12 <= centerx % num2 <= 18:  # Check if center x is within a valid range
                if level[(centery + num1) // num1][centerx // num2] < 3:  # Check down
                    turns[3] = True  # Set down turn as valid
                if level[(centery - num1) // num1][centerx // num2] < 3:  # Check up
                    turns[2] = True  # Set up turn as valid
            if 12 <= centery % num1 <= 18:  # Check if center y is within a valid range
                if level[centery // num1][(centerx - num3) // num2] < 3:  # Check left
                    turns[1] = True  # Set left turn as valid
                if level[centery // num1][(centerx + num3) // num2] < 3:  # Check right
                    turns[0] = True  # Set right turn as valid
    else:  # If center x is outside the board
        turns[0] = True  # Set right turn as valid
        turns[1] = True  # Set left turn as valid

    return turns  # Return the valid turns

def move_player(play_x, play_y):  # Function to move the player in the current direction if the turn is valid
    if direction == 0 and valid_turns[0]:  # If direction is right and turn is valid
        play_x += player_speed  # Move player to the right
    elif direction == 1 and valid_turns[1]:  # If direction is left and turn is valid
        play_x -= player_speed  # Move player to the left
    elif direction == 2 and valid_turns[2]:  # If direction is up and turn is valid
        play_y -= player_speed  # Move player up
    elif direction == 3 and valid_turns[3]:  # If direction is down and turn is valid
        play_y += player_speed  # Move player down
    return play_x, play_y  # Return the new player position

def check_collisions(score, powerup, power_count, eaten_ghosts):  # Function to check for collisions with dots and big dots
    num1 = (height - 50) // 32  # Height of each cell
    num2 = width // 30  # Width of each cell
    if 0 < player_x < 870:  # Check if player x is within the board
        if level[center_y // num1][center_x // num2] == 1:  # If player collides with a small dot
            level[center_y // num1][center_x // num2] = 0  # Remove the dot
            score += 10  # Increase the score
        elif level[center_y // num1][center_x // num2] == 2:  # If player collides with a big dot
            level[center_y // num1][center_x // num2] = 0  # Remove the dot
            score += 50  # Increase the score
            powerup = True  # Activate power-up
            power_count = 0  # Reset power-up timer
            eaten_ghosts = [False, False, False, False]  # Reset eaten ghosts status

    return score, powerup, power_count, eaten_ghosts  # Return the updated values

def draw_misc():  # Function to draw miscellaneous elements on the screen
    score_text = font.render(f"Score: {score}", True, ('red'))  # Render the score text
    screen.blit(score_text, (10, 920))  # Draw the score text on the screen
    if powerup:  # If power-up is active
        pygame.draw.circle(screen, 'blue', (140, 930), 15)  # Draw the power-up indicator
    for i in range(lives):  # Loop through the number of lives
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))  # Draw the lives

run = True  # Set the run status to True
while run:  # Main game loop
    for event in pygame.event.get():  # Loop through events
        if event.type == pygame.QUIT:  # If quit event
            run = False  # Set run status to False
        if event.type == pygame.KEYDOWN:  # If key down event
            if event.key == pygame.K_RIGHT:  # If right arrow key
                direction_command = 0  # Set direction command to right
            elif event.key == pygame.K_LEFT:  # If left arrow key
                direction_command = 1  # Set direction command to left
            elif event.key == pygame.K_UP:  # If up arrow key
                direction_command = 2  # Set direction command to up
            elif event.key == pygame.K_DOWN:  # If down arrow key
                direction_command = 3  # Set direction command to down
        if event.type == pygame.KEYUP:  # If key up event
            if event.key == pygame.K_RIGHT and direction_command == 0:  # If right arrow key and direction command is right
                direction_command = direction  # Set direction command to current direction
            elif event.key == pygame.K_LEFT and direction_command == 1:  # If left arrow key and direction command is left
                direction_command = direction  # Set direction command to current direction
            elif event.key == pygame.K_UP and direction_command == 2:  # If up arrow key and direction command is up
                direction_command = direction  # Set direction command to current direction
            elif event.key == pygame.K_DOWN and direction_command == 3:  # If down arrow key and direction command is down
                direction_command = direction  # Set direction command to current direction

    for i in range(4):  # Loop through directions
        if direction_command == i and valid_turns[i]:  # If direction command matches and turn is valid
            direction = i  # Set direction to the command

    if player_x > 900:  # If player x is greater than screen width
        player_x = -47  # Wrap around to the left
    elif player_x < -50:  # If player x is less than screen width
        player_x = 897  # Wrap around to the right

    screen.fill((0, 0, 0))  # Clear the screen with black
    draw_board()  # Draw the board with dots
    draw_player()  # Draw the player
    blinky=Ghost(blinky_x, blinky_y, targets[0], ghost_speed, blinky_img, blinky_direction, blinky_dead, blinky_box, 0)  # Create blinky ghost object, 0 is the id for blinky
    inky=Ghost(inky_x, inky_y, targets[1], ghost_speed, inky_img, inky_direction, inky_dead, inky_box, 1)  # Create inky ghost object, 1 is the id for inky
    pinky=Ghost(pinky_x, pinky_y, targets[2], ghost_speed, pinky_img, pinky_direction, pinky_dead, pinky_box, 2)  # Create pinky ghost object, 2 is the id for pinky
    clyde=Ghost(clyde_x, clyde_y, targets[3], ghost_speed, clyde_img, clyde_direction, clyde_dead, clyde_box, 3)  # Create clyde ghost object, 3 is the id for Blinky
    draw_misc()  # Draw miscellaneous elements
    center_x = player_x + 23  # Calculate the center x of the player
    center_y = player_y + 24  # Calculate the center y of the player
    valid_turns = check_position(center_x, center_y)  # Check valid turns based on the player's position
    if moving:  # If moving is True
        player_x, player_y = move_player(player_x, player_y)  # Move the player
    score, powerup, power_count, eaten_ghosts = check_collisions(score, powerup, power_count, eaten_ghosts)  # Check for collisions

    pygame.display.flip()  # Update the display
    timer.tick(fps)  # Limit the frame rate to 60 fps
    if counter < 19:  # If counter is less than 19
        counter += 1  # Increment the counter
        if counter > 3:  # If counter is greater than 3
            flicker = False  # Set flicker to False
    else:  # If counter is 19 or greater
        counter = 0  # Reset the counter
        flicker = True  # Set flicker to True
    if powerup and power_count < 600:  # If power-up is active and power count is less than 600
        power_count += 1  # Increment the power count
    elif powerup and power_count >= 600:  # If power-up is active and power count is 600 or greater
        power_count = 0  # Reset the power count
        powerup = False  # Deactivate power-up
        eaten_ghosts = [False, False, False, False]  # Reset eaten ghosts status
    if start_counter < 180:  # If start counter is less than 180
        moving = False  # Set moving to False
        start_counter += 1  # Increment the start counter
    else:  # If start counter is 180 or greater
        moving = True  # Set moving to True

pygame.quit()  # Quit the game when the loop ends