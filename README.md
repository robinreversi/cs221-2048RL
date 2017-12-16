# Artificial Intelligence Techniques for Playing Concurrent Games of 2048

Stanford CS 221: Artificial Intelligence -- Final Project

Alex Wang, Robin Cheong, Vince Ranganathan

Updated 12/15/17

----------------------------------------

To run Expectimax on multiple boards, cd to the Expectimax folder and run game.py with flags:  

  -d = Depth for Expectimax, default=2, type=int  

  -b = Number of boards to play on, default=2, type=int  

  -g = Number of full games to play, default=1, type=int  

  -m = Which weighting strategy to use, default='simple', choices=('direness', 'simple', 'weighted', 'max'))  

  -f = Use fill (1) or sampling (0) for Expectimax, default=1, type=int)  

  -n = File name to use to store the data  

  
All data used for graphs and tables are stored in Expectimax/data, and is stored in python3 picklized format.
data_visualizer.py can be (internally) modified to output the tables or graphs shown in the final report  

Run puzzle.py to see our code run on a GUI with 4 boards!  

gameutil.py stores all of our board manipulation logic
player.py stores all of the logic for the actual Expectimax algorithm  

Multi_Game_2048 stores all the files we used for playing multiple games of 2048 in an RL setting in OpenAI Gym's Format  

DQ_learning.py stores the code for Deep Q Learning -- run by calling the script in command line using python3   
