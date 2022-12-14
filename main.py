import copy

class Node: #Creating a Node class that contains the current puzzle board state, the parent puzzle state, h score, and g score.
    def __init__(self, currentPuzzleState, h, g, previousMove):
        self.currentPuzzleState = currentPuzzleState
        self.h = h #h score will be found depending on type of heursitc, heurstic function will be called to do calculation
        self.g = g # g = parent depth + 1
        self.previousMove = previousMove
    
def empty(nodes): #returns true if nodes queue is empty
    if not nodes: 
        return True
    else:
        return False

def removeFront(nodes): #removes first element (node) of nodes and returns removed node
    removedNode = nodes.pop(0)
    return removedNode

def goalState(currentNodeState): #returns true if the currentNodeState (first element in nodes) is equivalent to goal
    if currentNodeState == puzzleGoalState:
        return True
    else:
        return False

def findCoordinates(puzzleState, value): #finds the location of specified value in puzzle
    for x in range(3): #cycle through puzzle, one row at a time
        for y in range(3): #cycle through every element (column) of the current row
            if puzzleState[x][y] == value:
                return (x,y) #returns coordinates of specified value

def isDuplicateCheck(puzzleState, listNodes): #check to see if puzzleState already exists in passed in node list
    for g in range(len(listNodes)):
        if puzzleState == listNodes[g].currentPuzzleState:
            return True
    return False

def expand(node, problemOperators, expanded):
    blankTile = findCoordinates(node.currentPuzzleState, 0) #coordinates of 0 (blank tile) 
    x, y = blankTile[0], blankTile[1] # x -> column # of blank tile, y -> row # of blank tile

    moves = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)] #up, right, down, left
    children = [] #array that will hold all children nodes of the current node
    skipMove = -1 #impossible for move to be -1, update later on

    if node.g != 0:
        previousMove = problemOperators.index(node.previousMove) #find index of the previous move in operators list

        if previousMove == 2: #finding the opposite move to avoid repeating parent puzzle state
            skipMove = 0
        elif previousMove == 3:
            skipMove = 1
        else:
            skipMove = previousMove + 2
    

    for i in range(len(moves)): #cycle through every potential move
        nodeStateCopy = copy.deepcopy(node.currentPuzzleState) #create temp of puzzle board state
        #create deep copy because dont want original node to update
        a, b = moves[i][0], moves[i][1] # a -> column # of tile that is moving, b -> row # of tile that is moving

        if a < 0 or a > 2 or b < 0 or b > 2: #if move is illegal, move on
            continue
        else:
            #swap selected tile (at a, b) and blank tile
            nodeStateCopy[x][y], nodeStateCopy[a][b] = nodeStateCopy[a][b], nodeStateCopy[x][y]

            #print("Child Expanded: ", nodeStateCopy)

            if isDuplicateCheck(nodeStateCopy, expanded): #check to see if puzzle state has already been expanded
                continue
            elif skipMove == i: #move on to avoid repeating parent state
                continue
            else:
                #add temp node (with switched tiles) to children array
                children.append(Node(nodeStateCopy, 0, (node.g + 1), problemOperators[i]))
    return children

def uniformCostSearchQueue(nodes, children):    
    for i in range(len(children)):   
        if isDuplicateCheck(children[i], nodes): #check if child already exists in nodes
            continue
        else:
            children[i].h = 0 #uniform cost search is A* w/ h being hardcoded as 0
            nodes.append(children[i]) #adding all children to nodes

def misplacedTileQueue(nodes, children):
    for i in range(len(children)):
        if isDuplicateCheck(children[i], nodes): #check if child already exists in nodes
            continue
        else:
            children[i].h = misplacedTileH(children[i].currentPuzzleState) #setting child node h using misplaced tile heuristic
            nodes.append(children[i]) #adding all children to nodes

def manhattanDistanceQueue(nodes, children):
    for i in range(len(children)):
        if isDuplicateCheck(children[i], nodes):
            continue
        else:
            children[i].h = manhattanH(children[i].currentPuzzleState) #setting child node h using manhattan heuristic
            nodes.append(children[i]) #adding all children to nodes

