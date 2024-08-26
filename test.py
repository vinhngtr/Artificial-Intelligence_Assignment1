from Board import *
from DepthFirstSearch import *
import json
import os

gridSize = 0
searchAlgorithm = None
average = 0
exeTime = 0
testCase = []

def getTestCase():
    folder_path = "Test/"
    return [file for file in os.listdir(folder_path) if file.endswith(".txt")]

def getBoardata(selectedTestcase):
    with open("Test/" + selectedTestcase, 'r') as file:
        content = file.read()
    try:
        testcase_list = eval(content)
    except SyntaxError:
        testcase_list = json.loads(content)

    return testcase_list
testCase = getTestCase()
print("{:<20} {:<25} {:<25} {:<15} {:<10}".format("ID", "Memory Usage (bytes)","Execution Time", "Traversed Node", "max stack"))
print("-" * 100)
for case in testCase:
    board = getBoardata(case)
    gridSize = len(board[0])
    searchAlgorithm = DepthFirstSearch(board, gridSize)
    exeTime = 0
    average = 0
    step = 0
    for i in range(100):
        searchAlgorithm.solveBoard(0)
        step = searchAlgorithm.step
        mem = searchAlgorithm.memoryUsage
        exeTime += searchAlgorithm.endTime - searchAlgorithm.startTime
        average += mem
    print("{:<20} {:<25} {:<25} {:<15} {:<10}".format(case, average/100, exeTime/100, step, searchAlgorithm.stack.max_stored_items))
    print("-" * 100)