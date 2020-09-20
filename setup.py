import numpy as np
import matplotlib.pyplot as plt

class setup():
    def __init__(self):
        self.Q = np.zeros([131072])
        self.Q_up = np.zeros([131072])
        
        self.episode = []
        self.direction = np.array([[0,1],[2,3]])
                           
        #Initializing the display window
        self.size = (300,210)
        
        #Starting coordinates of the paddle
        self.rect_x = int(np.random.randint(0,285)/15)*15
        self.rect_y = 195
        print('x ' + str(self.rect_x) + 'y '+ str(self.rect_y))
        #initial speed of the paddle
        self.rect_change_x = 0
        self.rect_change_y = 0
        
        #initial position of the ball
        self.ball_x = int(np.random.randint(0,285)/15)*15 #0
        self.ball_y = 0
        print('x ' + str(self.ball_x) + 'y '+ str(self.ball_y))
        #speed of the ball
        self.ball_change_x = 15
        self.ball_change_y = 15
        
        # Define ball size
        self.ball_size_x = 15
        self.ball_size_y = 15
        
        self.score = 0
        self.numberofupdates = 0
        
    # Read number of episodes and wins and plot statistics
    def stats(self,file_name):
        file = open(file_name, 'r')
        episodes = []
        wins = []
        
        for line in file.readlines():
            fname = line.rstrip().split(',') #using rstrip to remove the \n
            episodes.append(int(fname[0]))
            wins.append(int(fname[1]))
        
        res = [i / j for i, j in zip(wins[1:], episodes[1:])]
        plt.figure()
        plt.plot(episodes,wins,'o')
        plt.xlabel('Number of Episodes')
        plt.ylabel('Number of Wins')
        plt.grid()
        
        plt.figure()
        plt.plot(episodes[1:],res)
        plt.xlabel('Number of Episodes')
        plt.ylabel('Accuracy [%]')
        plt.grid()