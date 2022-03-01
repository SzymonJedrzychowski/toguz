from game.toguzGame import gameState
from agents import human, totalRandom, randomLegal, minMax, minMaxT, minMaxTI, minMaxAB, mcts

GAME_SIZE = 5
GAMES_NUMBER = 1

playingAgents = {
    1: mcts.agent(300),
    -1: minMaxAB.agent(3)
}

results = []
gameCount = 0
env = gameState(GAME_SIZE)

while gameCount < GAMES_NUMBER:
    env.resetState()
    done = False
    while not done:
        env.printBoard()
        calculatedMove = playingAgents[env.currentPlayer].findMove(env)
        if calculatedMove in env.getLegalMoves():
            env.move(calculatedMove)
            reward, score, done = env.ifTerminal()
            env.currentPlayer *= -1
        else:
            reward = -env.currentPlayer
            done = True
    env.printBoard(True)
    results.append(reward)
    gameCount += 1

print("RESULTS: 1W: {} - D: {} - -1W: {}".format(results.count(1),
      results.count(0), results.count(-1)))
