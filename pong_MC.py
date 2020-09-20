#!/usr/bin/python
import numpy as np
import pygame 
from setup import setup
import matplotlib.pyplot as plt

# Color definition for printing
R  = '\033[1;31m' # red
G  = '\033[1;32m' # green
W  = '\033[0m'  # white (normal)
BLACK = (0,0,0); WHITE = (255,255,255); GREEN = (0,255,0)
pygame.init()
        
env = setup();
        
screen = pygame.display.set_mode(env.size)
pygame.display.set_caption('Monte Carlo')        
        
def encode(bx,by,bdir,padx,cmd):
    result = bx*2**12+by*2**8+bdir*2**6+padx*2**2+cmd
    if result>131072:
        print('Out of Bounds', result,  bx, by, bdir, padx, cmd)
    return int(result)

#draws the paddle. Also restricts its movement between the edges
#of the window.
def drawrect(screen,x,y):
    if x <= 0:
        x = 0
    if x >= 210:
        x = 210    
    pygame.draw.rect(screen,GREEN,[x,y,90,15])
   
#game's main loop    
done = False
clock=pygame.time.Clock()

num_games = 0
num_wins  = 0

# Open file to record stats
file = open('stats.txt','w')
file.write('%s,%s\n' % (str(0),str(0)))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    #  we need to pick left, right or stay randomly
    # We need to check if any of the three commands wins
    dirx = env.ball_change_x/15 
    diry = env.ball_change_y/15 
    print('dirx' , dirx , 'diry' , diry, 'ballx', env.ball_x, 'bally', env.ball_y, 'paddlex', env.rect_x)
  #  print('ball_change_x', ball_change_x, 'ball_change_y', ball_change_y)
    if dirx == -1:
        dirx = 0
    else:
        dirx = 1
    if diry == -1:
        diry = 0
    else:
        diry = 1
    
    dirval = env.direction[dirx,diry]
    test1 = encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,0)
    test2 = encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,1)
    test3 = encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,2)
    if env.Q[test1] > env.Q[test2] and env.Q[test1] > env.Q[test3]:
        cmd = 0  # left
        env.rect_change_x = -15
        print(G+'***************** MOVE LEFT *****************' +W)
        print('test1 - max',env.Q[test1],'test2',env.Q[test2],'test3',env.Q[test3])
        env.episode = np.append(env.episode,encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,cmd))
    elif env.Q[test2] > env.Q[test1] and env.Q[test2] > env.Q[test3]:
        cmd = 1  # right
        env.rect_change_x = 15
        print(G+'***************** MOVE RIGHT *****************'+W)
        print('test1',env.Q[test1],'test2 - max',env.Q[test2],'test3',env.Q[test3])
        env.episode = np.append(env.episode,encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,cmd))
    elif env.Q[test3] > env.Q[test1] and env.Q[test3] > env.Q[test2]:
        cmd = 0 # no move
        env.rect_change_x = 0
        print(G+'***************** DO NOT MOVE *****************'+W)
        print('test1',env.Q[test1],'test2',env.Q[test2],'test3 - max',env.Q[test3])
        env.episode = np.append(env.episode,encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,cmd))
    else:
        print(R+'================= RANDOM MOVE ================='+W)
        rndnumber  = np.random.randint(0,100)
        if rndnumber< 35:
            # this will be left position
            cmd=0
            env.rect_change_x = -15
            env.episode = np.append(env.episode,encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,cmd))
        elif rndnumber <70:
            cmd = 1
            env.rect_change_x = +15
            env.episode = np.append(env.episode,encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,cmd))
        else:
            cmd = 2
            env.rect_change_x = 0
            env.episode = np.append(env.episode,encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,cmd))
    #rect_x = np.random.randint(0,285)
    print('cmd = ',cmd)
    
    screen.fill(BLACK)
    env.rect_x += env.rect_change_x
    env.rect_y += env.rect_change_y
    if env.rect_x < 0:
        env.rect_x = 0
    if env.rect_x > 285:
        env.rect_x = 285
    
    env.ball_x += env.ball_change_x
    env.ball_y += env.ball_change_y
    # at this time we have old position and new position. let's record the episode
          
    #this handles the movement of the ball.
    if env.ball_x<0:
        env.ball_x=0
        env.ball_change_x = env.ball_change_x * -1
    elif env.ball_x>300-env.ball_size_x:
        env.ball_x=300-env.ball_size_x
        env.ball_change_x = env.ball_change_x * -1
    elif env.ball_y<0:
        env.ball_y=0
        env.ball_change_y = env.ball_change_y * -1
    elif env.ball_x>=env.rect_x and env.ball_x<=env.rect_x+90 and env.ball_y==env.rect_y-env.ball_size_y:
        env.ball_change_y = env.ball_change_y * -1
        env.score = env.score + 1
        reward = 1
        # We won, need to update Q
        env.numberofupdates = env.numberofupdates + 1
        
        print(env.episode)
        print('WIN!')
        num_games+=1
        for icnt in range(0,len(env.episode)):
            env.Q_up[int(env.episode[icnt])] = env.Q_up[int(env.episode[icnt])] + 1
            env.Q[int(env.episode[icnt])] = env.Q[int(env.episode[icnt])]+ (1/env.Q_up[int(env.episode[icnt])])*(reward - env.Q[int(env.episode[icnt])])
            
        env.episode = []
        num_wins += 1
        
        if np.mod(num_games,1000) == 0:
            file.write('%s,%s\n' % (str(num_games),str(num_wins)))
        
    elif env.ball_y>180: 
        env.ball_change_y = env.ball_change_y * -1
            
        if env.score > 0:
            env.score = env.score - 1 
        reward = -1
        print('Loss!')
        num_games+=1
        
        if np.mod(num_games,1000) == 0:
            file.write('%s,%s\n' % (str(num_games),str(num_wins)))
        # We lost, update the Q 
        env.numberofupdates = env.numberofupdates + 1 
        for icnt in range(0,len(env.episode)):    
            env.Q_up[int(env.episode[icnt])] = env.Q_up[int(env.episode[icnt])] + 1
            env.Q[int(env.episode[icnt])] = env.Q[int(env.episode[icnt])]+ (1/env.Q_up[int(env.episode[icnt])])*(reward - env.Q[int(env.episode[icnt])])
 
        env.episode = []                     
    pygame.draw.rect(screen,WHITE,[env.ball_x,env.ball_y,15,15])
    
    drawrect(screen,env.rect_x,env.rect_y)
        
   #score board
    font= pygame.font.SysFont('Times', 22,  True, False)
    text = font.render("Score : " + str(env.score), True, WHITE)
    screen.blit(text,[20,20])    
     
    pygame.display.flip()         
    clock.tick(1500)
    

pygame.quit()  
file.close()    
env.stats('stats.txt')  
