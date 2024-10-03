import pygame
import numpy as np
import random

#pygame setup
pygame.init()

#initializes the screen
screen_width = 800
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True




#setting up the map

width = 16
length = 16
snake_size = length*width
snake_count =1
snake_size_image =50
body = np.full((snake_size,2), fill_value =-1, dtype = int)
move = np.zeros((snake_size,2))


tile_size_y = 19
tile_size_x =23
tile_offset_x = 13
tile_offset_y = 13


gamesizex = width*tile_size_x
gamesizey = length*tile_size_y

gamex = int(screen_width*1/2-gamesizex/2)
gamey = int(screen_height*1/2-gamesizey/2)

start_x = gamex+tile_size_x*0-tile_offset_x
start_y = gamey+tile_size_y*0-tile_offset_y

velx = 0
vely = 0


body[0] = [6,6]

headimage1 = pygame.image.load('head2.png')
headimage1 = pygame.transform.scale(headimage1,(snake_size_image,snake_size_image))
headimage2 = pygame.image.load('head1.png')
headimage2 = pygame.transform.scale(headimage2,(snake_size_image,snake_size_image))

foodimage = pygame.image.load('body.png')
foodimage = pygame.transform.scale(foodimage,(snake_size_image,snake_size_image))

dinoimage = pygame.image.load('dino.png')
dinoimage = pygame.transform.scale(dinoimage,(gamesizex,gamesizey+5))

titleimage = pygame.image.load('snakegame.png')
titleimage = pygame.transform.scale(titleimage,(700,150))

scoreimage = pygame.image.load('score.png')
scoreimage = pygame.transform.scale(scoreimage,(400,150))

gameoverimage = pygame.image.load('gameover.png')
gameoverimage = pygame.transform.scale(gameoverimage,(700,500))


scoresize = 100
oneimg = pygame.image.load('one.png')
oneimg = pygame.transform.scale(oneimg, (scoresize,scoresize))

twoimg = pygame.image.load('two.png')
twoimg = pygame.transform.scale(twoimg, (scoresize,scoresize))

threeimg = pygame.image.load('three.png')
threeimg = pygame.transform.scale(threeimg, (scoresize,scoresize))

fourimg = pygame.image.load('four.png')
fourimg = pygame.transform.scale(fourimg, (scoresize,scoresize))

fiveimg = pygame.image.load('five.png')
fiveimg = pygame.transform.scale(fiveimg, (scoresize,scoresize))

siximg = pygame.image.load('six.png')
siximg = pygame.transform.scale(siximg, (scoresize,scoresize))

sevenimg = pygame.image.load('seven.png')
sevenimg = pygame.transform.scale(sevenimg, (scoresize,scoresize))

eightimg = pygame.image.load('eight.png')
eightimg = pygame.transform.scale(eightimg, (scoresize,scoresize))

nineimg = pygame.image.load('nine.png')
nineimg = pygame.transform.scale(nineimg, (scoresize,scoresize))

zeroimg = pygame.image.load('zero.png')
zeroimg = pygame.transform.scale(zeroimg, (scoresize,scoresize))

numbers = {"1":"one",
           "2":"two",
           "3":"three",
           "4":"four",
           "5":"five",
           "6":"six",
           "7":"seven",
           "8":"eight",
           "9":"nine",
           "0":"zero"}
numimgs = {"one.png":oneimg,
           "two.png":twoimg,
           "three.png":threeimg,
           "four.png":fourimg,
           "five.png":fiveimg,
           "six.png":siximg,
           "seven.png":sevenimg,
           "eight.png":eightimg,
           "nine.png":nineimg,
           "zero.png":zeroimg
}

food = False
score =0
outofbounds = False
fx,fy=-1,-1
showscore = False

def addfood():
    global food,snake_count,fx,fy
    x = random.randint(0,20)
    if x==4 and not food:
        food = True
        fx = random.randint(0,15)
        fy = random.randint(0,15)
        for i in range(snake_count):
            if body[i][0]==fx and body[i][1]==fy:
                food=False
    if food:
        if(body[0][0]==fx and body[0][1]==fy):
            snake_count+=1
            food=False
            fx,fy=-1,-1
        

        


def updatebody(dpx, dpy): #updates the list of movements keep track of all of them as they come in
    global outofbounds

    for i in reversed(range(len(move))):
        if(dpx==0 and dpy==0):
            continue
        if i ==0:
            body[0][0]+=dpx
            body[0][1]+=dpy
            if body[0][0] < 0 or body[0][0] > 15 or body[0][1]<0 or body[0][1]>15:
                outofbounds = True
            #if body[0][0]==body[2][0] and body[0][1]==body[2][1]and snake_count>1:
             #   outofbounds = True
              #  print(body[0])
               # print(body[1])
            
        else:
            body[i]=body[i-1]
            if(body[i][0]==body[0][0]+dpx and body[i][1]==body[0][1]+dpy) and snake_count>1 and i<snake_count:
                outofbounds = True
    

def fillboard():
    screen.fill("black")
    screen.blit(dinoimage, (gamex,gamey-2,gamesizex,gamesizey+6))

    for i in range(snake_count):
        if i==0:
            if dir:
                screen.blit(headimage1, (start_x,start_y) + body[0]*(tile_size_x,tile_size_y))
            else:
                screen.blit(headimage2, (start_x,start_y) + body[0]*(tile_size_x,tile_size_y))
        else:
            if(body[i][0]!=-1):
                screen.blit(foodimage,(start_x,start_y) + body[i]*(tile_size_x,tile_size_y))
    if fx!=-1:
        screen.blit(foodimage,(fx*tile_size_x+start_x,fy*tile_size_y+start_y))

    printscore()


def endscreen():
    #do what happens when the game ends
    print("game over!")
    screen.fill("black")
    screen.blit(scoreimage,(50,540))
    screen.blit(gameoverimage,(0,0))

    index=0
    for i in score:
        imgname = numbers[i]+".png"
        screen.blit(numimgs[imgname],(450+index*80,540))
        index+=1


def printscore():
    global score
    score = str(snake_count-1)
    index=0
    for i in score:
        imgname = numbers[i]+".png"
        screen.blit(numimgs[imgname],(450+index*80,550))
        index+=1

    screen.blit(scoreimage,(50,530))
    screen.blit(titleimage,(50,40))

def update():
    global running
    
    updatebody(velx,vely) #updates the body position
    addfood()
    if outofbounds:
        endscreen()
        #running = False
    else:
        fillboard() #displayes the board 
    
    
   # pygame.draw.rect(screen,"red",[body[0][0]+tile_offset_x,body[0][1]+tile_offset_y,tile_size_x,tile_size_y])

    pygame.display.update()
    clock.tick(8)


#while the game is running
while running:
     #polls for events in the game
    
    events = pygame.event.get()
    for event in events:
        #checks for the user closing the window
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            dir=not dir
            if event.key == pygame.K_a:
                velx=-1
                vely=0
            elif event.key == pygame.K_d:
                velx=1
                vely=0
            elif event.key == pygame.K_w:
                velx=0
                vely=-1
            elif event.key == pygame.K_s:
                velx=0
                vely=1
            else:
                continue
            update()     
    if(not events):
        update()

        
pygame.quit() #quits