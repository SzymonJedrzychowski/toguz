import random
import math

class agent:
    def __init__(self, maxI=10, c=1.41):
        self.maxI = maxI
        self.c = c

    def findMove(self, env):
        currentNode = node(env)
        i = 0
        
        while i < self.maxI:
            selectedNode = currentNode.select(self.c)
            while selectedNode != None:
                selectedNode = selectedNode.select(self.c)
            i+= 1
        
        UCB = [j.reward/j.visits for j in currentNode.children]
        
        if currentNode.state.currentPlayer == 1:
            nextMove = random.choice([i for i in range(len(UCB)) if UCB[i] == max(UCB)])
        else:
            nextMove = random.choice([i for i in range(len(UCB)) if UCB[i] == min(UCB)])
        
        return currentNode.children[nextMove].action

class node:
    def __init__(self, state, action=None, parent=None):
        self.state = state
        self.action = action
        self.reward = 0
        self.visits = 0
        self.children = []
        self.parent = parent
    
    def select(self, c):
        if self.children == []:
            s = self.state.createCopy()
            s.currentPlayer *= -1

            self.expand()

            for i in self.children:
                i.visits = 0.0001

            if len(self.children) == 0:
                return None

            newState = random.choice(self.children)
            reward = newState.randomPolicy()
            newState.propagate(reward)

        else:
            if self.state.currentPlayer == 1:
                UCB = [i.reward/i.visits+c*(2*math.log(self.visits)/i.visits)**0.5 for i in self.children]
            else:
                UCB = [-i.reward/i.visits+c*(2*math.log(self.visits)/i.visits)**0.5 for i in self.children]
            nextMove = random.choice([i for i in range(len(UCB)) if UCB[i] == max(UCB)])
            newNode = self.children[nextMove]

            return newNode
            
    def expand(self):
        if self.children == []:
            for i in self.state.getLegalMoves():
                newState = self.state.createCopy()
                newState.move(i)
                newState.currentPlayer *= -1
                self.children.append(node(newState, i, parent=self))

    def propagate(self, reward):
        currentNode = self
        
        while currentNode.parent != None:
            currentNode = currentNode.parent
            currentNode.visits = int(currentNode.visits + 1)
            currentNode.reward += reward

    def randomPolicy(self):
        thisState = self.state.createCopy()
        
        thisState.currentPlayer *= -1
        reward, _, done = thisState.ifTerminal()
        thisState.currentPlayer *= -1
        
        if done:
            self.reward += reward
            self.visits = int(self.visits + 1)
            return reward
        else:
            while True:
                availableMoves = thisState.getLegalMoves()

                thisState.move(random.choice(availableMoves))

                reward, _, done = thisState.ifTerminal()
                thisState.currentPlayer *= -1
                if done:
                    self.reward += reward
                    self.visits = int(self.visits+1)
                    return reward