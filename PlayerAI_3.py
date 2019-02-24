from random import randint
from BaseAI_3 import BaseAI
from Displayer_3 import Displayer
from Grid_3 import Grid

from decimal import Decimal
from copy import deepcopy
import time
import heapq
  
 
class PlayerAI(BaseAI):
    
    def getMove(self, grid):
        
        #moves = grid.getAvailableMoves() #get movable direction
        
        
        self.grid = grid     
        self.deep = 0  
        
        dumpChild, move, dumpScores = self.minixax()
        
        
        return move
        
        # return moves[randint(0, len(moves) - 1)] if moves else None
    
    def minixax(self):
        alpha = -1000000
        beta = 1000000
        
        child, move, scores = self.max(self.grid, alpha, beta)

        return child, move, scores
    
    def min(self, grid, alpha, beta):
                
        self.deep = self.deep + 1
        
        if (self.deep == 3):
            dumpChild = -1
            dumpMove = -1
            scores = self.heuristic(grid)
            self.deep = self.deep - 1
            return dumpChild, dumpMove, scores
        
        minChild = None
        minChildMove = None
        minScores = 1000000
        
        childrenMap = []
        computerPossibleMoves = grid.getAvailableCells()
        
        x = 0
        for i in computerPossibleMoves:
            copyGrid_2 = deepcopy(grid)
            copyGrid_2.setCellValue(i, 2)
            childrenMap.append(copyGrid_2)
            
            x = x + 1
            
            copyGrid_4 = deepcopy(grid)
            copyGrid_4.setCellValue(i, 4)
            childrenMap.append(copyGrid_4)
            
            x = x + 1
        
        for child in childrenMap:
            dumpChild, dumpMove, scores = self.max(child, alpha, beta)
            
            if scores < minScores:
                minChild = child
                minScores = scores
            
            if (minScores <= alpha):
                break
            
            if (minScores < beta):
                beta = minScores
        
        self.deep = self.deep - 1
        
        return minChild, minChildMove, minScores
    
    def max(self, grid, alpha, beta):
        
        self.deep = self.deep + 1
        
        if (self.deep == 3):
            self.deep  = self.deep  - 1
            dumpChild = -1
            dumpMove = -1
            scores = self.heuristic(grid)
            return dumpChild, dumpMove, scores
               
        maxChild = None
        maxChildMove = None
        MaxScores = -1000000
        
        childrenMap = []
        childrenMoveList = grid.getAvailableMoves()
        #print ("moves list =" + str(childrenMoveList))
        
        for i in childrenMoveList:
            copyGrid = deepcopy(grid)
            copyGrid.move(i)
            childrenMap.append(copyGrid)
        
        i = 0
        for child in childrenMap:
            dumpChild, dumpMove, scores = self.min(child, alpha, beta)
            
            if scores > MaxScores:
                maxChild = child
                maxChildMove = childrenMoveList[i]
                MaxScores = scores
            
            if (MaxScores >= beta):
                break
            
            if (MaxScores > alpha):
                alpha = MaxScores
            
            i = i + 1
        
        self.deep = self.deep - 1
        
        return maxChild, maxChildMove, MaxScores
    
    def heuristic(self, grid):
        
        '''
        monotonicityWeight = 10
        maxtilePositionWeight = 1000
        AvailableCeilsWeight = 10
        #contiuniousValuesWeight = 10
        
        scores = 0
        
        scores = scores + monotonicityWeight * self.checkMonotonicity(grid)
        scores = scores + maxtilePositionWeight * self.checkMaxTilePosition(grid)
        scores = scores + AvailableCeilsWeight * self.checkAvailableCells(grid)
        '''
        
        scores = 0
        
        monoW = 10
        availableCellsW = 1
        smoothW = 100
        scoresW = 0
        
        
        scores = scores + monoW * self.checkMono(grid)
        scores = scores + availableCellsW * self.checkAvailableCells(grid)
        scores = scores + smoothW * self.checkSsmooth(grid)
        scores = scores + scoresW * self.checkScores(grid)
        
        return scores
    
    def checkMonotonicity(self, grid):
        sameValueScores = 2
        greaterValueScores = 2
        result = 0
        
        transposeMap = zip(*(grid.map))
        
        for i in grid.map:
            for x in range(len(i) - 1):
                if (x < 3):
                #if i[x+1] != 0:
                    if (i[x+1] == i[x]):
                        result = result + sameValueScores
                        #print ("row sameValueScores get!, row = " + str(i) + " value 0  = " + str(i[x]) + " value 1 = " + str(i[x+1]))
                    elif (i[x+1] > i[x]):
                        #result = result + greaterValueScores
                        result = result
                    else:
                        result = result -1
                        #print ("row greaterValueScores get!, row = " + str(i) + " value 0  = " + str(i[x]) + " value 1 = " + str(i[x+1]))
        
        for i in transposeMap:
            for x in range(len(i) - 1):
                if (x < 3):
                #if i[x+1] != 0:
                    if (i[x+1] == i[x]):
                        result = result + sameValueScores
                        #print ("column sameValueScores get!, row = " + str(i) + " value 0  = " + str(i[x]) + " value 1 = " + str(i[x+1]))
                    elif (i[x+1] < i[x]):
                        #result = result + greaterValueScores
                        result = result
                    else:
                        result = result - 1
                        #print ("column greaterValueScores get!, row = " + str(i) + "value 0  = " + str(i[x]) + " value 1 = " + str(i[x+1]))
        
        return result

    def checkMaxTilePosition(self, grid):
        result = 0
        scores = 1
        
        copyGrid = deepcopy(grid)
        
        maxtile = copyGrid.getMaxTile()
        
        if copyGrid.map[0][3] == maxtile:
            result = result + scores
            
            copyGrid.map[0][3] = 0
            
            maxtile2 = copyGrid.getMaxTile()
            
            if (copyGrid.map[0][2] == maxtile2) or (copyGrid.map[2][3] == maxtile2):
                result = result + scores * 2
        
        return result

    def checkAvailableCells(self, grid):
        availableCells = grid.getAvailableCells()
        
        
        return len(availableCells) * 1
    
    def checkContiuniousValues(self, grid):
        result = 0
        scores = 10
        
        if (grid.map[0][0] > grid.map[0][1]) and (grid.map[0][1] > grid.map[0][2]) and (grid.map[0][2] > grid.map[0][3]):
            result = result + scores 
            
        return result

    def checkMono(self, grid):
        result = 0
        scores = 1
        '''
        maxTile = grid.getMaxTile()
        
        if grid.map[0][0] >= grid.map[0][1] and grid.map[0][1] >= grid.map[0][2] and grid.map[0][2] >= grid.map[0][3]:
            result = result + scores
        
        if grid.map[1][0] >= grid.map[1][1] and grid.map[1][1] >= grid.map[1][2] and grid.map[1][2] >= grid.map[1][3]:
            result = result + scores
            
        if grid.map[2][0] >= grid.map[2][1] and grid.map[2][1] >= grid.map[2][2] and grid.map[2][2] >= grid.map[2][3]:
            result = result + scores
            
        if grid.map[3][0] >= grid.map[3][1] and grid.map[3][1] >= grid.map[3][2] and grid.map[3][2] >= grid.map[3][3]:
            result = result + scores
            
        if grid.map[0][0] >= grid.map[1][0] and grid.map[1][0] >= grid.map[2][0] and grid.map[2][0] >= grid.map[3][0]:
            result = result + scores
        
        if grid.map[0][1] >= grid.map[1][1] and grid.map[1][1] >= grid.map[2][1] and grid.map[2][1] >= grid.map[3][1]:
            result = result + scores
            
        if grid.map[0][2] >= grid.map[1][2] and grid.map[1][2] >= grid.map[2][2] and grid.map[2][2] >= grid.map[3][2]:
            result = result + scores
        
        if grid.map[0][3] >= grid.map[1][3] and grid.map[1][3] >= grid.map[2][3] and grid.map[2][3] >= grid.map[3][3]:
            result = result + scores
        '''
        
        if grid.map[0][0] > grid.map[0][1] and grid.map[0][1] > grid.map[0][2] and grid.map[0][2] > grid.map[0][3]:
            result = result + scores
        
        if grid.map[1][0] > grid.map[1][1] and grid.map[1][1] > grid.map[1][2] and grid.map[1][2] > grid.map[1][3]:
            result = result + scores
            
        if grid.map[2][0] > grid.map[2][1] and grid.map[2][1] > grid.map[2][2] and grid.map[2][2] > grid.map[2][3]:
            result = result + scores
            
        if grid.map[3][0] > grid.map[3][1] and grid.map[3][1] > grid.map[3][2] and grid.map[3][2] > grid.map[3][3]:
            result = result + scores
            
        if grid.map[0][0] > grid.map[1][0] and grid.map[1][0] > grid.map[2][0] and grid.map[2][0] > grid.map[3][0]:
            result = result + scores
        
        if grid.map[0][1] > grid.map[1][1] and grid.map[1][1] > grid.map[2][1] and grid.map[2][1] > grid.map[3][1]:
            result = result + scores
            
        if grid.map[0][2] > grid.map[1][2] and grid.map[1][2] > grid.map[2][2] and grid.map[2][2] > grid.map[3][2]:
            result = result + scores
        
        if grid.map[0][3] > grid.map[1][3] and grid.map[1][3] > grid.map[2][3] and grid.map[2][3] > grid.map[3][3]:
            result = result + scores
        
        return result

    def checkMaxTile(self, grid):
        result = 0
        scores = 10
        
        maxtile = grid.getMaxTile()
        
        if (grid.map[0][0] == maxtile):
            result = result + scores
            
        return result
    
    def checkSsmooth(self, grid):
        result = 0
        scores = 1
        
        for i in range(4):
            if grid.map[i][0] != 0 and grid.map[i][0] == grid.map[i][1]:
                result = result + scores
                
            if grid.map[i][0] != 0 and grid.map[i][1] == grid.map[i][2]:
                result = result + scores
                
            if grid.map[i][0] != 0 and grid.map[i][2] == grid.map[i][3]:
                result = result + scores
        
        for i in range(4):
            if grid.map[0][i] != 0 and grid.map[0][i] == grid.map[1][i]:
                result = result + scores
                
            if grid.map[0][i] != 0 and grid.map[1][i] == grid.map[2][i]:
                result = result + scores
            
            if grid.map[0][i] != 0 and grid.map[2][i] == grid.map[3][i]:
                result = result + scores
    
        return result
    def checkScores(self, grid):
        result = 1
        
        for i in grid.map:
            for j in i:
                    result = result + j * j
        
        return result