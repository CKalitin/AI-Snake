from collections import namedtuple
import pygame
import random

Point = namedtuple('Point', 'x, y')

game = None
ai = None

class SnakeGame:
    playerControlled = True
    useHardCodedAI = False

    deltaTime = 0.0
    targetFps = 60
    running = True

    stepsSinceReset = 0

    movementInput = [False, False, False, False] # WASD

    rows, cols = (20, 20)

    cellWidth = 16
    cellHeight = 16

    snakeColor = (0, 255, 50)
    foodColor = (255, 50, 0)

    snakePos = Point(0,0)
    foodPos = Point(0,0)

    snakeDirection = Point(1, 0)
    snakeMoveSpeed = 7
    snakeMovementAmount = 0

    foodEaten = False
    
    def __init__(self, playerControlled):
        pygame.init()
        self.screen = pygame.display.set_mode(((self.cols + 1) * self.cellWidth, (self.rows + 1) * self.cellHeight))
        pygame.display.set_caption("AI Snake")
        self.font = pygame.font.SysFont("data/Motorblock.tff", 30)
        
        self.playerControlled = playerControlled
        
        self.ResetGame()
        
        if self.playerControlled: self.GameLoop()
            
    def RenderCells(self):
        for i in range(len(self.snakePos)):
            pygame.draw.rect(self.screen, self.snakeColor, pygame.Rect(self.snakePos[i].x * self.cellWidth, self.snakePos[i].y * self.cellHeight, self.cellWidth, self.cellHeight))
        
        pygame.draw.rect(self.screen, self.foodColor, pygame.Rect(self.foodPos.x * self.cellWidth, self.foodPos.y * self.cellHeight, self.cellWidth, self.cellHeight))
        
    def GameStep(self):
        self.RotateSnake()
        self.MoveSnake()
        
        self.HandleFoodCollisions()
        self.HandleCollisions()
        
        self.stepsSinceReset += 1
        
        if ai: ai.GameStep()

    def GameLoop(self):
        while self.running:
            self.GameLoopStep()

    def GameLoopStep(self):
        self.HandlePygameEvents()
            
        self.screen.fill((0, 0, 0))
        
        self.RenderCells()

        self.DisplayScoreText()
        
        #self.deltaTime = pygame.time.Clock().tick(self.targetFps) / 1000
        if self.playerControlled: self.deltaTime = pygame.time.Clock().tick(self.targetFps) / 1000
        else:  self.deltaTime = 1
        
        if self.useHardCodedAI and self.playerControlled: self.SetMovementInputTowardsFood()
        if self.playerControlled: self.GameStep()

        pygame.display.update()
        

    def ResetGame(self):
        if (ai): ai.GameReset()
        
        self.snakePos = [ Point(random.randrange(0, self.cols), random.randrange(0, self.rows)) ]
        self.snakePos.append(Point(self.snakePos[0].x - 1, self.snakePos[0].y))
        self.snakePos.append(Point(self.snakePos[0].x - 2, self.snakePos[0].y))
        self.foodPos = Point(random.randint(0, self.cols), random.randint(0, self.rows))
        self.snakeDirection = Point(1, 0)
        self.stepsSinceReset = 0
        
    def HandlePygameEvents(self):
        if self.playerControlled: self.movementInput = [False, False, False, False]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.KEYDOWN and self.playerControlled):
                if (event.key == pygame.K_w): self.movementInput[0] = True
                if (event.key == pygame.K_a): self.movementInput[1] = True
                if (event.key == pygame.K_s): self.movementInput[2] = True
                if (event.key == pygame.K_d): self.movementInput[3] = True
        
    def RotateSnake(self):
        previousDirection = self.snakeDirection
        
        if self.movementInput[0]: self.snakeDirection = Point(0, -1)
        if self.movementInput[1]: self.snakeDirection = Point(-1, 0)
        if self.movementInput[2]: self.snakeDirection = Point(0, 1)
        if self.movementInput[3]: self.snakeDirection = Point(1, 0)
        
        if len(self.snakePos) > 1 and (self.snakePos[0].x + self.snakeDirection.x, self.snakePos[0].y + self.snakeDirection.y) == self.snakePos[1]:
            self.snakeDirection = previousDirection

    def MoveSnake(self):
        self.snakeMovementAmount += self.deltaTime * self.snakeMoveSpeed
        
        if (self.snakeMovementAmount > 1):
            self.snakeMovementAmount = 0
            self.snakePos.insert(0, Point(self.snakePos[0].x + self.snakeDirection.x, self.snakePos[0].y + self.snakeDirection.y))
            if (self.foodEaten == False):
                self.snakePos.pop(len(self.snakePos) - 1)
            else:
                self.foodEaten = False
                
    def HandleCollisions(self):
        if (self.snakePos[0].x < 0 or self.snakePos[0].x > self.cols or self.snakePos[0].y < 0 or self.snakePos[0].y > self.rows):
            self.ResetGame()

        for i in range(len(self.snakePos)):
            if i != 0 and i < len(self.snakePos) and self.snakePos[0] == self.snakePos[i]:
                self.ResetGame()
                
    def HandleFoodCollisions(self):
        if (self.snakePos[0] == self.foodPos):
            self.SpawnFood()
            self.foodEaten = True
            if (ai): ai.FoodEaten()

    def SpawnFood(self):
        self.foodPos = Point(random.randint(0, self.cols), random.randint(0, self.rows))
        while self.CheckFoodInSnake():
            self.foodPos = Point(random.randint(0, self.cols), random.randint(0, self.rows))
            
    def CheckFoodInSnake(self):
        for i in range(len(self.snakePos)):
            if (self.snakePos[i] == self.foodPos):
                return True
        return False

    def DisplayScoreText(self):
        scoreText = self.font.render(f"Score: {len(self.snakePos) - 3}", True, (255,255,255))
        self.screen.blit(scoreText, (10, 10))
        
    def SetMovementInputTowardsFood(self):
        foodUp = self.foodPos.y > self.snakePos[0].y
        foodDown = self.foodPos.y < self.snakePos[0].y
        foodLeft = self.foodPos.x < self.snakePos[0].x
        foodRight = self.foodPos.x > self.snakePos[0].x
        
        if foodUp and self.snakeDirection != Point(0, 1):
            self.movementInput = [False, False, True, False]
        elif foodDown and self.snakeDirection != Point(0, -1):
            self.movementInput = [True, False, False, False]
        elif foodLeft and self.snakeDirection != Point(-1, 0):
           self.movementInput = [False, True, False, False]
        elif foodRight and self.snakeDirection != Point(1, 0):
            self.movementInput = [False, False, False, True]

