# toguz

## Description

Toguz korgol is a game from mancala family. (More information on: https://en.wikipedia.org/wiki/Toguz_korgol).

## Agents

Currently, there is 6 agents that can play the game:
    - human player,
    - randomLegal - agent that knows what moves are legal, and chooses one of them,
    - totalRandom - agent that picks a random place on board,
    - minMax - standard minMax algorithm,
    - minMaxAB - minMax algorithm with alpha-beta prunning,
    - mcts - Monte carlo tree search.

## How to use

To choose agents that will be playing, change the name of class in agent dictionary in main.py file. Player 1 is always starting first.
For agents minMax and minMaxAB, depth (int) needs to be specified.
For agent mcts, number of iterations (int) and exploration constant (float) needs to be specified.