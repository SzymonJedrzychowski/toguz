import copy

class agent:
    def __init__(self, globalDepth=1):
        self.globalDepth = globalDepth
    
    def findMove(self, env, depth=None):
        if depth == None:
            depth = self.globalDepth
        maxi = env.currentPlayer==1

        availableMoves = env.getLegalMoves()
        if maxi:
            value = -500
            for i in availableMoves:
                newState = copy.deepcopy(env)
                newState.move(i)
                reward, score, done = newState.ifTerminal()
                if reward != 0:
                    reward *= 100
                else:
                    reward = score[1]-score[-1]
                newState.currentPlayer *= -1
                if done or depth==1:
                    if reward > value:
                        value = reward
                        move = i
                else:
                    sim = self.findMove(newState, depth-1)
                    if sim > value:
                        value = sim
                        move = i
            if self.globalDepth==depth:
                return move
            return value
        else:
            value = 500
            for i in availableMoves:
                newState = copy.deepcopy(env)
                newState.move(i)
                reward, score, done = newState.ifTerminal()
                if reward != 0:
                    reward *= 100
                else:
                    reward = score[1]-score[-1]
                newState.currentPlayer *= -1
                if done or depth==1:
                    if reward < value:
                        value = reward
                        move = i
                else:
                    sim = self.findMove(newState, depth-1)
                    if sim < value:
                        value = sim
                        move = i
            if self.globalDepth==depth:
                return move
            return value