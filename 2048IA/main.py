from PIL import ImageGrab, ImageOps
import pyautogui
import math
import time

"""Contains the current status of the grid"""
currentGrid = [0, 0, 0, 0,
               0, 0, 0, 0,
               0, 0, 0, 0,
               0, 0, 0, 0]

"""Calculates the score : Keeps the best values at the top left corner of the grid"""
scoreGrid = [50, 30, 20, 0,
             30, 20, 10, 0,
             20, 10, 0, 0,
             0, 0, 0, 0]

"""Directions"""
UP = 100
LEFT = 101
DOWN = 102
RIGHT = 103


class Cords:
    """Cords class contains all the coordinates of the tiles"""
    cord11 = (167, 292)
    cord12 = (280, 289)
    cord13 = (389, 289)
    cord14 = (497, 289)
    cord21 = (172, 396)
    cord22 = (302, 395)
    cord23 = (391, 399)
    cord24 = (498, 401)
    cord31 = (142, 505)
    cord32 = (305, 582)
    cord33 = (384, 513)
    cord34 = (500, 506)
    cord41 = (206, 694)
    cord42 = (276, 618)
    cord43 = (388, 619)
    cord44 = (493, 619)

    cordArray = [cord11, cord12, cord13, cord14,
                 cord21, cord22, cord23, cord24,
                 cord31, cord32, cord33, cord34,
                 cord41, cord42, cord43, cord44]


class Values:
    """class of greyscale values of existing tiles in the game"""
    empty = 195
    two = 229
    four = 225
    eight = 190
    sixteen = 172
    thirtyTwo = 157
    sixtyFour = 135
    oneTwentyEight = 205
    twoFiftySix = 201
    fiveOneTwo = 197
    oneZeroTwoFour = 193
    twoZeroFourEight = 189

    valueArray = [empty, two, four, eight, sixteen, thirtyTwo, sixtyFour
        , oneTwentyEight, twoFiftySix, fiveOneTwo, oneZeroTwoFour, twoZeroFourEight]


def getGrid():
    """gets a scrrenshot of a grid, transforms it to greyscale then gets the values of the tiles"""
    image = ImageGrab.grab()
    # image.show()

    # Transform rgb image to Gray scale:
    # it's simply reducing complexity: from a 3D pixel value (R,G,B) to a 1D value
    gray_image = ImageOps.grayscale(image)

    # gets the greyscale values of pixels at any coord
    for index, cord in enumerate(Cords.cordArray):
        pixel = gray_image.getpixel(cord)
        print(cord, pixel)

        pos = Values.valueArray.index(pixel)

        if pos == 0:
            currentGrid[index] = 0
        else:
            currentGrid[index] = int(math.pow(2, pos))


def printGrid(grid):
    """prints a grid"""
    for i in range(len(grid)):
        if i % 4 == 0:
            print('[', grid[i], grid[i + 1], grid[i + 2], grid[i + 3], ']')


def getPixelPosition():
    # get the mouse pointer coordinate on the screen.
    time.sleep(1)
    print(pyautogui.position())


def swipeRow(row):
    """swipes the tiles to the left in a row, sums identical tiles"""
    temp = [0, 0, 0, 0]
    prev = -1
    i = 0
    for element in row:
        if element != 0:
            if prev == -1:
                prev = element
                temp[i] = element
                i += 1
            elif prev == element:
                temp[i - 1] = prev * 2
                prev = -1
            else:
                prev = element
                temp[i] = element
                i += 1
    return temp


