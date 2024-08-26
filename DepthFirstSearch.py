from constant import *
import time
import datetime
from Stack import *
from Board import *
import tracemalloc

class DepthFirstSearch:
    def __init__(self, board, gridSize):
        self.source = [2,2]
        self.board = Board(board,[0,0],self.source, gridSize=gridSize)
        self.path = []
        self.path.append([item[:] for item in self.board.board])
        self.fixPosition = self.board.findFixPosition()
        self.step = 0
        self.startTime = 0
        self.endTime = 0
        self.finalPath = []
        self.previousPosition = [-1,-1]
        self.stack = Stack()
        self.resultAfterSolved = 0
        self.memoryUsage = 0
    def resetAttributes(self):
        self.path = []
        self.fixPosition = []
        self.step = 0
        self.startTime = 0
        self.endTime = 0
        self.finalPath = []
        self.previousPosition = [-1,-1]
        self.memoryUsage = 0
        self.stack = Stack()


    def solveBoard(self, flag):
        self.resetAttributes()
        self.startTime = time.time()
        tracemalloc.start()
        self.result = self.traverseBoard()
        self.memoryUsage = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        self.endTime = time.time()
        self.calculateFinalPath()
        if flag == 1:
            self.printStatistics()
    
    def traverseBoard(self, root=[0,0]):
        
        if self.board.checkFinalState():
            return 1
        
        limit = len(self.board.board[1]) - 1

        self.stack.push(self.board.copy())

        while(not self.stack.isEmpty()):
            self.step += 1
            item = self.stack.pop()
            
            if self.previousPosition >= item.position:
                back = (limit+1)*(self.previousPosition[0] - item.position[0]) + (self.previousPosition[1] - item.position[1])
                for i in range(back+1):
                    self.path.pop()
            self.path.append([x[:] for x in item.board])
            if item.checkFinalState():
                return 1
            
            self.previousPosition = item.position
            if item.position[0] == item.position[1] and item.position[1] == limit:
                result, possibleMoveList = item.makeMove(item.position, self.fixPosition)
                if result == 0:
                    item.scanFromCurrentGrid(item.source)
                    if item.checkFinalState():
                        self.path.append(item)
                        return 1
                elif result == 1:
                    for i in possibleMoveList:
                        item.board[item.position[0]][item.position[1]] = i
                        item.scanFromCurrentGrid(item.source)
                        if item.checkFinalState():
                            self.path.append([x[:] for x in item.board])
                            return 1
        
            elif item.position[1] == limit:
                result, possibleMoveList = item.makeMove(item.position, self.fixPosition)

                if result == 0:
                    self.stack.push(item.copy(position=[item.position[0]+1, 0]))

                elif result == 1:
                    nextPosition = [item.position[0]+1, 0]
                    if self.generateNextChild(nextPosition, item, possibleMoveList):
                        return 1
                
            else:
                result, possibleMoveList = item.makeMove(item.position, self.fixPosition)

                if result == 0:
                    self.stack.push(item.copy(position=[item.position[0],item.position[1]+1]))

                elif result == 1:
                    nextPosition = [item.position[0],item.position[1]+1]
                    if self.generateNextChild(nextPosition, item, possibleMoveList):
                        return 1
        return 0

    def generateNextChild(self, nextPosition, item, possibleMoveList):
        for i in possibleMoveList:
            item.board[item.position[0]][item.position[1]] = i
            item.scanFromCurrentGrid(item.source)
            if item.checkFinalState():
                self.path.append([x[:] for x in item.board])
                return 1
            if not not nextPosition:
                self.stack.push(item.copy(position=nextPosition))
        return 0

    def printStatistics(self):
        data = [[self.result, self.step, len(self.finalPath)-1, self.memoryUsage, self.calculateExecutionTime()]]

        print("{:<25} {:<25} {:<15} {:<10}".format("Memory Usage (bytes)","Execution Time (hh:mm:ss)", "Traversed Node", "max stack"))
        print("-" * 100)
        print("{:<25} {:<25} {:<15} {:<10}".format(self.memoryUsage, self.calculateExecutionTime(), self.step, self.stack.max_stored_items))
        print("-" * 100)
        # self.printSolutionStep()

    def calculateFinalPath(self):
        for x in self.path:
            if x not in self.finalPath:
                self.finalPath.append(x)

    def printSolutionStep(self):
        finalPathLenght = len(self.finalPath)
        for i in range(finalPathLenght):
            print('Step {}:{}'.format(str(i).ljust(10), self.finalPath[i]))

    def calculateExecutionTime(self):
        execution_time = self.endTime - self.startTime
        execution_time_formatted = str(datetime.timedelta(seconds=execution_time))

        return execution_time_formatted
