import ujson

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
        print("1: {}, -1: {}".format(self.score[1], self.score[-1]))
        print("")
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
        print()
        print()
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
        print()
        print()
        if not done:
            print("Move of {}".format(self.currentPlayer))

    def createCopy(self):
        newState = gameState(self.size)
        thisStateDict = {"board": self.board, "currentPlayer": self.currentPlayer, "tuz": self.tuz, "score": self.score}
        d = ujson.loads(ujson.dumps(thisStateDict))
        newState.board = d["board"]
        newState.currentPlayer = d["currentPlayer"]
        newState.tuz = {
            -1: d["tuz"]["-1"],
            1: d["tuz"]["1"]
        }
        newState.score = {
            -1: d["score"]["-1"],
            1: d["score"]["1"]
        }
        return newState
