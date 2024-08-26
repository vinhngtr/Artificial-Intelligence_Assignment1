from constant import *
from Board import *


class Stack():
    def __init__(self):
        self.items = []
        self.size = 0
        self.max_stored_items = 0

    def printStack(self):
        print("start print stack")
        for i in self.items:
            print(f"Position: {i.position} \t board: {i.board}")
        print("end print stack")

    def push(self, item):
            
        self.size = self.size + 1

        if self.size > self.max_stored_items:
            self.max_stored_items = self.size
        self.items.append(item)
    
    def pop(self) -> Board:
        if not self.isEmpty():
            self.size = self.size - 1
            return self.items.pop()
        else:
            raise IndexError("Empty stack!")
    
    def isEmpty(self):
        return 1 if self.size == 0  else 0
    
    def size(self):
        return self.size
    

