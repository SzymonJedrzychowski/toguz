from game.toguzGame import gameState
from agents import human, randomLegal, totalRandom, minMax, minMaxAB, mcts

env = gameState(9)

agent = {
    1: minMaxAB.agent(7),
    -1: mcts.agent(25000, 3)
}

results = []
gameCount = 0

while gameCount < 1:
    env.resetState()
    done = False
    while not done:
        env.printBoard()
        a = agent[env.currentPlayer].findMove(env)
        if a in env.getLegalMoves():
            env.move(a)
            reward, score, done = env.ifTerminal()
            env.currentPlayer *= -1
        else:
            reward = -env.currentPlayer
            done = True
    env.printBoard(True)
    print("RESULT: {}".format(reward))
    results.append(reward)
    gameCount += 1

print(results.count(1), results.count(0), results.count(-1))
