#global variables
Table = {}
board = [0]*(100*100)
currentLoc = []
numOfRobo = 0


def read_file(filename):
    f = open(filename, 'r')
    contents = f.read()
    return contents


def string_to_list(contents):
    instructions = contents.split('\n')
    return instructions


def stringEleToListList(instructions):
    listList = []
    listList.append(instructions[0].split(', '))
    for i in instructions[1:len(instructions)-1]:
        element = i[1:len(i)-1]
        element = element.split(', ')
        listList.append(element)
    return listList


def stringToIntFloat(listList):  # ps naming is teriible lol -_-
    returnList = []
    for i in listList:
        counter = 0
        element = []
        for j in i:
            if (counter != 3):
                element.append(int(j))
            else:
                element.append(float(j))
            counter = counter + 1
        returnList.append(element)
    return returnList


def hashTable(hash, List):
    for i in (List[1:]):
        productNum = i[2]
        try:
            hash[productNum][1] = hash[productNum][1] + 1
        except:
            hash[productNum] = [i[3], 1, i[0], i[1]]
        # store elements in the hash table as (weight, quantity, locationx, locationy)
        # try:
        #    hash[i[2]][1] = hash[i[2]][1] + 1
        # except:
        #    hash[i[2]] = [i[2][3], 1, i[2][0], i[2][1]]

    return 0


def convertCoordinateToIndex(x, y):
    return (y * 100) + x

# Convert an index to a coordinate and return the coordinate in a list


def convertIndexToCoordinate(index):
    x = index % 100
    y = index / 100
    return [x, y]


raw_contents = read_file('4a.in')
instructions = string_to_list(raw_contents)
listList = stringEleToListList(instructions)
listList = stringToIntFloat(listList)
hashTable(Table, listList)


# in hash: (weight, quantity, locationx, locationy)

for i in Table:
    x = Table[i][2]
    y = Table[i][3]
    index = convertCoordinateToIndex(x, y)
    board[index] = i

numOfRobo = listList[0][0]

for i in range(0, numOfRobo):
    currentLoc.append([i, 0])

# board with the robot is all set up
# algorithm plan: keep all the robots stationary except (0,0)
# make sure the robot at (0,0) never travels to a (x,0)
