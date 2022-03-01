class gameState:
    def __init__(self, size):
        self.size = size
        self.resetState()
    
    def resetState(self):
        self.currentPlayer = 1
        self.board = [self.size for i in range(self.size*2)]
        self.score = {
            1: 0,
            -1: 0
        }
        self.tuz = {
            1: None,
            -1: None
        }

    def ifTerminal(self):
        if self.currentPlayer == -1:
            if sum(self.board[0:self.size]) == 0:
                self.score[-1] += sum(self.board[self.size:])
        elif self.currentPlayer == 1:
            if sum(self.board[self.size:]) == 0:
                self.score[1] += sum(self.board[0:self.size])
        if self.score[1] > self.size**2:
            return 1, self.score, True
        elif self.score[-1] > self.size**2:
            return -1, self.score, True
        elif self.score[1]+self.score[-1] == 2*self.size**2:
            return 0, self.score, True
        
        return 0, self.score, False

    def move(self, place):
        if self.currentPlayer == -1:
            place += self.size
        
        balls = self.board[place]
        self.board[place] = 0
        if balls == 1:
            drop = place+1
            if drop >= 2*self.size:
                drop = 0
            self.board[drop] += 1
        else:
            drop = place-1
            for _ in range(balls):
                drop += 1
                if drop >= 2*self.size:
                    drop = 0
                self.board[drop] += 1

        if self.currentPlayer == 1 and drop >= self.size:
            if self.board[drop]%2 == 0:
                self.score[1] += self.board[drop]
                self.board[drop] = 0
            elif self.board[drop] == 3 and self.tuz[1] == None:
                if drop != self.size*2-1:
                    if self.tuz[-1] == None:
                        self.score[1] += 3
                        self.board[drop] = 0
                        self.tuz[1] = drop
                    else:
                        if self.tuz[-1]+self.size != drop:
                            self.score[1] += 3
                            self.board[drop] = 0
                            self.tuz[1] = drop
        elif self.currentPlayer == -1 and drop < self.size:
            if self.board[drop]%2 == 0:
                self.score[-1] += self.board[drop]
                self.board[drop] = 0
            elif self.board[drop] == 3 and self.tuz[-1] == None:
                if drop != self.size-1:
                    if self.tuz[1] == None:
                        self.score[-1] += 3
                        self.board[drop] = 0
                        self.tuz[-1] = drop
                    else:
                        if self.tuz[1]-self.size != drop:
                            self.score[-1] += 3
                            self.board[drop] = 0
                            self.tuz[-1] = drop
        
        if self.tuz[1] != None:
            self.score[1] += self.board[self.tuz[1]]
            self.board[self.tuz[1]] = 0
        if self.tuz[-1] != None:
            self.score[-1] += self.board[self.tuz[-1]]
            self.board[self.tuz[-1]] = 0

    def getLegalMoves(self):
        if self.currentPlayer == 1:
            return [i for i in range(self.size) if self.board[i] > 0]
        else:
            return [i for i in range(self.size) if self.board[i+self.size] > 0]

    def printBoard(self, done=False):
        print("---")
        print("1: {}, -1: {}\n".format(self.score[1], self.score[-1]))
        for i in range(self.size):
            if self.tuz[1] == self.size*2-1-i:
                print(" T", end = " ")
            else:
                print(" {}".format(self.size-i-1), end = " ")
        print()
        for i in range(self.size):
            if self.board[self.size*2-i-1] > 9:
                print(self.board[self.size*2-1-i], end = " ")
            else:
                print(" {}".format(self.board[self.size*2-1-i]), end = " ")
        print("\n")
        for i in range(self.size):
            if self.board[i] > 9:
                print(self.board[i], end = " ")
            else:
                print(" {}".format(self.board[i]), end = " ")
        print()
        for i in range(self.size):
            if self.tuz[-1] == i:
                print(" T", end = " ")
            else:
                print(" {}".format(i), end = " ")
        print("\n")
        if not done:
            print("Move of {}".format(self.currentPlayer))

    def createCopy(self):
        toReturn = gameState(self.size)
        toReturn.board = [i for i in self.board]
        toReturn.tuz = {1: self.tuz[1], -1: self.tuz[-1]}
        toReturn.score = {1: self.score[1], -1: self.score[-1]}
        toReturn.currentPlayer = self.currentPlayer
        return toReturn

    def __eq__(self, other):
        return self.board == other.board and self.currentPlayer == other.currentPlayer and self.tuz == other.tuz and self.score == other.score 

    def __hash__(self):
        return hash(":".join([str(j) for j in [i for i in self.board]+[self.score[-1], self.score[1], self.tuz[-1], self.tuz[1], self.currentPlayer]]))