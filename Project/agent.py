import torch
import random
import numpy as np
from collections import deque
import snake_game

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001 # Learning Rate

agent = None

class Agent:
    game = None
    ai = None
    
    def __init__(self):
        self.game = snake_game.game
        self.ai = snake_game.ai
        
        self.numGames = 0
        self.epsilon = 0 # Randomness
        self.gamma = 0 # Discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft() on max memory
        self.model = None # TODO
        self.trainer = None # TODO
        # TODO: model, trainer
    
    def playStep(self, action):
        self.game.GameStep()
        return self.ai.reward, self.ai.gameWasReset, self.game.snakePos.__len__ - 1
    
    def getState(self, game):
        state = [
            (self.ai.dangerDir[0]), # Danger straight
            (self.ai.dangerDir[1]), # Danger right
            (self.ai.dangerDir[2]), # Danger left
            (self.game.snakeDirection == snake_game.Point(0, 1)), # Moving Up
            (self.game.snakeDirection == snake_game.Point(0, -1)), # Moving Down
            (self.game.snakeDirection == snake_game.Point(-1, 0)), # Moving Left
            (self.game.snakeDirection == snake_game.Point(1, 0)), # Moving Right
            (self.ai.foodDir[0]), # Food Up
            (self.ai.foodDir[1]), # Food Left
            (self.ai.foodDir[2]), # Food Down
            (self.ai.foodDir[3]) # Food Right
        ]
        
        return np.array(state, dtype=int)
    
    def remember(self, state, action, reward, nextState, done):
        self.memory.append((state, action, reward, nextState, done)) # Adds tuple to memory
    
    def trainLongMemory(self):
        if len(self.memory) > BATCH_SIZE: miniSample = random.sample(self.memory, BATCH_SIZE) # Returns list of tuples
        else: miniSample = self.memory
        
        states, actions, rewards, nextStates, dones = zip(*miniSample)
        
        self.trainer.trainStep(states, actions, rewards, nextStates, dones)
    
    def trainShortMemory(self, state, action, reward, nextState, done):
        self.trainer.trainStep(state, action, reward, nextState, done)
    
    def getAction(self, state):
        # Random moves (Tradeoff between exploration / exploitation)
        # Chance of random move starts at 40%, then goes to 0 over 80 moves. Because of (0, 200 < 80)
        self.epsilon = 80 - self.numGames
        finalMove = [0,0,0]
        
        if (random.randint(0, 200) < self.epsilon):
            move = random.randint(0, 2)
            finalMove[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediciton = self.model.predict(state0)
            move = torch.argmax(prediciton).item()
            finalMove[move] = 1
        
        return finalMove
    
def train():
    plotScores = []
    plotMeanScores = []
    totalScore = 0
    recordScore = 0
    agent = Agent()
    game = snake_game.SnakeGame()
    
    while (True):
        # get old state
        stateOld = agent.getState(game)
        
        # Get new move
        finalMove = agent.getAction(stateOld)
        
        # Perform move and get new state
        reward, done, score = agent.playStep(finalMove)
        stateNew = agent.getState(game)
        
        agent.trainShortMemory(stateOld, finalMove, reward, stateNew, done)
        
        # Remember
        agent.remember(stateOld, finalMove, reward, stateNew, done)
        
        if done:
            # Train long memory, plot result
            snake_game.ai.Reset()
            
            agent.numGames += 1
            agent.trainLongMemory()
            
            if score > recordScore:
                recordScore = score
                #agent.model.save()
            
            print('Game', agent.numGames, 'Score', score, 'Record', recordScore)
            # TODO: Plot
            
            
            

if __name__ == '__main__':
    train()