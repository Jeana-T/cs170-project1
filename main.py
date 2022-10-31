import copy
import bisect

class Node: #Creating a Node class that contains the current puzzle board state, the parent puzzle state, h score, and g score.
    def __init__(self, currentPuzzleState, parent, h, g):
        self.currentPuzzleState = currentPuzzleState
        self.parent = parent #parent element will be used to avoid duplicating it when creating children states
        self.h = h #h score will be found depending on type of heursitc, heurstic function will be called to do calculation
        self.g = g # g = parent depth + 1
    
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

def findCoordinates(node, value): #finds the location of specified value in puzzle
    for x in range(3): #cycle through puzzle, one row at a time
        for y in range(3): #cycle through every element (column) of the current row
            if node.currentPuzzleState[x][y] == value:
                return (x,y) #returns coordinates of specified value

def expand(node, problemOperators):
    blankTile = findCoordinates(node, 0) #coordinates of 0 (blank tile) 
    x, y = blankTile[0], blankTile[1] # x -> column # of blank tile, y -> row # of blank tile

    moves = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)] #up, right, down, left (only possible moves in this puzzle)
    children = [] #array that will hold all children nodes of the current node

    for i in range(len(moves)): #cycle through every potential move
        nodeStateCopy = copy.deepcopy(node.currentPuzzleState) #create temp of puzzle board state
        #create deep copy because dont want original node to update
        a, b = moves[i][0], moves[i][1] # a -> column # of tile that is moving, b -> row # of tile that is moving

        if a < 0 or a > 2 or b < 0 or b > 2: #if move is illegal, move on
            continue
        else:
            #swap selected tile (at a, b) and blank tile
            nodeStateCopy[x][y], nodeStateCopy[a][b] = nodeStateCopy[a][b], nodeStateCopy[x][y]

            #add temp node (with switched tiles) to children array
            children.append(Node(nodeStateCopy, node.currentPuzzleState, node.g + 1, 0))
    return children

def uniformCostSearchQueue(nodes, children):    
    for i in range(len(children)):
        #bisect.insort(nodes, children[i])
        children[i].h = 0 #uniform cost search is A* w/ h being hardcoded as 0
        nodes.append(children[i]) #adding all children to nodes
        
    #sort nodes
    #nodes.sort(key=lambda x: x.g + x.h, reverse=True)

def misplacedTileQueue(nodes, children):
    for i in range(len(children)):
        #bisect.insort(nodes, children[i])
        children[i].h = misplacedTileH(children[i].currentPuzzleState)
        #nodes.append(children[i]) #adding all children to nodes

def manhattanDistanceQueue(nodes, children):
    for i in range(len(children)):
        #bisect.insort(nodes, children[i])
        #children[i].h = manhattanH(children[i].currentPuzzleState)
        manhattanH(children[i].currentPuzzleState)
        #nodes.append(children[i]) #adding all children to nodes

def misplacedTileH(currentPuzzleState): #return h(n) of current puzzle state
    h = 0
    
    for x in range(len(currentPuzzleState)):
            for y in range(len(currentPuzzleState[0])):
                if currentPuzzleState[x][y] == 0: #do not count the blank tile
                    continue
                elif currentPuzzleState[x][y] != puzzleGoalState[x][y]: #check to see if tile in current puzzle state is the correct tile (compared to goal state)
                    h += 1 #if tile is misplaced add to h
    
    return h

def manhattanH(currentPuzzleState):
    h = 0

    for x in range(len(currentPuzzleState)):
            for y in range(len(currentPuzzleState[0])):
                if currentPuzzleState[x][y] == 0: #do not count the blank tile
                    continue
                elif currentPuzzleState[x][y] != puzzleGoalState[x][y]: #check to see if tile in current puzzle state is the correct tile (compared to goal state)
                    correctTilePositon = findCoordinates(puzzleGoalState, currentPuzzleState[x][y])

                    xDistance = abs(correctTilePositon[0] - x)
                    yDistance = abs(correctTilePositon[1] - y)

                    h += xDistance + yDistance
    return h

def genSearchAlg(problem, typeOfHueristic): #problem operator is type of heuristic search
    keepGoing = True
    problemOperators = ['up', 'right', 'down', 'left']

    #firstNode = Node([1,2,3,4,5,6,7,8,0], None, 0, 0)
    firstNode = Node(problem, None, 0, 0)
    secondNode = Node([1,2,3], problem, 0, 0)
    nodes = [firstNode]

    while keepGoing: #loop will continue until goal state is found or all tested every possible node
        if empty(nodes):
            keepGoing = False
            return "failure" #proved that there is no solution
        
        node = removeFront(nodes)

        if goalState(node.currentPuzzleState):
            return "found solution" #return node

        if typeOfHueristic == 0: #uniform cost search
            print("uniform cost search")
            nodes = uniformCostSearchQueue(nodes, expand(node, problemOperators))
        elif typeOfHueristic == 1: #A* w/ Misplaced Tile heuristic
            print("A* w/ Misplaced Tile heuristic")
            nodes = misplacedTileQueue(nodes, expand(node, problemOperators))
        elif typeOfHueristic == 2: #A* w/ Manhattan Distance heuristic
            print("A* w/ Manhattan Distance heuristic")
            nodes = manhattanDistanceQueue(nodes, expand(node, problemOperators))

if __name__ == "__main__":
    puzzleGoalState = [[1,2,3],[4,5,6],[7,8,0]] #only one possible goal state for 8 puzzle
    
    testUserInput = [[1,2,3],[4,5,9],[7,8,0]]

    genSearchAlg(testUserInput, 2)
