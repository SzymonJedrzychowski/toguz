import random

class agent:
    def findMove(self, env):
        return random.randint(0, env.size-1)