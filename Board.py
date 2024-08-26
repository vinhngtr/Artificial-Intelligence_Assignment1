from constant import *

class Board:
    def __init__(self, board, position, root, gridSize):
        self.board = [item[:] for item in board]
        self.position = [x for x in position]
        self.source = root
        self.gridSize = gridSize
        self.scanFromCurrentGrid(self.source)

    def copy(self, board=[], position=[], root=[]):
        # t_board = [item[:] for item in self.board] if not board else [item[:] for item in board]
        t_board = self.board if not board else board
        t_position = [x for x in self.position] if not position else [x for x in position]
        t_root = [y for y in self.source] if not root else [y for y in root]
        
        return Board(t_board, t_position, t_root, self.gridSize)
    
    def findFixPosition(self):
        fixPosition = []
        if abs(self.board[0][0]) >= UL and abs(self.board[0][0]) <= DL:
            self.board[0][0] = DR
            fixPosition.append([0,0])

        if abs(self.board[0][self.gridSize-1]) >= UL and abs(self.board[0][self.gridSize-1]) <= DL:
            self.board[0][self.gridSize-1] = DL
            fixPosition.append([0,self.gridSize-1])  

        if abs(self.board[self.gridSize-1][0]) >= UL and abs(self.board[self.gridSize-1][0]) <= DL:
            self.board[self.gridSize-1][0] = UR
            fixPosition.append([self.gridSize-1,0])

        if abs(self.board[self.gridSize-1][self.gridSize-1]) >= UL and abs(self.board[self.gridSize-1][self.gridSize-1]) <= DL:
            self.board[self.gridSize-1][self.gridSize-1] = UL
            fixPosition.append([self.gridSize-1,self.gridSize-1])

        for i in range(1,self.gridSize):
            # first row
            if abs(self.board[0][ i]) == H or abs(self.board[0][ i]) == V:
                self.board[0][i] = H
                fixPosition.append([0,i])

            elif abs(self.board[0][ i]) >= TU and abs(self.board[0][ i]) <= TL:
                self.board[0][i] = TD
                fixPosition.append([0,i])
            # last row
            if abs(self.board[self.gridSize-1][ i]) == H or abs(self.board[self.gridSize-1][ i]) == V:
                self.board[self.gridSize-1][i] = H
                fixPosition.append([self.gridSize-1,i])

            elif abs(self.board[self.gridSize-1][ i]) >= TU and abs(self.board[self.gridSize-1][ i]) <= TL:
                self.board[self.gridSize-1][i] = TU
                fixPosition.append([self.gridSize-1,i])
            # first column
            if abs(self.board[i][ 0]) == H or abs(self.board[i][ 0]) == V:
                self.board[i][0] = V
                fixPosition.append([i, 0])

            elif abs(self.board[i][ 0]) >= TU and abs(self.board[i][ 0]) <= TL:
                self.board[i][0] = TR
                fixPosition.append([i,0])
            # last column
            if abs(self.board[i][self.gridSize-1]) == H or abs(self.board[i][self.gridSize-1]) == V:
                self.board[i][self.gridSize-1] = V
                fixPosition.append([i,self.gridSize-1])

            elif abs(self.board[i][self.gridSize-1]) >= TU and abs(self.board[i][self.gridSize-1]) <= TL:
                self.board[i][self.gridSize-1] = TL
                fixPosition.append([i,self.gridSize-1])
        self.scanFromCurrentGrid(self.source)
        return fixPosition
            

    def isUpConnect(self, refGrid):
        if refGrid[0] - 1 < 0:return 0
        targetGrid = [refGrid[0] - 1, refGrid[1]]
        grid = abs(self.board[targetGrid[0]][targetGrid[1]])
        if ((grid==DL)|(grid==DR)|(grid==V)|(grid==TL)|(grid==TR)|(grid==TD)|(grid==ED)):
            return 1
        return 0
    def isLeftConnect(self, refGrid):
        if refGrid[1] - 1 < 0:
            return 0
        targetGrid = [refGrid[0], refGrid[1] - 1]
        grid = abs(self.board[targetGrid[0]][targetGrid[1]])
        if ((grid==UR)|(grid==DR)|(grid==H)|(grid==TR)|(grid==TU)|(grid==TD)|(grid==ER)):
            return 1
        return 0

    def isRightConnect(self, refGrid):
        if refGrid[1] + 1 >= self.gridSize:
            return 0
        targetGrid = [refGrid[0], refGrid[1] + 1]
        grid = abs(self.board[targetGrid[0]][targetGrid[1]])
        if ((grid==UL)|(grid==DL)|(grid==H)|(grid==TL)|(grid==TU)|(grid==TD)|(grid==EL)):
            return 1
        return 0
    def isDownConnect(self, refGrid):
        if refGrid[0] + 1 >= self.gridSize:
            return 0
        targetGrid = [refGrid[0] + 1, refGrid[1]]
        grid = abs(self.board[targetGrid[0]][targetGrid[1]])
        if ((grid==UR)|(grid==UL)|(grid==V)|(grid==TR)|(grid==TU)|(grid==TL)|(grid==EU)):
            return 1
        return 0
        
    def scanLeft(self, root):
        if root[1] > 0: # left
            if self.isLeftConnect(root):
                if self.board[root[0]][root[1]] < 0 and self.board[root[0]][root[1]-1] > 0:
                    self.board[root[0]][root[1]-1] = (-1) * self.board[root[0]][root[1]-1]
                    #TODO: add to path
                    self.startScan([root[0], root[1]-1])
    def scanUp(self, root):
        if root[0] > 0: # up
            if self.isUpConnect(root):
                if self.board[root[0]][root[1]] < 0 and self.board[root[0]-1][root[1]] > 0:
                    self.board[root[0]-1][root[1]] = (-1) * self.board[root[0]-1][root[1]]
                    #TODO: add to path
                    self.startScan([root[0]-1, root[1]])
    def scanDown(self, root):
        if root[0] < self.gridSize - 1: # down
            if self.isDownConnect(root):
                if self.board[root[0]][root[1]] < 0 and self.board[root[0]+1][root[1]] > 0:
                    self.board[root[0]+1][root[1]] = (-1) * self.board[root[0]+1][root[1]]
                    #TODO: add to path
                    self.startScan([root[0]+1, root[1]])
    def scanRight(self, root):
        if root[1] < self.gridSize - 1: # right
            if self.isRightConnect(root):
                if self.board[root[0]][root[1]] < 0 and self.board[root[0]][root[1]+1] > 0:
                    self.board[root[0]][root[1]+1] = (-1) * self.board[root[0]][root[1]+1]
                    #TODO: add to path
                    self.startScan([root[0], root[1]+1])
    
    def setToPositive(self):
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if [i,j] != self.source:
                    self.board[i][j] = abs(self.board[i][j])
                else:
                    self.board[i][j] = (-1) * abs(self.board[i][j])

    def scanFromCurrentGrid(self, root):
        self.setToPositive()
        self.startScan(root)

    def startScan(self, root):
        
        if self.board[root[0]][root[1]] == CH:
            self.scanLeft(root)
            self.scanRight(root)

        elif self.board[root[0]][root[1]] == CV:
            self.scanUp(root)
            self.scanDown(root)
    
        elif self.board[root[0]][root[1]] == CUL:
            self.scanUp(root)
            self.scanLeft(root)

        elif self.board[root[0]][root[1]] == CUR:
            self.scanUp(root)
            self.scanRight(root)

        elif self.board[root[0]][root[1]] == CDR:
            self.scanDown(root)
            self.scanRight(root)

        elif self.board[root[0]][root[1]] == CDL:
            self.scanDown(root)
            self.scanLeft(root)

        elif self.board[root[0]][root[1]] == CTU:
            self.scanUp(root)
            self.scanLeft(root)
            self.scanRight(root)

        elif self.board[root[0]][root[1]] == CTD:
            self.scanDown(root)
            self.scanLeft(root)
            self.scanRight(root)

        elif self.board[root[0]][root[1]] == CTR:
            self.scanUp(root)
            self.scanDown(root)
            self.scanRight(root)

        elif self.board[root[0]][root[1]] == CTL:
            self.scanUp(root)
            self.scanDown(root)
            self.scanLeft(root)

        return 1
    def checkConnect(self, root):
        if self.board[root[0]][root[1]] == CH:
            return self.isLeftConnect(root) and self.isRightConnect(root)

        elif self.board[root[0]][root[1]] == CV:
            return self.isUpConnect(root) and self.isDownConnect(root)
    
        elif self.board[root[0]][root[1]] == CUL:
            return self.isUpConnect(root) and self.isLeftConnect(root)

        elif self.board[root[0]][root[1]] == CUR:
            return self.isUpConnect(root) and self.isRightConnect(root)

        elif self.board[root[0]][root[1]] == CDR:
            return self.isDownConnect(root) and self.isRightConnect(root)

        elif self.board[root[0]][root[1]] == CDL:
            return self.isDownConnect(root) and self.isLeftConnect(root)

        elif self.board[root[0]][root[1]] == CTU:
            return self.isUpConnect(root) and self.isLeftConnect(root) and self.isRightConnect(root)

        elif self.board[root[0]][root[1]] == CTD:
            return self.isDownConnect(root) and self.isLeftConnect(root) and self.isRightConnect(root)

        elif self.board[root[0]][root[1]] == CTR:
            return self.isUpConnect(root) and self.isDownConnect(root) and self.isRightConnect(root)

        elif self.board[root[0]][root[1]] == CTL:
            return self.isUpConnect(root) and self.isDownConnect(root) and self.isLeftConnect(root)
        elif self.board[root[0]][root[1]] > 0: 
            return False
        return True
    def checkFinalState(self):
        length = len(self.board[0])
        for i in range(length):
            for j in range(length):
                if not self.checkConnect([i,j]):
                    return 0
        return 1

    def makeMove(self, root, fixPosition):
        possibleMove = []
        if root in fixPosition:
            return 0, possibleMove
        elif (
            self.board[root[0]][root[1]] == EU or self.board[root[0]][root[1]] == CEU or
            self.board[root[0]][root[1]] == CER or self.board[root[0]][root[1]] == ER or
            self.board[root[0]][root[1]] == CED or self.board[root[0]][root[1]] == ED or
            self.board[root[0]][root[1]] == CEL or self.board[root[0]][root[1]] == EL
        ):
            if self.isUpConnect(root) and self.isLeftConnect(root):
                return -1, possibleMove
            elif self.isUpConnect(root): 
                possibleMove.append(EU)
            elif self.isLeftConnect(root): 
                possibleMove.append(EL)
            else:
                possibleMove.append(ED)
                possibleMove.append(ER)

        elif (
            self.board[root[0]][root[1]] == CH or self.board[root[0]][root[1]] == H or
            self.board[root[0]][root[1]] == CV or self.board[root[0]][root[1]] == V
        ):
            if self.isUpConnect(root) and self.isLeftConnect(root):
                return -1, possibleMove
            elif self.isUpConnect(root):
                possibleMove.append(V)
            elif self.isLeftConnect(root):
                possibleMove.append(H)

    
        elif (
            self.board[root[0]][root[1]] == CUL or self.board[root[0]][root[1]] == UL or
            self.board[root[0]][root[1]] == CUR or self.board[root[0]][root[1]] == UR or
            self.board[root[0]][root[1]] == CDR or self.board[root[0]][root[1]] == DR or
            self.board[root[0]][root[1]] == CDL or self.board[root[0]][root[1]] == DL
        ):
            # print("UL --> UR")
            if self.isUpConnect(root) and self.isLeftConnect(root):
                possibleMove.append(UL)
            elif not self.isUpConnect(root) and self.isLeftConnect(root):
                possibleMove.append(DL)
            elif self.isUpConnect(root) and not self.isLeftConnect(root):
                possibleMove.append(UR)
            else:
                possibleMove.append(DR)

        elif (
            self.board[root[0]][root[1]] == CTU or self.board[root[0]][root[1]] == TU or
            self.board[root[0]][root[1]] == CTD or self.board[root[0]][root[1]] == TD or
            self.board[root[0]][root[1]] == CTR or self.board[root[0]][root[1]] == TR or
            self.board[root[0]][root[1]] == CTL or self.board[root[0]][root[1]] == TL
        ):
            if self.isUpConnect(root) and self.isLeftConnect(root):
                possibleMove.append(TU)
                possibleMove.append(TL)
            elif not self.isUpConnect(root) and self.isLeftConnect(root):
                possibleMove.append(TD)
            elif self.isUpConnect(root) and not self.isLeftConnect(root):
                possibleMove.append(TR)
            else: 
                return -1, possibleMove
            
        return 1, possibleMove

