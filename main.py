
from runningPuzzle import PipesPuzzle
from pyGame import PuzzleInterface

if __name__ == "__main__":
  
  
  solve_choice = input("Su dung giai thuat A* with puzzple pipes (key 1):") 

  puzzle_pipes = PipesPuzzle()
  puzzle_pipes.solve(solve_choice)
  puzzle_interface = PuzzleInterface(puzzle_pipes)
  puzzle_interface.running()
  if len(puzzle_pipes.dataForPlot) != 0:
    t = input("Hien thi thong tin thong ke cho tim kiem ? (Y: Yes, other: No)")
    if t == 'Y' or t =='y':
      puzzle_pipes.simulatePlot()
 