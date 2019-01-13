import math

# global variables
board = []
currPos = 0  # convert xy coordinates to 1 d by y*100+x
weight = 0  # must be less than 100
packages = []
moves = []
remainingPackages = 0
totalPackages = 0


def moveToCoor(x, y, addMoves):  # if want to change global variable moves enter 1
    global moves
    global currPos
    accumMoves = []
    # first convert current position to x,y
    currX, currY = convertIndexToCoordinate(currPos)
    # find the coordinate differences
    dx = x - currX
    dy = y - currY
    # print "dy:", dy
    tempX = currX
    tempY = currY

    if(dx >= 0):
        # horiz = 1 for right, -1 for left (if horizontally abve stored as 1)
        horiz = 1
    else:
        horiz = -1  # move left

    if (dy >= 0):
        vert = 1  # vert = 1 -> up, else down
    else:
        vert = -1

    dx = abs(dx)
    dy = abs(dy)
    # first need to find diagonal travel
    diagCounter = 0
    while (dx > 0 and dy > 0):
        diagCounter = diagCounter + 1
        dy = dy - 1
        dx = dx - 1

    # the remining dy or dx value will be the amount  o f mov es  the r obo t  has  to   take in a  direct io n de fi ned in vert or horiz

    # find index of moves
    while (diagCounter != 0):
        tempX = tempX + horiz
        tempY = tempY + vert
        accumMoves.append('move ' + str(tempX) + ' ' + str(tempY))
        diagCounter = diagCounter - 1
    while (dy > 0):
        tempY = tempY + vert
        accumMoves.append('move ' + str(tempX) + ' ' + str(tempY))
        dy = dy - 1
    while (dx != 0):
        tempX = tempX + horiz
        accumMoves.append('move ' + str(tempX) + ' ' + str(tempY))
        dx = dx - 1
    if (addMoves == 1):
        moves = moves + accumMoves
        print "tempX:", tempX
        print "tempY:", tempY
        currPos = convertCoordinateToIndex(tempX, tempY)

    return accumMoves

# Takes a file, such as "Part2a.in"
# Returns list data structure
# At each square, we have [quantity, productID, weight, obstacle]
# Defaults to [0,-1,0,False] if not occupied


def encode(filename):
    out = []
    for i in range(10000):
        out.append([0, -1, 0, False])
    with open(filename) as data:
        fline = data.readline()
        totalPackages = int(fline.split(", ")[1])
        for line in data:
            line = line.strip().strip('()').split(',')
            line = map(float, line)
            line = map(round, line)
            line = map(int, line)
            idx = convertCoordinateToIndex(line[0], line[1])
            out[idx][0] += 1
            out[idx][1] = line[2]
            out[idx][2] = line[3]
            out[idx][3] = False
    return out, totalPackages


def pickup(x, y, board):
    global weight
    global packages
    global moves
    index = convertCoordinateToIndex(x, y)
    weight = weight + board[index][2]*board[index][0]
    for i in range(0, board[index][0]):
        moves.append('pick ' + str(board[index][1]))
    packages.append(board[index][1])
    board[index] = [0, -1, 0, False]
    return moves


def drop():
    global packages
    global moves
    global weight
    while (packages != []):
        moves.append('drop ' + str(packages.pop(0)))
    weight = 0
    return moves

# Take an coordinate and return an index


def convertCoordinateToIndex(x, y):
    return (y * 100) + x


# Convert an index to a coordinate and return the coordinate in a list
def convertIndexToCoordinate(index):
    x = index % 100
    y = index / 100
    return [x, y]


# Given the current index, return the index of the closest package
def findClosestPackage(currentIndex, board):
    packagePositions = []
    for i in range(0, len(board)):
        quantity = board[i][0]
        if quantity != 0:
            packagePositions.append(i)
    for i in range(0, len(packagePositions)):
        index = packagePositions[i]
        coordinates = convertIndexToCoordinate(index)
        packagePositions[i] = coordinates
    closestPackageCoordinates = [None, None]
    leastMoves = None
    if len(packagePositions) == 0:
        return False
    for i in range(0, len(packagePositions)):
        x = packagePositions[i][0]
        y = packagePositions[i][1]
        moves = moveToCoor(x, y, 0)
        numberOfMoves = len(moves)
        # Handle first iteration
        if leastMoves == None:
            leastMoves = numberOfMoves
            closestPackageCoordinates = [x, y]
        elif moves < leastMoves:
            leastMoves = moves
            closestPackageCoordinates = [x, y]
    closestX = closestPackageCoordinates[0]
    closestY = closestPackageCoordinates[1]
    closestPackageIndex = convertCoordinateToIndex(closestX, closestY)
    return closestPackageIndex


# check if exceed 100kg with current and the addition of next package
# if True = exceeds 100kg; False = less than/equal to 100kg
def weight_checker(weight, board):
    next_package_index = findClosestPackage(currPos, board)
    next_package = board[next_package_index]
    next_weight = next_package[2]
    total_weight = weight + next_weight
    if total_weight > 100:
        return True
    elif total_weight <= 100:
        return False


def main_func(filename):
    i = 0
    board, totalPackages = encode(filename)
    while (i < totalPackages):
        # print i
        next_pos = findClosestPackage(currPos, board)
        is_overweight = weight_checker(weight, board)
        if is_overweight == True:
            moveToCoor(0, 0, 1)
            drop()
            print weight
        else:
            #print board
            moves = convertIndexToCoordinate(next_pos)
            move_1 = moves[0]
            move_2 = moves[1]
            print moves
            moveToCoor(move_1, move_2, 1)
            pickup(move_1, move_2, board)
            i = i + 1


# Write moves to output file
def outputMovesToFile(filename):
    f = open(filename, 'w+')
    for instruction in moves:
        f.write(instruction + '\n')

    # print moves

    # Tests
    # print convertCoordinateToIndex(0, 0)
    # print convertCoordinateToIndex(99, 0)
    # print convertCoordinateToIndex(0, 99)
    # print convertCoordinateToIndex(99, 99)
    # print convertCoordinateToIndex(50, 50)

    # print convertIndexToCoordinate(0)
    # print convertIndexToCoordinate(99)
    # print convertIndexToCoordinate(9999)


main_func('2a.in')
outputMovesToFile('2a.out')
main_func('2b.in')
outputMovesToFile('2b.out')
main_func('2c.in')
outputMovesToFile('2c.out')