class SnakeAI:
    reward = 0
    score = 0
    gameWasReset = False
    
    foodDir = [False, False, False, False] # Up, Left, Down, Right / WASD
    dangerDir = [False, False, False] # Forward, Right, Left
    
    def Reset(self):
        self.reward = 0
        self.score = 0
        self.gameWasReset = False
    
    def GameStep(self):
        # If snake has done nothing for 100 game steps
        if game.stepsSinceReset > 100*len(game.snakePos):
            game.ResetGame()

        if len(game.snakePos) > 3:
            self.score = len(game.snakePos) - 3

        self.GetDangerDirection()
        self.GetFoodDirection()
            
    def GameReset(self):
        self.reward -= 10
        self.gameWasReset = True
        
    def FoodEaten(self):
        self.reward += 15
        
    def GetDangerDirection(self):
        self.dangerDir = [False, False, False]
    
        # Convert to Point
        forwardPos = Point(game.snakePos[0].x + game.snakeDirection.x, game.snakePos[0].y + game.snakeDirection.y)
        rightPos = Point(game.snakePos[0].x + self.LocalDirtoGameDir(1).x, game.snakePos[0].y + self.LocalDirtoGameDir(1).y)
        leftPos = Point(game.snakePos[0].x + self.LocalDirtoGameDir(2).x, game.snakePos[0].y + self.LocalDirtoGameDir(2).y)
        
        # Borders
        if (forwardPos.x < 0 or forwardPos.x > game.cols or forwardPos.y < 0 or forwardPos.y > game.rows): self.dangerDir[0] = True
        if (rightPos.x < 0 or rightPos.x > game.cols or rightPos.y < 0 or rightPos.y > game.rows): self.dangerDir[1] = True
        if (leftPos.x < 0 or leftPos.x > game.cols or leftPos.y < 0 or leftPos.y > game.rows): self.dangerDir[2] = True
            
        # Snake
        for i in range(len(game.snakePos)):
            if forwardPos == game.snakePos[i]: self.dangerDir[0] = True
            if rightPos == game.snakePos[i]: self.dangerDir[1] = True
            if leftPos == game.snakePos[i]: self.dangerDir[2] = True
        
    def GetFoodDirection(self):
        self.foodDir = [False, False, False, False]
        
        self.foodDir[0] = game.foodPos.y > game.snakePos[0].y
        self.foodDir[1] = game.foodPos.x < game.snakePos[0].x
        self.foodDir[2] = game.foodPos.y < game.snakePos[0].y
        self.foodDir[3] = game.foodPos.x > game.snakePos[0].x
    
    def LocalDirtoGameDir(self, localDir):
        # Local Direction (Forward, Right, Left) to Game Direction
        if localDir == 0:
            return game.snakeDirection
        elif localDir == 1:
            if game.snakeDirection == Point(0, 1): return Point(1,0)
            elif game.snakeDirection == Point(0, -1): return Point(-1, 0)
            elif game.snakeDirection == Point(1, 0): return Point(0, -1)
            elif game.snakeDirection == Point(-1, 0): return Point(0, 1)
        elif localDir == 2:
            if game.snakeDirection == Point(0, 1): return Point(-1,0)
            elif game.snakeDirection == Point(0, -1): return Point(1, 0)
            elif game.snakeDirection == Point(1, 0): return Point(0, 1)
            elif game.snakeDirection == Point(-1, 0): return Point(0, -1)
    
if __name__ == '__main__':
    game = SnakeGame(True)