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

Q = np.zeros([131072])

episode = []
icount = 0
direction = np.array([[0,1],[2,3]])
    
BLACK = (0,0,0); WHITE = (255,255,255); GREEN = (0,255,0)

env = setup();

pygame.init()
fout = open('Logfile.txt','w')

#Initializing the display window
size = (300,210)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Q Learning')

#Starting coordinates of the paddle
rect_x = int(np.random.randint(0,285)/15)*15
rect_y = 195
print('x ' + str(rect_x) + 'y '+ str(rect_y))

#initial speed of the paddle
rect_change_x = 0
rect_change_y = 0

#initial position of the ball
ball_x = int(np.random.randint(0,285)/15)*15 #0
ball_y = 0
print('x ' + str(ball_x) + 'y '+ str(ball_y))
#speed of the ball
ball_change_x = 15
ball_change_y = 15

# Define ball size
ball_size_x = 15
ball_size_y = 15

score = 0
numberofupdates = 0

#draws the paddle. Also restricts its movement between the edges
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
    dirx = ball_change_x/15 
    diry = ball_change_y/15 
    print('dirx' , dirx , 'diry' , diry, 'ballx', ball_x, 'bally', ball_y, 'paddlex', rect_x)
    if dirx == -1:
        dirx = 0
    else:
        dirx = 1
    if diry == -1:
        diry = 0
    else:
        diry = 1
    
    dirval = direction[dirx,diry]
    test1 = encode(ball_x/15,ball_y/15,dirval,rect_x/15,0)
    test2 = encode(ball_x/15,ball_y/15,dirval,rect_x/15,1)
    test3 = encode(ball_x/15,ball_y/15,dirval,rect_x/15,2)
    if Q[test1] > Q[test2] and Q[test1] > Q[test3] and Q[test1]>0:
        cmd = 0  # left
        rect_change_x = -15
        print(G+'***************** MOVE LEFT *****************' +W)
        print('test1 - max',Q[test1],'test2',Q[test2],'test3',Q[test3])
        episode = np.append(episode,encode(ball_x/15,ball_y/15,dirval,rect_x/15,cmd))
        
        icount += 1
        print('icount = ', icount, 'length of episode', len(episode))
        if icount > 1:
            Q[int(episode[icount-2])] = Q[int(episode[icount-2])] + alpha*(r[0] + 0.99*Q[int(episode[icount-1])] - Q[int(episode[icount-2])])
        
    elif Q[test2] > Q[test1] and Q[test2] > Q[test3] and Q[test2]>0:
        cmd = 1  # right
        rect_change_x = 15
        print(G+'***************** MOVE RIGHT *****************'+W)
        print('test1',Q[test1],'test2 - max',Q[test2],'test3',Q[test3])
        episode = np.append(episode,encode(ball_x/15,ball_y/15,dirval,rect_x/15,cmd))
        
        icount += 1
        print('icount = ', icount, 'length of episode', len(episode))
        if icount > 1:
            Q[int(episode[icount-2])] = Q[int(episode[icount-2])] + alpha*(r[0] + 0.99*Q[int(episode[icount-1])] - Q[int(episode[icount-2])])
        
    elif Q[test3] > Q[test1] and Q[test3] >Q[test2] and Q[test3]>0:
        cmd = 0 # no move
        rect_change_x = 0
        print(G+'***************** DO NOT MOVE *****************'+W)
        print('test1',Q[test1],'test2',Q[test2],'test3 - max',Q[test3])
        episode = np.append(episode,encode(ball_x/15,ball_y/15,dirval,rect_x/15,cmd))
        
        icount += 1
        print('icount = ', icount, 'length of episode', len(episode))
        if icount > 1:
            Q[int(episode[icount-2])] = Q[int(episode[icount-2])] + alpha*(r[0] + 0.99*Q[int(episode[icount-1])] - Q[int(episode[icount-2])])
        
    else:
        print(R+'================= RANDOM MOVE ================='+W)
        rndnumber  = np.random.randint(0,100)
        if rndnumber< 35:
            # this will be left position
            cmd=0
            rect_change_x = -15
            episode = np.append(episode,encode(ball_x/15,ball_y/15,dirval,rect_x/15,cmd))
            
            icount += 1
            print('icount = ', icount)
            if icount == 1:
                Q[int(episode[icount-1])] = r[0] 
            else:
                Q[int(episode[icount-2])] = Q[int(episode[icount-2])] + alpha*(r[0] + 0.99*Q[int(episode[icount-1])] - Q[int(episode[icount-2])])
            
        elif rndnumber <70:
            cmd = 1
            rect_change_x = +15
            episode = np.append(episode,encode(ball_x/15,ball_y/15,dirval,rect_x/15,cmd))
            icount += 1
            print('icount = ', icount)
            if icount == 1:
                Q[int(episode[icount-1])] = r[0] 
            else:
                Q[int(episode[icount-2])] = Q[int(episode[icount-2])] + alpha*(r[0] + 0.99*Q[int(episode[icount-1])] - Q[int(episode[icount-2])])
            
        else:
            cmd = 2
            rect_change_x = 0
            episode = np.append(episode,encode(ball_x/15,ball_y/15,dirval,rect_x/15,cmd))
            
            icount += 1
            print('icount = ', icount)
            if icount == 1:
                Q[int(episode[icount-1])] = r[0] 
            else:
                Q[int(episode[icount-2])] = Q[int(episode[icount-2])] + alpha*(r[0] + 0.99*Q[int(episode[icount-1])] - Q[int(episode[icount-2])])
            
    #rect_x = np.random.randint(0,285)
    print('cmd = ',cmd)
    
    screen.fill(BLACK)
    rect_x += rect_change_x
    rect_y += rect_change_y
    if rect_x < 0:
        rect_x = 0
    if rect_x > 285:
        rect_x = 285
    
    ball_x += ball_change_x
    ball_y += ball_change_y
    # at this time we have old position and new position. let's record the episode
        
    # WE ARE UPDATING ALONG THE WAY 
    
    #this handles the movement of the ball.
    if ball_x<0:
        ball_x=0
        ball_change_x = ball_change_x * -1
    elif ball_x>300-ball_size_x:
        ball_x=300-ball_size_x
        ball_change_x = ball_change_x * -1
    elif ball_y<0:
        ball_y=0
        ball_change_y = ball_change_y * -1
    elif ball_x>=rect_x and ball_x<=rect_x+90 and ball_y==rect_y-ball_size_y:
        ball_change_y = ball_change_y * -1
        score = score + 1
        reward = 1
        # We won, need to update Q
        numberofupdates = numberofupdates + 1
        
        print(episode)
        print('WIN!')
        if num_games%1000 == 0:
            fout.write("%d, %d\n"%(num_games,score))
        num_games+=1
    
        Q[int(episode[icount-1])] = r[2] 

        icount = 0   
        episode = []
    elif ball_y>180: 
        ball_change_y = ball_change_y * -1
            
        if score > 0:
            score = score - 1 
        reward = -1
        print('Loss!')
        if num_games%1000 == 0:
            fout.write("%d, %d\n"% (num_games,score))
        num_games+=1
        # We lost, update the Q 
        numberofupdates = numberofupdates + 1 
        
        Q[int(episode[icount-1])] = r[1] 

        icount = 0
        episode = []                     
    pygame.draw.rect(screen,WHITE,[ball_x,ball_y,15,15])
    
    drawrect(screen,rect_x,rect_y)
    
    # Stop after certain number of iterations
    if num_games == 250000:
        break
        
    print('Number of games: ',num_games)
   #score board
    font= pygame.font.SysFont('Times', 22,  True, False)
    text = font.render("Score : " + str(score), True, WHITE)
    screen.blit(text,[20,20])    
     
    pygame.display.flip()         
    clock.tick(1500)
    
pygame.quit()    

