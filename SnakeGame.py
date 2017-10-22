import pygame, sys, random, time

check_errors = pygame.init()

if check_errors[1] > 0:
    print("(!) Error when initializing program".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) PyGame initialize successful!")


#Display surface
display_width = 700
display_height = 500
playSurface = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake game')

#Colors
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)

#Frame Per Second controller
fpsController = pygame.time.Clock()



#Display menu at the beginning
def gameMenu(show=1):
    while show == 1:
        playSurface.fill(white)
        menuFont = pygame.font.SysFont('monaco', 80)
        menuSurface = menuFont.render('Snake game', True, black)
        menuRect = menuSurface.get_rect()
        menuRect.midtop = ((display_width/2), (display_height/2)-200)
        playSurface.blit(menuSurface, menuRect)
        menuFont = pygame.font.SysFont('monaco', 50)
        menuSurface = menuFont.render('Press enter to start...', True, black)
        menuRect = menuSurface.get_rect()
        menuRect.midtop = ((display_width/2), (display_height/2)+50)
        playSurface.blit(menuSurface, menuRect)
        menuFont = pygame.font.SysFont('monaco', 50)
        menuSurface = menuFont.render('ESC to exit', True, black)
        menuRect = menuSurface.get_rect()
        menuRect.midtop = ((display_width/2), (display_height/2)+100)
        playSurface.blit(menuSurface, menuRect)
        pygame.display.flip()

        gameAction()

#Display score
def showScore(position=1):
    #On the top left corner
    if position == 1:
        scoreFont = pygame.font.SysFont('monaco', 25)
        scoreSurface = scoreFont.render('Score: {0}'.format(score), True, red)
        scoreRect = scoreSurface.get_rect()
        scoreRect.midtop = (50, 20)
    #In the center when GameOver
    else:
        scoreFont = pygame.font.SysFont('monaco', 50)
        scoreSurface = scoreFont.render('Final Score: {0}'.format(score), True, red)
        scoreRect = scoreSurface.get_rect()
        scoreRect.midtop = ((display_width/2), 250)

    playSurface.blit(scoreSurface, scoreRect)

#Game over function
def gameOver():
    playSurface.fill(white)
    gameOverFont = pygame.font.SysFont('monaco', 75)
    gameOverSurface = gameOverFont.render('GameOver', True, red)
    gameOverRect = gameOverSurface.get_rect()
    gameOverRect.midtop = ((display_width/2), 50)
    playSurface.blit(gameOverSurface, gameOverRect)
    gameOverFont = pygame.font.SysFont('monaco', 25)
    gameOverSurface = gameOverFont.render('Press enter to play again', True, red)
    gameOverRect = gameOverSurface.get_rect()
    gameOverRect.midtop = ((display_width/2), (display_height/2)+200)
    playSurface.blit(gameOverSurface, gameOverRect)
    showScore(2)
    pygame.display.flip()

    gameAction()

def gameAction():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                if event.key == pygame.K_RETURN or event.key == ord('\r'):
                    startGame()

def startGame():
    gameStatus = True

    #Initial score
    global score
    score = 0

    #Snake initial start position
    snakePos = [100, 50]
    snakeBody = [[100, 50], [90, 50], [80, 50]]

    #Food position (generate randomly)
    foodPos = [random.randrange(1,70)*10, random.randrange(1,50)*10]
    foodStatus = True

    #Initialize game settings
    direction = 'RIGHT'
    changeTo = direction

    while gameStatus:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    changeTo = 'RIGHT'

                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    changeTo = 'LEFT'

                if event.key == pygame.K_UP or event.key == ord('w'):
                    changeTo = 'UP'

                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    changeTo = 'DOWN'

                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        #Validation fo direction
        if changeTo == 'RIGHT' and not direction == 'LEFT':
            direction = 'RIGHT'

        if changeTo == 'LEFT' and not direction == 'RIGHT':
            direction = 'LEFT'

        if changeTo == 'UP' and not direction == 'DOWN':
            direction = 'UP'

        if changeTo == 'DOWN' and not direction == 'UP':
            direction = 'DOWN'

        #Change th snake position
        if direction == 'RIGHT':
            snakePos[0] += 10

        if direction == 'LEFT':
            snakePos[0] -= 10

        if direction == 'UP':
            snakePos[1] -= 10

        if direction == 'DOWN':
            snakePos[1] += 10

        #Snake body
        snakeBody.insert(0, list(snakePos))
        if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
            score += 10
            foodStatus = False
        else:
            snakeBody.pop()

        if foodStatus == False:
            foodPos = [random.randrange(1,70)*10, random.randrange(1,50)*10]
        foodStatus = True

        playSurface.fill(white)

        #Draw the snake body
        for pos in snakeBody:
            pygame.draw.rect(playSurface, green, pygame.Rect(pos[0], pos[1], 10, 10))

        #Draw the food
        pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1], 10, 10))

        #Set the boundaries for the game
        if snakePos[0] > 690 or snakePos[0] < 10:
            gameOver()
            gameStatus = False
        if snakePos[1] > 490 or snakePos[1] < 10:
            gameOver()
            gameStatus = False

        #Check if snake hits itself
        for block in snakeBody[1:]:
            if snakePos[0] == block[0] and snakePos[1] == block[1]:
                gameOver()
                gameStatus = False

        showScore()
        pygame.display.flip()
        fpsController.tick(50)

gameMenu()
