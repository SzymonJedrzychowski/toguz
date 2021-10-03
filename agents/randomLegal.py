import random

class agent:
    def findMove(self, env):
        return random.choice(env.getLegalMoves())