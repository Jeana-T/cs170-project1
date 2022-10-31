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
    puzzleGoalState = [1,2,3,4,5,6,7,8,0] #only one possible goal state for 8 puzzle
    
    if currentNodeState == puzzleGoalState:
        return True
    else:
        return False

def locatateBlankTile(node): #finds the location of 0 (blank tile) is in the puzzle
    for x in range(3): #cycle through puzzle, one row at a time
        for y in range(3): #cycle through every element (column) of the current row
            if node.currentPuzzleState[x][y] == 0:
                return (x,y) #returns 0 coordinates

def expand(node, problemOperators):
    blankTile = locatateBlankTile(node) #coordinates of 0 (blank tile) 
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
    for k in range(len(nodes)):
        print("before appending")
        print(nodes[k].currentPuzzleState)

    for i in range(len(children)):
        #bisect.insort(nodes, children[i])
        nodes.append(children[i])

    #nodes.sort(key=lambda x: x.g + x.h, reverse=True)

    for j in range(len(nodes)):
        print("after appending")
        print(nodes[j].currentPuzzleState)


def h(currentState, nodes):
    h = 0

    if():
        h = 0
    elif ():
        #manhattan distance
        for x in range(len(nodes)):
            for y in range(len(nodes[0])):
                if nodes[x][y] == 0:
                    continue
                elif nodes[x][y] != goalState[x][y]:
                    h += 1
    elif():
        for x in range(len(nodes)):
            for y in range(len(nodes[0])):
                if nodes[x][y] == 0:
                    continue
                elif nodes[x][y] != goalState[x][y]:
                    h += 1
    
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
        # elif typeOfHueristic == 1: #A* w/ Misplaced Tile heuristic
        #     print("A* w/ Misplaced Tile heuristic")
        #     nodes = queueingFunction(nodes, expand(node, problemOperators))
        # else: #A* w/ Manhattan Distance heuristic
        #     print("A* w/ Manhattan Distance heuristic")
        #     nodes = queueingFunction(nodes, expand(node, problemOperators))

if __name__ == "__main__":
    testUserInput = [[1,2,3],[4,5,9],[7,8,0]]

    genSearchAlg(testUserInput, 0)
