from collections import namedtuple
import pygame
import random

Point = namedtuple('Point', 'x, y')

game = None

class SnakeGame:
    playerControlled = True
    useHardCodedAI = False

    deltaTime = 0.0
    targetFps = 60
    running = True

    movementInput = [False, False, False, False] # WASD

    rows, cols = (20, 20)

    cellWidth = 24
    cellHeight = 24

    snakeColor = (0, 255, 50)
    foodColor = (255, 50, 0)

    snakePos = Point(0,0)
    foodPos = Point(0,0)

    snakeDirection = Point(1, 0)
    snakeMoveSpeed = 7
    snakeMovementAmount = 0

    foodEaten = False
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(((self.cols + 1) * self.cellWidth, (self.rows + 1) * self.cellHeight))
        pygame.display.set_caption("AI Snake")
        self.font = pygame.font.SysFont("data/Motorblock.tff", 24)
        
        self.ResetGame()
        
        if self.playerControlled:
            self.GameLoop()
            
    def RenderCells(self):
        for i in range(len(self.snakePos)):
            pygame.draw.rect(self.screen, self.snakeColor, pygame.Rect(self.snakePos[i].x * self.cellWidth, self.snakePos[i].y * self.cellHeight, self.cellWidth, self.cellHeight))
        
        pygame.draw.rect(self.screen, self.foodColor, pygame.Rect(self.foodPos.x * self.cellWidth, self.foodPos.y * self.cellHeight, self.cellWidth, self.cellHeight))
        
    def GameStep(self):
        self.HandleFoodCollisions()
        self.HandleCollisions()
        
        self.RotateSnake()
        self.MoveSnake()
        
        self.RenderCells()

        self.DisplayScoreText()

    def GameLoop(self):
        while self.running:
            self.HandlePygameEvents()
            
            self.screen.fill((0, 0, 0))

            if self.playerControlled: self.deltaTime = pygame.time.Clock().tick(self.targetFps) / 1000
            else:  self.deltaTime = 1
            
            if self.useHardCodedAI and self.playerControlled:
                self.SetMovementInputTowardsFood()
                
            self.GameStep()

            pygame.display.update()

    def ResetGame(self):
        self.snakePos = [ Point(random.randrange(0, self.cols), random.randrange(0, self.rows)) ]
        self.foodPos = Point(random.randint(0, self.cols), random.randint(0, self.rows))
        self.snakeDirection = Point(1, 0)
        
    def HandlePygameEvents(self):
        self.movementInput = [False, False, False, False]
        
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
        
        if self.snakePos.__len__() > 1 and (self.snakePos[0].x + self.snakeDirection.x, self.snakePos[0].y + self.snakeDirection.y) == self.snakePos[1]:
            self.snakeDirection = previousDirection

    def MoveSnake(self):
        self.snakeMovementAmount += self.deltaTime * self.snakeMoveSpeed
        
        if (self.snakeMovementAmount > 1):
            self.snakeMovementAmount = 0
            self.snakePos.insert(0, Point(self.snakePos[0].x + self.snakeDirection.x, self.snakePos[0].y + self.snakeDirection.y))
            if (self.foodEaten == False):
                self.snakePos.pop(self.snakePos.__len__() - 1)
            else:
                self.foodEaten = False
                
    def HandleCollisions(self):
        if (self.snakePos[0].x < 0 or self.snakePos[0].x > 20 or self.snakePos[0].y < 0 or self.snakePos[0].y > 20):
            self.ResetGame()

        for i in range(self.snakePos.__len__()):
            if i != 0 and i < self.snakePos.__len__() and self.snakePos[0] == self.snakePos[i]:
                self.ResetGame()
                
    def HandleFoodCollisions(self):
        if (self.snakePos[0] == self.foodPos):
            self.SpawnFood()
            self.foodEaten = True

    def SpawnFood(self):
        self.foodPos = Point(random.randint(0, self.cols), random.randint(0, self.rows))
        while self.CheckFoodInSnake():
            self.foodPos = Point(random.randint(0, self.cols), random.randint(0, self.rows))
            
    def CheckFoodInSnake(self):
        for i in range(self.snakePos.__len__()):
            if (self.snakePos[i] == self.foodPos):
                return True
        return False

    def DisplayScoreText(self):
        scoreText = self.font.render(f"Score: {self.snakePos.__len__() - 1}", True, (255,255,255))
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
    
if __name__ == '__main__':
    game = SnakeGame()