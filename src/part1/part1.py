def parse_input(lines):
    '''
    parses a header row: n_robots, n_items, n_obstacles
    items (x, y, product id, weight (in kg))
    followed by obstacles (x1, y1, x2, y2)
    '''
    header = next(lines)
    n_robots, n_items, n_obstacles = map(int, header.split(','))
    parsed_lines = [line.strip().strip('()').split(',') for line in lines]
    items = [(int(x), int(y), int(product_number), float(weight))
             for x, y, product_number, weight in parsed_lines[:n_items]]
    obstacles = [[int(coord) for coord in line]
                 for line in parsed_lines[n_items:]]

    print n_robots
    print items
    print obstacles
    return n_robots, items, obstacles


def read_file(filename):
    f = open(filename, 'r')
    contents = f.read()
    return contents


# for line in contents:
    '''
 with open('1a.in') as data:
         robots, items, obstacles = parse_input(data)
 '''


def string_to_list(contents):
    instructions = contents.split('\n')
    return instructions


def stringEleToListList(instructions):
    listList = []
    for i in instructions:
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
                j = j.strip()
                element.append(float(j))
            counter = counter + 1
        returnList.append(element)
    return returnList


def hashTable(hash, List):
    for i in (List):
        productNum = i[2]
        # store elements in the hash table as (weight, quantity, locationx, locationy)
        try:
            hash[productNum][1] = hash[productNum][1] + 1
        except:
            hash[productNum] = [i[3], 1, i[0], i[1]]


def main_func(file_in, file_out):
    Table = {}
    raw_contents = read_file(file_in)
    instructions = string_to_list(raw_contents)
    listList = stringEleToListList(instructions)
    listList = stringToIntFloat(listList)
    hashTable(Table, listList)

    # write content in hashTable

    # first need to sort product numbers
    productNumbers = []
    for i in Table:
        productNumbers.append(i)
    sorted(productNumbers)
    # write to file 1a.out
    f = open(file_out, "w+")
    for i in productNumbers:
        print "Product Number: " + str(i) + "; Weight: " + \
            str(Table[i][0]) + "; Qty: " + str(Table[i][1]) + \
            "; Location: (" + str(Table[i][2]) + "," + str(Table[i][3]) + ")"
        f.write("Product Number: " + str(i) + "; Weight: " + str(Table[i][0]) + "; Qty: " + str(
            Table[i][1]) + "; Location: (" + str(Table[i][2]) + "," + str(Table[i][3]) + ") \n")
    f.close()


main_func('1a.in', '1a.out')
main_func('1b.in', '1b.out')
main_func('1c.in', '1c.out')
