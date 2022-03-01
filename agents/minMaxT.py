class agent:
    def __init__(self, globalDepth=1):
        self.globalDepth = globalDepth

    def findMove(self, env, depth=None):
        if depth == None:
            depth = self.globalDepth
            self.transpositionTable = {}

        availableMoves = env.getLegalMoves()
        if env.currentPlayer == 1:
            value = -500
            for i in availableMoves:
                newState = env.createCopy()
                newState.move(i)
                reward, score, done = newState.ifTerminal()
                if reward != 0:
                    reward *= 100
                else:
                    reward = score[1]-score[-1]
                newState.currentPlayer *= -1
                if done or depth == 1:
                    if reward > value:
                        value = reward
                        move = i
                else:
                    skipMinMax = False
                    stateHash = hash(newState)
                    if stateHash in self.transpositionTable:
                        if self.transpositionTable[stateHash][0] >= depth:
                            if self.transpositionTable[stateHash][1] > value:
                                value = self.transpositionTable[stateHash][1]
                                move = i
                            skipMinMax = True
                    if not skipMinMax:
                        sim = self.findMove(newState, depth-1)
                        self.transpositionTable[stateHash] = [depth, sim]
                        if sim > value:
                            value = sim
                            move = i
            if self.globalDepth == depth:
                return move
            return value
        else:
            value = 500
            for i in availableMoves:
                newState = env.createCopy()
                newState.move(i)
                reward, score, done = newState.ifTerminal()
                if reward != 0:
                    reward *= 100
                else:
                    reward = score[1]-score[-1]
                newState.currentPlayer *= -1
                if done or depth == 1:
                    if reward < value:
                        value = reward
                        move = i
                else:
                    skipMinMax = False
                    stateHash = hash(newState)
                    if stateHash in self.transpositionTable:
                        if self.transpositionTable[stateHash][0] >= depth:
                            if self.transpositionTable[stateHash][1] < value:
                                value = self.transpositionTable[stateHash][1]
                                move = i
                            skipMinMax = True
                    if not skipMinMax:
                        sim = self.findMove(newState, depth-1)
                        self.transpositionTable[stateHash] = [depth, sim]
                        if sim < value:
                            value = sim
                            move = i

            if self.globalDepth == depth:
                return move
            return value