def misplacedTileH(currentPuzzleState): #return h(n) of current puzzle state
    misplacedTileH = 0
    
    for x in range(len(currentPuzzleState)):
            for y in range(len(currentPuzzleState[0])):
                if currentPuzzleState[x][y] == 0: #do not count the blank tile
                    continue
                elif currentPuzzleState[x][y] != puzzleGoalState[x][y]: #check to see if tile in current puzzle state is the correct tile (compared to goal state)
                    misplacedTileH += 1 #if tile is misplaced add to h
    
    return misplacedTileH

def manhattanH(currentPuzzleState):
    manhattanH = 0

    for x in range(len(currentPuzzleState)):
            for y in range(len(currentPuzzleState[0])):
                if currentPuzzleState[x][y] == 0: #do not count the blank tile
                    continue
                elif currentPuzzleState[x][y] != puzzleGoalState[x][y]: #check to see if tile in current puzzle state is the correct tile (compared to goal state)
                    correctTilePositon = findCoordinates(puzzleGoalState, currentPuzzleState[x][y])

                    xDistance = abs(correctTilePositon[0] - x) #horizontal distance from correct position
                    yDistance = abs(correctTilePositon[1] - y) #vertical distance from correct position

                    manhattanH += xDistance + yDistance #summing total distance of how far tile is
    return manhattanH

def genSearchAlg(problem, typeOfHueristic): #problem operator is type of heuristic search
    keepGoing = True
    problemOperators = ['up', 'right', 'down', 'left'] #all possible moves in puzzle
    expanded = []
    nodeExpandedCount = 0

    firstNode = Node(problem, 0, 0, None)
    nodes = [firstNode]
    currentNodesMax = 1

    while keepGoing: #loop will continue until goal state is found or all tested every possible node
        if empty(nodes):
            keepGoing = False
            print("failure") #proved that there is no solution
            return
        node = removeFront(nodes)
        expanded.append(node) #keep track of the nodes already expanded
        nodeExpandedCount += 1

        if (len(nodes) > currentNodesMax):
            currentNodesMax = len(nodes)

        print("The best state to expand with g(n) = " + str(node.g) + " and h(n) = " + str(node.h) + " is...")
        print(node.currentPuzzleState)

        if goalState(node.currentPuzzleState): #found solution!!!
            print("found solution")
            print("Solution depth was " + str(node.g))
            print("Number of nodes expanded: " + str(nodeExpandedCount))
            print("Max Queue Size: " + str(currentNodesMax))
            return
        if typeOfHueristic == 0: #uniform cost search
            uniformCostSearchQueue(nodes, expand(node, problemOperators, expanded))
        elif typeOfHueristic == 1: #A* w/ Misplaced Tile heuristic
            misplacedTileQueue(nodes, expand(node, problemOperators, expanded))
        elif typeOfHueristic == 2: #A* w/ Manhattan Distance heuristic
            manhattanDistanceQueue(nodes, expand(node, problemOperators, expanded))
        nodes.sort(key=lambda x: x.g + x.h) #sorting by g+h, which is f

if __name__ == "__main__":
    puzzleGoalState = [[1,2,3],[4,5,6],[7,8,0]] #only one possible goal state for 8 puzzle
    
    algorithmSelection = input("Please select the algorithm that you would to use.\n (1) for Uniform Cost Search\n (2) for Misplaced Tile\n (3) for Manhattan Distance\n")

    print("Now enter the puzzle one row at a time. Seperate numbers with a space. Use 0 to represent the blank tile")
    firstRowString = raw_input("Enter the first row: ")
    secondRowString = raw_input("Enter the second row: ")
    thirdRowString = raw_input("Enter the third row: ")
    
    #splitting up the string by spaces
    firstRowList = firstRowString.split(' ')
    secondRowList = secondRowString.split(' ')
    thirdRowList = thirdRowString.split(' ')

    #changing list to list of int
    row1numList = [eval(i) for i in firstRowList]
    row2numList = [eval(i) for i in secondRowList]
    row3numList = [eval(i) for i in thirdRowList]

    puzzle = [row1numList, row2numList, row3numList]
    
    #algorithmSelection = 2
    #puzzle = [[1,3,2],[4,5,6],[7,8,0]]

    genSearchAlg(puzzle, algorithmSelection)