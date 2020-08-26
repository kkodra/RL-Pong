#!/usr/bin/python
"""
Main script to run RL-Pong
User can choose between two algorithms: MC and Q
MC: Monte Carlo method
Q : Q-Learning
"""

# Select algorithm: 'MC' or 'Q'
algo = 'MC'

if algo == 'MC':
    import pong_MC
elif algo == 'Q':
    import pong_Q
else:
    raise Exception('Option not available.')
        

