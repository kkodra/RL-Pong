# RL-Pong

## Overview
Implementation of RL algorithm to the classic single-player pong game.

Episode: Ends whenever the ball hits the paddle or the ground
State-space: Product of all possible locations of the ball, all possible moves of the paddle, all possible directions of the ball.
Environment is 14 x 20 units where one unit is the size of the ball. Pygame has been used to code the environment. Developed in collaboration with N. Beser.

* Monte Carlo (MC)
	* Learning is noticeable in about 5 minutes (tested on a Intel CORE i7, 16 GB. Can vary based on system.)
* Temporal difference (Q-Learning)
	* Learning is slower that MC. Takes about twice as long (compared to MC) to notice learning.
\* To be added \*

## How to Run
Simply run _pong_MC.py_. The following libraries are needed:
1. pygame
2. numpy
3. matplotlib
