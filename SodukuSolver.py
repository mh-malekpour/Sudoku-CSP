from time import time
import copy

class SodukuSolver:
    def __init__(self,dim,fileDir):
        self.dim = dim
        self.expandedNodes = 0
        with open(fileDir) as f:
	        content = f.readlines()
	        self.board = [list(x.strip()) for x in content]
        self.rv = self.getRemainingValues()


    def getDomain(self,row,col):
        RVCell = [str(i) for i in range(1 ,self.dim + 1)]
        for i in range(self.dim):
            if self.board[row][i] != '0':
                if self.board[row][i] in RVCell:
                    RVCell.remove(self.board[row][i])

        for i in range(self.dim):
            if self.board[i][col] != '0':
                if self.board[i][col] in RVCell:
                    RVCell.remove(self.board[i][col])

        boxRow = row - row%3
        boxCol = col - col%3
        for i in range(3):
            for j in range(3):
                if self.board[boxRow+i][boxCol+j]!=0:
                    if self.board[boxRow+i][boxCol+j] in RVCell:
                        RVCell.remove(self.board[boxRow+i][boxCol+j])
        return RVCell


    def getRemainingValues(self):
        RV=[]
        for row in range(self.dim):
            for col in range(self.dim):
                if self.board[row][col] != '0':
                    RV.append(['x'])
                else:
                    RV.append(self.getDomain(row,col))
        return RV


    def isSafe(self,row,col,choice):
        choiceStr = str(choice)
        for i in range(self.dim):
            if self.board[row][i] == choiceStr or self.board[i][col] ==choiceStr:
                return False

        boxR = row - (row % 3)
        boxV = col - (col % 3)
        for i in range(3):
            for j in range(3):
                if self.board[boxR + i][boxV + j] == choiceStr:
                    return False
        return True


    def getDomainLength(self,lst):
        if 'x' in lst or lst == []:
            return 10
        else:
            return len(lst)
              

    def getNextMRVRowCol(self):
        rvMap = list(map(self.getDomainLength,self.rv))
        minimum = min(rvMap)
        if minimum == 10:
            return (-1,-1)
        index = rvMap.index(minimum)
        return(index // 9, index % 9)


    def isEmptyDomainProduced(self,row,col,choice):
        element = self.rv.pop(row*9 + col)
        if [] in self.rv:
            self.rv.insert(row*9+col,element)
            return True
        else:
            self.rv.insert(row*9+col,element)
            return False
                

    def solveCSPFH(self):
        location = self.getNextMRVRowCol()
        if location[0] == -1:
            return True
        else:
            self.expandedNodes+=1
            # rv = self.getRemainingValues()
            row = location[0]
            col = location[1]
            for choice in self.rv[row*9+col]:
                choice_str = str(choice)
                self.board[row][col] =  choice_str
                cpy = copy.deepcopy(self.rv) 
                self.rv = self.getRemainingValues()
                
                if not self.isEmptyDomainProduced(row,col,choice_str):
                    if self.solveCSPFH():
                        return True
                self.board[row][col] = '0'
                self.rv = cpy

            return False

    
    def __str__(self):
        string = ''
        for row in self.board:
            for x in row:
                string += x+" "
            string+='\n'
        string+= "Nodes expanded: {}".format(self.expandedNodes)
        return string



# Driver code:
if __name__ == '__main__':
    file = 'test'
    s = SodukuSolver(9,'{}.txt'.format(file))
    start = time()
    s.solveCSPFH()
    end = time()
    print(s)
    print("Time Elapsed:{}".format(end-start))
