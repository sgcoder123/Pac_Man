import pygame
from board import boards
import math
pygame.init()

width=900
height=950

screen=pygame.display.set_mode((width,height)) # sets screen size
timer=pygame.time.Clock()
fps=60
font=pygame.font.Font("freesansbold.ttf", 20)
level=boards
color=('blue')
pi=math.pi
player_images=[]
for i in range (1,5):
    player_images.append(pygame.transform.scale(pygame.image.load(f"images/pacman{i}.png"), (45,45)))
# Load and scale Pac-Man images for animation

player_x=450
player_y=663
direction=0
counter=0
flicker=False
valid_turns=[False, False, False, False] # Right, Left, Up, Down
direction_command=0
player_speed=2
score=0
powerup = False
eaten_ghosts = [False, False, False, False]
power_count = 0
start_counter=0
moving=False
lives=3

def draw_board():
    num1=((height-50)//32)
    num2=(width//30)
    for i in range(len(level)): #  i = row
        for j in range(len(level[i])):# j = column
            if level[i][j]==1:
                pygame.draw.circle(screen, 'white', (j*num2+(0.5*num2), i*num1+(0.5*num1)), 4) # 1 = dot
            elif level[i][j]==2 and not flicker:
                pygame.draw.circle(screen, 'white', (j*num2+(0.5*num2), i*num1+(0.5*num1)), 10) # 2 = big dot
            elif level[i][j]==3:
                pygame.draw.line(screen, color, (j*num2 + (0.5*num2), i*num1), (j*num2 + (0.5*num2), i*num1 + num1), 3) # 3 = vertical line
            elif level[i][j]==4:
                pygame.draw.line(screen, color, (j*num2, i*num1 + (0.5*num1)), (j*num2 + num2, i*num1 + (0.5*num1)), 3) # 4 = horizontal line
            elif level[i][j]==5:
                pygame.draw.arc(screen, color, [(j*num2-(num2*0.4))-2, (i*num1+(0.5*num1)), num2, num1], 0, pi/2, 3) # 5 = top right arc
            elif level[i][j]==6:
                pygame.draw.arc(screen, color, [(j*num2+(num2*0.5)), (i*num1+(0.5*num1)), num2, num1], pi/2, pi, 3) # 6 = top left arc
            elif level[i][j]==7:
                pygame.draw.arc(screen, color, [(j*num2+(num2*0.5)), (i*num1-(0.4*num1)), num2, num1], pi, 3*pi/2, 3) # 7 = bottom left arc
            elif level[i][j]==8:
                pygame.draw.arc(screen, color, [(j*num2-(num2*0.4))-2, (i*num1-(0.4*num1)), num2, num1], 3*pi/2, 2*pi, 3) # 8 = bottom right arc
            elif level[i][j]==9:
                pygame.draw.line(screen, 'white', (j*num2, i*num1 + (0.5*num1)), (j*num2 + num2, i*num1 + (0.5*num1)), 3) # 9 = white horizontal line

def draw_player():
    if direction==0: # right
        screen.blit(player_images[counter//5], (player_x, player_y))
    elif direction==1: # left
        screen.blit(pygame.transform.flip(player_images[counter//5], True, False), (player_x, player_y))
    elif direction==2: # up
        screen.blit(pygame.transform.rotate(player_images[counter//5], 90), (player_x, player_y))
    elif direction==3: # down
        screen.blit(pygame.transform.rotate(player_images[counter//5], 270), (player_x, player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (height - 50) // 32
    num2 = (width // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def move_player(play_x, play_y):
    if direction == 0 and valid_turns[0]:
        play_x += player_speed
    elif direction == 1 and valid_turns[1]:
        play_x -= player_speed
    elif direction == 2 and valid_turns[2]:
        play_y -= player_speed
    elif direction == 3 and valid_turns[3]:
        play_y += player_speed
    return play_x, play_y

def check_collisions(score,powerup,power_count,eaten_ghosts):

    num1=(height-50)//32
    num2=width//30
    if 0<player_x<870:
        if level[center_y//num1][center_x//num2]==1:
            level[center_y//num1][center_x//num2]=0
            score+=10
        elif level[center_y//num1][center_x//num2]==2:
            level[center_y//num1][center_x//num2]=0
            score+=50
            powerup=True
            power_count=0
            eaten_ghosts=[False, False, False, False]

    return score,powerup,power_count,eaten_ghosts

def draw_misc():
    score_text=font.render(f"Score: {score}", True, ('red'))
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30,30)), (650+i*40, 915))
# Draw score, power-up indicator, and lives

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT: # right arrow key
                direction_command=0
            elif event.key==pygame.K_LEFT: # left arrow key
                direction_command=1
            elif event.key==pygame.K_UP: # up arrow key
                direction_command=2
            elif event.key==pygame.K_DOWN: # down arrow key
                direction_command=3
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_RIGHT and direction_command==0: # right arrow key
                direction_command=direction
            elif event.key==pygame.K_LEFT and direction_command==1: # left arrow key
                direction_command=direction
            elif event.key==pygame.K_UP and direction_command==2: # up arrow key
                direction_command=direction
            elif event.key==pygame.K_DOWN and direction_command==3: # down arrow key
                direction_command=direction
        
    for i in range(4):
        if direction_command == i and valid_turns[i]:
            direction = i

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897
        
    screen.fill((0, 0, 0))  # Clear screen with black
    draw_board()            # Draw the board with dots
    draw_player()           # Draw the player
    draw_misc()             # Draw miscellaneous elements
    center_x=player_x+23
    center_y=player_y+24    
    valid_turns=check_position(center_x, center_y)
    if moving:
        player_x, player_y=move_player(player_x, player_y)
    score, powerup, power_count, eaten_ghosts = check_collisions(score, powerup, power_count, eaten_ghosts)

    pygame.display.flip()   # Update the display
    timer.tick(fps)         # Limit the frame rate to 60 fps
    if counter<19:
        counter+=1
        if counter>3:
            flicker=False
    else:
        counter=0
        flicker=True
    if powerup and power_count<600:
        power_count+=1
    elif powerup and power_count>=600:
        power_count=0
        powerup=False
        eaten_ghosts=[False, False, False, False]
    if start_counter<180:
        moving=False
        start_counter+=1
    else:
        moving=True

pygame.quit()
# Quit the game when the loop ends