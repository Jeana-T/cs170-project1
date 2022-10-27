class Node:
    def __init__(self, currentPuzzleState, parent, h, g):
        self.currentPuzzleState = currentPuzzleState
        self.parent = parent
        self.h = h
        self.g = g
    
def empty(nodes):
    if len(nodes) == 0: 
        return True
    else:
        return False

def removeFront(nodes):
    removedNode = nodes.pop(0)
    return removedNode

def h_of_n(currentState, nodes):
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

    firstNode = Node(problem, None, 0, 0)
    secondNode = Node([1,2,3], None, 0, 0)
    nodes = [firstNode, secondNode]

    while keepGoing:
        if empty(nodes):
            keepGoing = False
            return "failure"
        
        node = removeFront(nodes) #remove front of node

if __name__ == "__main__":
    testUserInput = [1,2,3,4,5,0,7,8,6]

    genSearchAlg(testUserInput, 1)