def getNextGrid(grid, move):
    """guesses the next grid using a move (up, down, left, right)"""
    temp = [0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0]

    if move == UP:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4 * j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i + 4 * j] = val

    elif move == LEFT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[4 * i + j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[4 * i + j] = val

    elif move == DOWN:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4 * (3 - j)])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i + 4 * (3 - j)] = val

    elif move == RIGHT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[4 * i + 3 - j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[4 * i + 3 - j] = val

    return temp


def getScore(grid):
    """Calculates the score of the grid"""
    score = 0
    for i in range(4):
        for j in range(4):
            score += grid[4 * i + j] * scoreGrid[4 * i + j]
    return score


def isMoveValid(grid, move):
    if getNextGrid(grid, move) == currentGrid:
        return False
    else:
        return True


# TODO: make a better function getBestMove with deepness level
def getBestMove(grid):
    firstGridUp = getNextGrid(grid, UP)
    scoreUp = getScore(firstGridUp) + getSecondBestMove(firstGridUp)
    firstGridDown = getNextGrid(grid, DOWN)
    scoreDown = getScore(firstGridDown) + getSecondBestMove(firstGridDown)
    firstGridLeft = getNextGrid(grid, LEFT)
    scoreLeft = getScore(firstGridLeft) + getSecondBestMove(firstGridLeft)
    firstGridRight = getNextGrid(grid, RIGHT)
    scoreRight = getScore(firstGridRight) + getSecondBestMove(firstGridRight)

    if not isMoveValid(currentGrid, UP):
        scoreUp = 0
    if not isMoveValid(currentGrid, DOWN):
        scoreDown = 0
    if not isMoveValid(currentGrid, LEFT):
        scoreLeft = 0
    if not isMoveValid(currentGrid, RIGHT):
        scoreRight = 0

    bestScore = max(scoreDown, scoreUp, scoreLeft, scoreRight)

    if scoreUp == bestScore:
        print('up')
        return UP
    elif scoreDown == bestScore:
        print('down')
        return DOWN
    elif scoreLeft == bestScore:
        print('left')
        return LEFT
    else:
        print('right')
        return RIGHT


def getSecondBestMove(grid):
    secondGridUp = getNextGrid(grid, UP)
    scoreUp = getScore(secondGridUp) + getThirdBestMove(secondGridUp)
    secondGridDown = getNextGrid(grid, DOWN)
    scoreDown = getScore(secondGridDown) + getThirdBestMove(secondGridDown)
    secondGridLeft = getNextGrid(grid, LEFT)
    scoreLeft = getScore(secondGridLeft) + getThirdBestMove(secondGridLeft)
    secondGridRight = getNextGrid(grid, RIGHT)
    scoreRight = getScore(secondGridRight) + getThirdBestMove(secondGridRight)

    bestScore = max(scoreDown, scoreUp, scoreLeft, scoreRight)

    return bestScore


def getThirdBestMove(grid):
    thirdGridUp = getNextGrid(grid, UP)
    scoreUp = getScore(thirdGridUp) + getFourthBestMove(thirdGridUp)
    thirdGridDown = getNextGrid(grid, DOWN)
    scoreDown = getScore(thirdGridDown) + getFourthBestMove(thirdGridDown)
    thirdGridLeft = getNextGrid(grid, LEFT)
    scoreLeft = getScore(thirdGridLeft) + getFourthBestMove(thirdGridLeft)
    thirdGridRight = getNextGrid(grid, RIGHT)
    scoreRight = getScore(thirdGridRight) + getFourthBestMove(thirdGridRight)

    bestScore = max(scoreDown, scoreUp, scoreLeft, scoreRight)

    return bestScore


def getFourthBestMove(grid):
    fourthGridUp = getNextGrid(grid, UP)
    scoreUp = getScore(fourthGridUp)
    fourthGridDown = getNextGrid(grid, DOWN)
    scoreDown = getScore(fourthGridDown)
    fourthGridLeft = getNextGrid(grid, LEFT)
    scoreLeft = getScore(fourthGridLeft)
    fourthGridRight = getNextGrid(grid, RIGHT)
    scoreRight = getScore(fourthGridRight)

    bestScore = max(scoreDown, scoreUp, scoreLeft, scoreRight)

    return bestScore


def performMOve(move):
    if move == UP:
        pyautogui.keyDown('up')
        time.sleep(0.1)
        pyautogui.keyUp('up')
    elif move == DOWN:
        pyautogui.keyDown('down')
        time.sleep(0.1)
        pyautogui.keyUp('down')
    elif move == LEFT:
        pyautogui.keyDown('left')
        time.sleep(0.1)
        pyautogui.keyUp('left')
    else:
        pyautogui.keyDown('right')
        time.sleep(0.1)
        pyautogui.keyUp('right')


def main():
    time.sleep(3)
    while True:
        getGrid()
        performMOve(getBestMove(currentGrid))
        time.sleep(0.1)


if __name__ == '__main__':
    main()
    # image = ImageGrab.grab()
    # # image.show()
    # gray_image = ImageOps.grayscale(image)
    # pixel = gray_image.getpixel(Cords.cord12)
    # print(pixel)

    # getPixelPosition()
