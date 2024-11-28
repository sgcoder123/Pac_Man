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
player_x=450
player_y=663
direction=0
counter=0
flicker=False
valid_turns=[False, False, False, False]#Right, Left, Up, Down

def draw_board():
    num1=((height-50)//32)
    num2=(width//30)
    for i in range(len(level)): #  i = row
        for j in range(len(level[i])):# j = column
            if level[i][j]==1:
                pygame.draw.circle(screen, 'white', (j*num2+(0.5*num2), i*num1+(0.5*num1)), 4) # 1 = dot #surface, color, center, radius
            elif level[i][j]==2 and not flicker:
                pygame.draw.circle(screen, 'white', (j*num2+(0.5*num2), i*num1+(0.5*num1)), 10) # 2 = big dot #surface, color, center, larger radius
            elif level[i][j]==3:
                pygame.draw.line(screen, color, (j*num2 + (0.5*num2), i*num1), (j*num2 + (0.5*num2), i*num1 + num1), 3) # 3 = vertical line #surface, color, start_pos, end_pos, line thickness
            elif level[i][j]==4:
                pygame.draw.line(screen, color, (j*num2, i*num1 + (0.5*num1)), (j*num2 + num2, i*num1 + (0.5*num1)), 3) # 4 = horizontal line #surface, color, start_pos, end_pos, line thickness
            elif level[i][j]==5:
                pygame.draw.arc(screen, color, [(j*num2-(num2*0.4))-2, (i*num1+(0.5*num1)), num2, num1], 0, pi/2, 3) # 5 = top right #surface, color, rect, start_angle, stop_angle, line thickness
            elif level[i][j]==6:
                pygame.draw.arc(screen, color, [(j*num2+(num2*0.5)), (i*num1+(0.5*num1)), num2, num1], pi/2, pi, 3) # 6 = top left #surface, color, rect, start_angle, stop_angle, line thickness
            elif level[i][j]==7:
                pygame.draw.arc(screen, color, [(j*num2+(num2*0.5)), (i*num1-(0.4*num1)), num2, num1], pi, 3*pi/2, 3) 
            elif level[i][j]==8:
                pygame.draw.arc(screen, color, [(j*num2-(num2*0.4))-2, (i*num1-(0.4*num1)), num2, num1], 3*pi/2, 2*pi, 3) 
            elif level[i][j]==9:
                pygame.draw.line(screen, 'white', (j*num2, i*num1 + (0.5*num1)), (j*num2 + num2, i*num1 + (0.5*num1)), 3)

def draw_player():
    if direction==0:#right
        screen.blit(player_images[counter//5], (player_x, player_y))
    elif direction==1:#left
        screen.blit(pygame.transform.flip(player_images[counter//5], True, False), (player_x, player_y))
    elif direction==2:#up
        screen.blit(pygame.transform.rotate(player_images[counter//5], 90), (player_x, player_y))
    elif direction==3:#down
        screen.blit(pygame.transform.rotate(player_images[counter//5], 270), (player_x, player_y))

def check_position(centerx, centery):
    valid_turns=[False, False, False, False]
    num1=(height-50)//32
    num2=(width//30)
    num3=15
    #check collions based on center x and center y of player with fudge factor of 15
    if centerx //30<29:
        if direction==0:#right
            if level [centery//num1][(centerx-num3)//num2]<3:
                valid_turns[1]=True
        if direction==1:#left
            if level [centery//num1][(centerx+num3)//num2]<3:
                valid_turns[0]=True
        if direction==2:#up
            if level [(centery+num3)//num1][(centerx-num3)//num2]<3:
                valid_turns[3]=True
        if direction==3:#down
            if level [(centery-num3)//num1][(centerx-num3)//num2]<3:
                valid_turns[2]=True
        
        if direction==2 or direction==3: 
            if 12<=centerx%num2<=18:
                if level[(centery+num3)//num1][centerx//num2]<3:
                    valid_turns[3]=True
                if level[(centery+num3)//num1][centerx//num2]<3:
                    valid_turns[2]=True
            if 12<=centery%num1<=18:
                if level[centery//num1][(centerx-num2)//num2]<3:
                    valid_turns[1]=True
                if level[centery//num1][(centerx+num2)//num2]<3:
                    valid_turns[0]=True
        if direction==0 or direction==1: 
            if 12<=centerx%num2<=18:
                if level[(centery+num1)//num1][centerx//num2]<3:
                    valid_turns[3]=True
                if level[(centery+num1)//num1][centerx//num2]<3:
                    valid_turns[2]=True
            if 12<=centery%num1<=18:
                if level[centery//num1][(centerx-num3)//num2]<3:
                    valid_turns[1]=True
                if level[centery//num1][(centerx+num3)//num2]<3:
                    valid_turns[0]=True
    else:
        vaild_turns[0]=True
        vaild_turns[1]=True
    return valid_turns


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:#right arrow key
                direction=0
            elif event.key==pygame.K_LEFT:#left arrow key
                direction=1
            elif event.key==pygame.K_UP:#up arrow key
                direction=2
            elif event.key==pygame.K_DOWN:#down arow key
                direction=3
    screen.fill((0, 0, 0))  # Clear screen with black
    draw_board()            # Draw the board with dots
    draw_player()           # Draw the player
    center_x=player_x+23
    center_y=player_y+24    
    pygame.draw.circle(screen, 'white', (center_x, center_y), 2)
    vaild_turns=check_position(center_x, center_y)

    pygame.display.flip()   # Update the display
    timer.tick(fps)        # Limit the frame rate to 60 fps
    if counter<19:
        counter+=1
        if counter>3:
            flicker=False
    else:
        counter=0
        flicker=True

pygame.quit()