# cs221-2048RL

To run Expectimax on multiple boards, cd to the Expectimax folder and run game.py with flags:
  -d = Depth for Expectimax, default=2, type=int
  -b = Number of boards to play on, default=2, type=int
  -g = Number of full games to play, default=1, type=int
  -m = Which weighting strategy to use, default='simple', choices=('direness', 'simple', 'weighted', 'max'))
  -f = Use fill (1) or sampling (0) for Expectimax, default=1, type=int)
  -n = File name to use to store the data
  
All data used for graphs and tables are stored in Expectimax/data, and is stored in python3 picklized format.
data_visualizer.py can be (internally) modified to output the tables or graphs shown in the final report

