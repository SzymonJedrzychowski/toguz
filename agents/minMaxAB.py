class agent:
    def __init__(self, globalDepth=1):
        self.globalDepth = globalDepth

    def findMove(self, env, a=-200, b=200, depth=None):
        if depth == None:
            depth = self.globalDepth

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
                    deeperValue = self.findMove(newState, a, b, depth-1)
                    if deeperValue > value:
                        value = deeperValue
                        move = i
                if value >= b:
                    break
                a = max(a, value)
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
                    deeperValue = self.findMove(newState, a, b, depth-1)
                    if deeperValue < value:
                        value = deeperValue
                        move = i
                if value <= a:
                    break
                b = min(b, value)
            if self.globalDepth == depth:
                return move
            return value
