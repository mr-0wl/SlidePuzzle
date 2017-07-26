# Slide Puizzle
# From Invent with Python
#craighole.com
#Creative Commons

import pygame, sys, random
from pygame.locals import *

# Create the constants (try different values)
BOARDWIDTH = int(input("Boardwidth 4 is the default >"))
BOARDHEIGHT = int(input("Boardheight 4 is the default >"))
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

#
BLACK = (0,0,0)
WHITE = (255,255,255)
BRIGHTBLUE = (0,50,255)
DARKTURQUOISE = (3,54,73)
GREEN = (0,204,0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH -1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) /2 )

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    #Store the option buttons and their rectangles in OPTIONS
    RESET_SURF.RESET_RECT = makeText('Reset', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    NEW_SURF, NEW_RECT = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    mainBoard, solutionSeq = generateNewPuzzle(80)
    SOLVEDBOARD = getStartingBoard() #solved board is the same as a board in the start state
    allMoves = [] # list of moves made from the solved configuration

    while True: #main loop
        slideTo = None #the direction a tile should slide
        msg = '' #message to show in upper corner
        if mainBoard == SOLVEDBOARD:
            msg = 'Solved!'

        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get(): #event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    #check if an option button has been clicked
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves) #clicked reset button
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(80) #clicked new game
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves) #clicked solve button
                        allMoves = []
                    else:
                        #check if the clicked tile was next to the blank spot

                        blankx.blanky = getBlankPosition(mainBoard)
                        if spotx == blankx + 1 and spoty == blanky:
                            slideTo = LEFT
                        elif spotx == blankx - 1 and spoty == blanky:
                            slideTo = RIGHT
                        elif spotx == blankx and spoty == blanky + 1:
                            slideTo = UP
                        elif spotx == blankx and spoty == blanky - 1:
                            slideTo = DOWN

                elif event.type == KEYUP:
                    #Check if the user used a key to slide the tile
                    if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                        slideTo = LEFT
                    elif event.key in (K_RIGHT, K_D) and isValidMove(mainBoard, RIGHT):
                        slideTo = RIGHT
                    elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                        slideTo = UP
                    elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                        slideTo = DOWN

            if slideTo:
                slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide', 8) #show slide on screen
                makeMove(mainBoard, slideTo)
                allMoves.append(slideTo) # record the slide
            pygame.display.update()
            FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the quit events
        terminate() #terminate method called if quit event present
    for event in pygame.event.get(KEYUP): #get all keyup events
        if event.key == K_ESCAPE:
            terminate() #esc key kills
        pygame.event.post(event) #put the other KEYUP events back


def getStartingBoard():
    # Return a board data structure with tiles in the solved state
    # eg.if BOARDWIDTH and BOARDHEIGHT are both 3 this will return
    # [[1,4,7],[2,5,8],[3,6,None]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT -1) + BOARDWIDTH -1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = None
    return board


def getBlankPosition(board):
    # return the x and y of board coords of the blank space
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == None:
                return (x,y)


def makeMove(board, move):
    #This does not check if the move is valid
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky -1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx -1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
        (move == DOWN and blanky != 0) \
        (move == LEFT and blankx != len(board) -1) or \
        (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
                            
                            
                    
