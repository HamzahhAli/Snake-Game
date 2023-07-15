
import pygame
import time
import random 
from sys import exit
pygame.init()
pygame.mixer.init()
# pygame.mixer.music.load('projects/items/backgroundsound.mp3')
# pygame.mixer.music.play()
#1000,500
window = pygame.display.set_mode((510,510))
pygame.display.set_caption('Snake')

length = 1
size = 30
BG = (51,51,51)
window.fill(BG)

font = pygame.font.SysFont('arial', 15, bold = True)
surf = font.render('▐▐ ', True, 'white')

pausebtn = pygame.Rect(10,10,20,20)
fonted = pygame.font.SysFont('arial', 15, bold = True)
surfed = fonted.render('Resume', True, 'white')

pausedbtn = pygame.Rect(250,250,250,250)
resumebtn = pygame.image.load('projects/items/resumebutton.png').convert()
resumebtnrect = pygame.Rect(200,135,100,1000)

quitbtn = pygame.image.load('projects/items/quitbutton.png').convert()
quitbtnrect = pygame.Rect(200,250,200,250)

startbtn = pygame.image.load('projects/items/startbutton.png').convert()
startbtnrect = pygame.Rect(200,250,200,250)

snake = pygame.image.load('projects/items/block.jpg').convert()
snakex = [size]*length
snakey = [size]*length

rx = 240
ry = 240

direction = 'right'
# window.blit(snake,(snakex,snakey))

food = pygame.image.load('projects/items/apple.jpg').convert()
# window.blit(food,(10,10))
pygame.display.flip() 

freeze = False
pause = False
showbutton = True

def drawApple():
     global rx
     global ry
     window.blit(food,(rx,ry))
     pygame.display.flip()

def drawSnake():
    window.fill(BG)
    for i in range(length):
        window.blit(snake,(snakex[i],snakey[i]))
    # drawApple()
    pygame.display.flip() 

def up():
     global direction
     direction = 'up'
def down():
     global direction
     direction = 'down'
def left():
     global direction
     direction = 'left'
def right():
     global direction
     direction = 'right'

def walk(direction):
     global length
     global snakex
     global snakey
     for i in range(length-1,0,-1):
          snakex[i] = snakex[i-1]
          snakey[i] = snakey[i-1]
     
     if direction == 'up':
          snakey[0] -= 30
     elif direction == 'down':
          snakey[0] += 30
     elif direction == 'right':
          snakex[0] += 30
     elif direction == 'left':
          snakex[0] -= 30
     drawSnake()

def grow():
     global length
     length += 1
     snakex.append(-1)
     snakey.append(-1)
     

def respawn():
     global rx
     global ry
     rx = random.randint(1,16)*30
     ry = random.randint(1,16)*30
     
     
def hit():
     if snakex[0] >= rx and snakex[0] < rx + size:
         if snakey[0] >= ry and snakey[0] < ry + size:
           return True
     return False
    
def score():
     fontstyle = pygame.font.SysFont('gotgothic16', 40) 
     display = fontstyle.render(f'{length}', True, (255,255,255)) 
     window.blit(display, (240,3)) 
       
     pygame.display.flip()

def paused():
    global pause
    pause = True
    window.fill(BG)
    drawSnake()
    score()
    pygame.draw.rect(window, (0, 90, 156), (115, 100, 300, 300))

    window.blit(resumebtn,(165,150))
    window.blit(quitbtn, (200,250))

    pausesound = pygame.mixer.Sound('projects/items/pausesound.mp3')
    pygame.mixer.Sound.play(pausesound)
    pygame.display.flip()

def unpaused():
    global pause
    pause = False
    
def selfDestruct():
     if snakex[0] >= snakex[i] and snakex[0] < snakex[i] + size:
         if snakey[0] >= snakey[i] and snakey[0] < snakey[i] + size:
           return True
     
     return False

def gameover():
     crash = pygame.mixer.Sound('projects/items/hit.mp3') 
     pygame.mixer.Sound.play(crash)
     global freeze
     window.fill(BG)
     fontstyle = pygame.font.SysFont('bold arial', 60) 
     display = fontstyle.render(f'GAME OVER', True, (255,255,255)) 
     window.blit(display, (138,220))
     scorefontstyle = pygame.font.SysFont('bold arial', 20) 
     scoredisplay = scorefontstyle.render(f'Press ENTER to restart', True, (255,255,255)) 
     window.blit(scoredisplay, (190,270)) 
     pygame.display.flip()
     freeze = True
def restart():
     global length, snakex, snakey, direction, freeze
     length = 1
     snakex = [size] * length
     snakey = [size] * length
     direction = 'right'
     freeze = False

def startmenu():
     window.fill((255,255,255))
     pygame.display.flip()
 
clicked = False
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()   
            exit()  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            elif event.key == pygame.K_RETURN:
                 freeze = False
            if not freeze:
               if event.key == pygame.K_UP:
                    up()
               elif event.key == pygame.K_DOWN:
                    down()
               elif event.key == pygame.K_RIGHT:
                    right()
               elif event.key == pygame.K_LEFT:
                    left()
               elif event.key == pygame.K_RETURN:
                    restart()
               elif event.key == pygame.K_SPACE:
                    paused()
         
        if event.type == pygame.MOUSEBUTTONDOWN:
          if pausebtn.collidepoint(event.pos):
               clicked = True
               paused()
          if resumebtnrect.collidepoint(event.pos):
               unpaused()
          if quitbtnrect.collidepoint(event.pos):
               pygame.quit()
               exit()
                         
    if not freeze:
        if not pause:
          walk(direction)
          drawApple()
          score()
          if showbutton:
               pygame.draw.rect(window, (51,51,51), pausebtn)
               window.blit(surf,(pausebtn.x, pausebtn.y )) 
               pygame.display.flip()
          for i in range(3,length):
               if selfDestruct():
                    crash = pygame.mixer.Sound('projects/items/hit.mp3')
                    pygame.mixer.Sound.play(crash)
                    gameover()
                
          if hit():
               bite = pygame.mixer.Sound('projects/items/bite.mp3')
               pygame.mixer.Sound.play(bite)

               grow()
               respawn()
          clicked = False
          if snakex[0] > 510 or snakex[0] < 0 or snakey[0] > 510 or snakey[0] < 0:
               crash = pygame.mixer.Sound('projects/items/hit.mp3')
               pygame.mixer.Sound.play(crash)
               gameover() 
      
    time.sleep(0.1) 


 
#---------------Credit-----------------
#https://emojicombos.com/pause-symbol pause
#https://pixabay.com/service/license-summary/ audio