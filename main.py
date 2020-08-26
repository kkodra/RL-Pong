"""
Main script to run RL-Pong
User can choose between two algorithms: MC and Q
MC: Monte Carlo method
Q : Q-Learning
"""

import pong_Q
import pong_MC

# Select algorithm: 'MC' or 'Q'
algo = 'MC'

if algo == 'MC':
    pong_MC
elif algo == 'Q':
    pong_Q
else:
    raise Exception('Option not available.')
    

        

