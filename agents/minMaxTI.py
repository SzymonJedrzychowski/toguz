class agent:
    def __init__(self, globalDepth=1):
        self.globalDepth = 1
        self.globalDepthMax = globalDepth

    def findMove(self, env):
        self.transpositionalTable = {}
        self.globalDepth = 1

        for i in range(1, self.globalDepthMax+1):
            iterationMove = self.minMaxAlgorithm(env.createCopy(), i)
            self.globalDepth += 1
        return iterationMove

    def minMaxAlgorithm(self, env, depth):
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
                    if stateHash in self.transpositionalTable:
                        if self.transpositionalTable[stateHash][0] >= depth:
                            if self.transpositionalTable[stateHash][1] > value:
                                value = self.transpositionalTable[stateHash][1]
                                move = i
                            skipMinMax = True
                    if not skipMinMax:
                        sim = self.minMaxAlgorithm(newState, depth-1)
                        if stateHash in self.transpositionalTable:
                            if self.transpositionalTable[stateHash][0] > depth-1:
                                self.transpositionalTable[stateHash] = [
                                    depth, sim]
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
                    if stateHash in self.transpositionalTable:
                        if self.transpositionalTable[stateHash][0] >= depth:
                            if self.transpositionalTable[stateHash][1] < value:
                                value = self.transpositionalTable[stateHash][1]
                                move = i
                            skipMinMax = True
                    if not skipMinMax:
                        sim = self.minMaxAlgorithm(newState, depth-1)
                        self.transpositionalTable[stateHash] = [depth, sim]
                        if sim < value:
                            value = sim
                            move = i
            if self.globalDepth == depth:
                return move
            return value
