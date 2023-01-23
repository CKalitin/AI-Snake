import pygame
import random

# How To Improve This:
# 1. Make it a class
# 2. instead of (0,0) have a struct/class for Vector2s/Points (namedTuple)

#region Variables

playerControlled = True
useHardCodedAI = False

deltaTime = 0.0
targetFps = 60
running = True

movementInput = [False, False, False, False] # WASD

#endregion

#region Game Variables

rows, cols = (20, 20)

cellWidth = 24
cellHeight = 24

snakeColor = (0, 255, 50)
foodColor = (255, 50, 0)

snakePos = [ (random.randrange(0, cols), random.randrange(0, rows)) ]
foodPos = (random.randint(0, cols), random.randint(0, rows))

while foodPos == snakePos[0]:
    (random.randint(0, cols), random.randint(0, rows))

snakeDirection = (1, 0)
snakeMoveSpeed = 7
snakeMovementAmount = 0

foodEaten = False

#endregion

#region Pygame

pygame.init()

screen = pygame.display.set_mode(((cols + 1) * cellWidth, (rows + 1) * cellHeight))

pygame.display.set_caption("AI Snake")

font = pygame.font.SysFont("data/Motorblock.tff", 24)

#endregion

#region Drawing Functions

def RenderCells():
    for i in range(len(snakePos)):
        pygame.draw.rect(screen, snakeColor, pygame.Rect(snakePos[i][0] * cellWidth, snakePos[i][1] * cellHeight, cellWidth, cellHeight))
    
    pygame.draw.rect(screen, foodColor, pygame.Rect(foodPos[0] * cellWidth, foodPos[1] * cellHeight, cellWidth, cellHeight))

#endregion

#region Movement Functions

def RotateSnake(w, a, s, d):
    global snakeDirection
    global snakeMovementAmount
    
    previousDirection = snakeDirection
    
    if w:
        snakeDirection = (0, -1)
    if a:
        snakeDirection = (-1, 0)
    if s:
        snakeDirection = (0, 1)
    if d:
        snakeDirection = (1, 0)
    
    if snakePos.__len__() > 1 and (snakePos[0][0] + snakeDirection[0], snakePos[0][1] + snakeDirection[1]) == snakePos[1]:
        snakeDirection = previousDirection

def MoveSnake():
    global snakeMovementAmount
    global foodEaten
    
    snakeMovementAmount += deltaTime * snakeMoveSpeed
    
    if (snakeMovementAmount > 1):
        snakeMovementAmount = 0
        snakePos.insert(0, (snakePos[0][0] + snakeDirection[0], snakePos[0][1] + snakeDirection[1]))
        if (foodEaten == False):
            snakePos.pop(snakePos.__len__() - 1)
        else:
            foodEaten = False

#endregion

#region Collisions and Food

def HandleWallCollisions():
    if (snakePos[0][0] < 0 or snakePos[0][0] > 20 or snakePos[0][1] < 0 or snakePos[0][1] > 20):
        ResetGame()

def HandleSnakeCollisions():
    for i in range(snakePos.__len__()):
        if i != 0 and i < snakePos.__len__() and snakePos[0] == snakePos[i]:
            ResetGame()

def HandleFoodCollisions():
    global foodEaten
    global foodPos
    
    if (snakePos[0] == foodPos):
        SpawnFood()
        foodEaten = True

def SpawnFood():
    global foodPos
    
    foodPos = (random.randint(0, cols), random.randint(0, rows))
    while CheckFoodInSnake():
        foodPos = (random.randint(0, cols), random.randint(0, rows))

def CheckFoodInSnake():
    for i in range(snakePos.__len__()):
        if (snakePos[i] == foodPos):
            return True
    return False


#endregion

#region GUI

def DisplayGUI():
    ScoreText()

def ScoreText():
    scoreText = font.render(f"Score: {snakePos.__len__() - 1}", True, (255,255,255))
    screen.blit(scoreText, (10, 10))

#endregion

#region Basic AI

def SetMovementInputTowardsFood():
    global movementInput
    
    foodUp = foodPos[1] > snakePos[0][1]
    foodDown = foodPos[1] < snakePos[0][1]
    foodLeft = foodPos[0] < snakePos[0][0]
    foodRight = foodPos[0] > snakePos[0][0]
    
    if foodUp and snakeDirection != (0, 1):
        movementInput = [False, False, True, False]
    elif foodDown and snakeDirection != (0, -1):
        movementInput = [True, False, False, False]
    elif foodLeft and snakeDirection != (-1, 0):
        movementInput = [False, True, False, False]
    elif foodRight and snakeDirection != (1, 0):
        movementInput = [False, False, False, True]

#endregion

#region Game

def GameStep():
    HandleFoodCollisions()
    HandleWallCollisions()
    HandleSnakeCollisions()
    
    RotateSnake(movementInput[0], movementInput[1], movementInput[2], movementInput[3])
    MoveSnake()
    
    RenderCells()

    DisplayGUI()

def ResetGame():
    global snakePos
    global foodPos
    global snakeDirection
    
    snakePos = [ (random.randrange(0, cols), random.randrange(0, rows)) ]
    foodPos = (random.randint(0, cols), random.randint(0, rows))
    snakeDirection = (1, 0)

def HandlePygameEvents():
    global running
    global movementInput
    
    movementInput = [False, False, False, False]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (event.type == pygame.KEYDOWN and playerControlled):
            if (event.key == pygame.K_w): movementInput[0] = True
            if (event.key == pygame.K_a): movementInput[1] = True
            if (event.key == pygame.K_s): movementInput[2] = True
            if (event.key == pygame.K_d): movementInput[3] = True

#endregion

while running:
    HandlePygameEvents()
    
    screen.fill((0, 0, 0))

    if playerControlled: deltaTime = pygame.time.Clock().tick(targetFps) / 1000
    else:  deltaTime = 1
    
    if useHardCodedAI and playerControlled:
        SetMovementInputTowardsFood()
        
    GameStep()

    pygame.display.update()
