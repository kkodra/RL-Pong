import numpy as np
import pygame 
from setup import setup

alpha = 0.7

# Color definition for printing
R  = '\033[1;31m' # red
G  = '\033[1;32m' # green
W  = '\033[0m'    # white (normal)

def encode(bx,by,bdir,padx,cmd):
    result = bx*2**12+by*2**8+bdir*2**6+padx*2**2+cmd
    if result>131072:
        print('Out of Bounds', result,  bx, by, bdir, padx, cmd)
    return int(result)

icount = 0
direction = np.array([[0,1],[2,3]])
    
BLACK = (0,0,0); WHITE = (255,255,255); GREEN = (0,255,0)

env = setup();

pygame.init()
fout = open('Logfile.txt','w')

screen = pygame.display.set_mode(env.size)
pygame.display.set_caption('Q Learning')

print('x ' + str(env.rect_x) + 'y '+ str(env.rect_y))

#Draws the paddle. Also restricts its movement between the edges
#of the window.
def drawrect(screen,x,y):
    if x <= 0:
        x = 0
    if x >= 210:
        x = 210    
    pygame.draw.rect(screen,GREEN,[x,y,90,15])
     
#Game's main loop    
done = False
clock = pygame.time.Clock()

r = np.array([-1, -100, 100])

num_games = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    # We need to pick left, right or stay randomly
    # We need to check if any of the three commands wins
    dirx = env.ball_change_x/15 
    diry = env.ball_change_y/15 
    print('dirx' , dirx , 'diry' , diry, 'ballx', env.ball_x, 'bally', env.ball_y, 'paddlex', env.rect_x)
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
    if env.Q[test1] > env.Q[test2] and env.Q[test1] > env.Q[test3] and env.Q[test1]>0:
        cmd = 0  # left
        env.rect_change_x = -15
        print(G+'***************** MOVE LEFT *****************' +W)
        print('test1 - max',env.Q[test1],'test2',env.Q[test2],'test3',env.Q[test3])
        env.episode = np.append(env.episode,encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,cmd))
        
        icount += 1
        print('icount = ', icount, 'length of episode', len(env.episode))
        if icount > 1:
            env.Q[int(env.episode[icount-2])] = env.Q[int(env.episode[icount-2])] + alpha*(r[0] + 0.99*env.Q[int(env.episode[icount-1])] - env.Q[int(env.episode[icount-2])])
        
    elif env.Q[test2] > env.Q[test1] and env.Q[test2] > env.Q[test3] and env.Q[test2]>0:
        cmd = 1  # right
        env.rect_change_x = 15
        print(G+'***************** MOVE RIGHT *****************'+W)
        print('test1',env.Q[test1],'test2 - max',env.Q[test2],'test3',env.Q[test3])
        env.episode = np.append(env.episode,encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,cmd))
        
        icount += 1
        print('icount = ', icount, 'length of episode', len(env.episode))
        if icount > 1:
            env.Q[int(env.episode[icount-2])] = env.Q[int(env.episode[icount-2])] + alpha*(r[0] + 0.99*env.Q[int(env.episode[icount-1])] - env.Q[int(env.episode[icount-2])])
        
    elif env.Q[test3] > env.Q[test1] and env.Q[test3] > env.Q[test2] and env.Q[test3]>0:
        cmd = 0 # no move
        env.rect_change_x = 0
        print(G+'***************** DO NOT MOVE *****************'+W)
        print('test1',env.Q[test1],'test2',env.Q[test2],'test3 - max',env.Q[test3])
        env.episode = np.append(env.episode,encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,cmd))
        
        icount += 1
        print('icount = ', icount, 'length of episode', len(env.episode))
        if icount > 1:
            env.Q[int(env.episode[icount-2])] = env.Q[int(env.episode[icount-2])] + alpha*(r[0] + 0.99*env.Q[int(env.episode[icount-1])] - env.Q[int(env.episode[icount-2])])
        
    else:
        print(R+'================= RANDOM MOVE ================='+W)
        rndnumber  = np.random.randint(0,100)
        if rndnumber< 35:
            # this will be left position
            cmd=0
            env.rect_change_x = -15
            env.episode = np.append(env.episode,encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,cmd))
            
            icount += 1
            print('icount = ', icount)
            if icount == 1:
                env.Q[int(env.episode[icount-1])] = r[0] 
            else:
                env.Q[int(env.episode[icount-2])] = env.Q[int(env.episode[icount-2])] + alpha*(r[0] + 0.99*env.Q[int(env.episode[icount-1])] - env.Q[int(env.episode[icount-2])])
            
        elif rndnumber <70:
            cmd = 1
            env.rect_change_x = +15
            env.episode = np.append(env.episode,encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,cmd))
            icount += 1
            print('icount = ', icount)
            if icount == 1:
                env.Q[int(env.episode[icount-1])] = r[0] 
            else:
                env.Q[int(env.episode[icount-2])] = env.Q[int(env.episode[icount-2])] + alpha*(r[0] + 0.99*env.Q[int(env.episode[icount-1])] - env.Q[int(env.episode[icount-2])])
            
        else:
            cmd = 2
            env.rect_change_x = 0
            env.episode = np.append(env.episode,encode(env.ball_x/15,env.ball_y/15,dirval,env.rect_x/15,cmd))
            
            icount += 1
            print('icount = ', icount)
            if icount == 1:
                env.Q[int(env.episode[icount-1])] = r[0] 
            else:
                env.Q[int(env.episode[icount-2])] = env.Q[int(env.episode[icount-2])] + alpha*(r[0] + 0.99*env.Q[int(env.episode[icount-1])] - env.Q[int(env.episode[icount-2])])
            
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
        
    # WE ARE UPDATING ALONG THE WAY 
    
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
    elif env.ball_x>=env.rect_x and env.ball_x <= env.rect_x+90 and env.ball_y == env.rect_y-env.ball_size_y:
        env.ball_change_y = env.ball_change_y * -1
        env.score = env.score + 1
        reward = 1
        # We won, need to update Q
        env.numberofupdates = env.numberofupdates + 1
        
        print(env.episode)
        print('WIN!')
        if num_games%1000 == 0:
            fout.write("%d, %d\n"%(num_games,env.score))
        num_games+=1
    
        env.Q[int(env.episode[icount-1])] = r[2] 

        icount = 0   
        env.episode = []
    elif env.ball_y>180: 
        env.ball_change_y = env.ball_change_y * -1
            
        if env.score > 0:
            env.score = env.score - 1 
        reward = -1
        print('Loss!')
        if num_games%1000 == 0:
            fout.write("%d, %d\n"% (num_games,env.score))
        num_games+=1
        # We lost, update the Q 
        env.numberofupdates = env.numberofupdates + 1 
        
        env.Q[int(env.episode[icount-1])] = r[1] 

        icount = 0
        env.episode = []                     
    pygame.draw.rect(screen,WHITE,[env.ball_x,env.ball_y,15,15])
    
    drawrect(screen,env.rect_x,env.rect_y)
    
    # Stop after certain number of iterations
    if num_games == 250000:
        break
        
    print('Number of games: ',num_games)
   #score board
    font= pygame.font.SysFont('Times', 22,  True, False)
    text = font.render("Score : " + str(env.score), True, WHITE)
    screen.blit(text,[20,20])    
     
    pygame.display.flip()         
    clock.tick(1500)
    
pygame.quit()    

