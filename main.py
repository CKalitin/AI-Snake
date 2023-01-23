import time
import pygame
import random
import math

#region Variables

deltaTime = 0.0
targetFps = 60

rows, cols = (20, 20)

cellWidth = 24
cellHeight = 24

cellTypes = [
    (0,100,0), # Background
    (0, 100, 255), # Snake
    (255, 50, 0), # Food
]

snakeColor = (0, 255, 50)
foodColor = (255, 50, 0)

snakePos = [ (random.randrange(0, cols), random.randrange(0, rows)) ]

foodPos = (random.randint(0, cols), random.randint(0, rows))

snakeDirection = (1, 0)
snakeMoveSpeed = 7
snakeMovementAmount = 0

while foodPos == snakePos[0]:
    (random.randint(0, cols), random.randint(0, rows))

foodEaten = False

scoreTextPos = (10, 10)

#endregion

#region Pygame

pygame.init()

screen = pygame.display.set_mode(((cols + 1) * cellWidth, (rows + 1) * cellHeight))

pygame.display.set_caption("AI Snake")

t0 = time.time()
font = pygame.font.SysFont("data/Motorblock.tff", 24)
print('time needed for Font creation :', time.time()-t0)

#endregion

#region Drawing Functions

def RenderCells():
    for i in range(len(snakePos)):
        pygame.draw.rect(screen, snakeColor, pygame.Rect(snakePos[i][0] * cellWidth, snakePos[i][1] * cellHeight, cellWidth, cellHeight))
    
    pygame.draw.rect(screen, foodColor, pygame.Rect(foodPos[0] * cellWidth, foodPos[1] * cellHeight, cellWidth, cellHeight))

#endregion

#region Player Functions

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
        foodPos = (random.randint(0, cols), random.randint(0, rows))
        foodEaten = True

def ResetGame():
    global snakePos
    global foodPos
    global snakeDirection
    
    snakePos = [ (random.randrange(0, cols), random.randrange(0, rows)) ]
    foodPos = (random.randint(0, cols), random.randint(0, rows))
    snakeDirection = (1, 0)

#endregion

#region GUI

def DisplayGUI():
    ScoreText()

def ScoreText():
    scoreText = font.render(f"Score: {snakePos.__len__() - 1}", True, (255,255,255))
    screen.blit(scoreText, (scoreTextPos[0], scoreTextPos[1]))

#endregion

running = True
while running:
    input = [False, False, False, False] # WASD
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_w): input[0] = True
            if (event.key == pygame.K_a): input[1] = True
            if (event.key == pygame.K_s): input[2] = True
            if (event.key == pygame.K_d): input[3] = True
            
    screen.fill((0, 0, 0))

    deltaTime = pygame.time.Clock().tick(targetFps) / 1000
    
    HandleFoodCollisions()
    HandleWallCollisions()
    HandleSnakeCollisions()
    
    RotateSnake(input[0], input[1], input[2], input[3])
    MoveSnake()
    
    RenderCells()

    DisplayGUI()

    pygame.display.update()
