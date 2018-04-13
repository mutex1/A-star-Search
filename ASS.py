import sys
from heapq import heappush, heappop

class ASS():
    N = int()
    M = int()
    maze = list()
    start = list()
    end = list()

    # init variables
    def __init__(self):
        # read input file
        with open(sys.argv[1], 'r') as f:
            inputStrings = f.readlines()

        # set N, M
        mazeSize = inputStrings.pop(0)
        self.N, self.M = map(int, mazeSize.split())

        # set maze
        for row in inputStrings:
            localList1 = row.split()
            localList2 = list()
            for i in localList1:
                localList2.append(int(i))
            self.maze.append(localList2)

        # set start, end
        i = 0
        for row in self.maze:
            j = 0
            for node in row:
                if node == 3:
                    self.start.append(i)
                    self.start.append(j)
                if node == 4:
                    self.end.append([i, j])
                j += 1
            i += 1

    # get manhattan distance (Heuristic)
    def manhattan(self, start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    # get best path
    def getPath(self, node, parents, i):
        path = []
        while (node != None):
            path.append(node)
            node = parents[tuple(node)]
        return path

    # find near node
    def findNeighbors(self, node, visited):
        neighbors = []
        x, y = node[0], node[1]
        if (x + 1 < self.N) and (self.maze[x+1][y] != 1) and ([x+1, y] not in visited):
            neighbors.append([x+1, y])
        if (x > 0) and (self.maze[x-1][y] != 1) and ([x-1, y] not in visited):
            neighbors.append([x-1, y])
        if (y > 0) and (self.maze[x][y - 1] != 1) and ([x, y - 1] not in visited):
            neighbors.append([x, y - 1])
        if (y + 1 < self.M) and (self.maze[x][y + 1] != 1) and ([x, y + 1] not in visited):
            neighbors.append([x, y + 1])
        return neighbors

    # make output text format
    def makeOutput(self, length, time):
        output = str()
        for row in self.maze:
            for node in row:
                output += str(node)+' '
            output += '\n'
        output += '---\n'
        output += 'length='+str(length)+'\n'
        output += 'time='+str(time)+'\n'
        return output

    # run ASS
    def run(self):
        opened = list()
        closed = list()
        pathList = list()
        previous = dict()
        visited = list()
        lengthList = list()
        timeList = list()

        # set length & time to zero
        for i in range(len(self.end)):
            lengthList.append(0)
            timeList.append(0)

        # for each goal (main loop)
        for i in range(len(self.end)):
            # regard other goals as wall(1) and set i-th goal to the goal(4)
            for j in self.end:
                self.maze[j[0]][j[1]] = 1
            self.maze[self.end[i][0]][self.end[i][1]] = 4

            # begin ASS with start node
            previous[tuple(self.start)] = None
            heappush(opened, (self.manhattan(self.start, self.end[i]), self.start))
            timeList[i] += 1

            while (len(opened) > 0):
                # if reached to end node
                if (opened[0][1] == self.end[i]):
                    pathList.append(self.getPath(self.end[i], previous, i))
                    pathList[i].remove(self.start)
                    pathList[i].remove(self.end[i])
                    break

                # change to closed
                node = heappop(opened)[1]
                closed.append(node)

                #check visited
                if (node not in visited):
                    visited.append(node)

                # add a new node which locates near the node
                neighbors = self.findNeighbors(node, visited)
                for neighbor in neighbors:
                    if neighbor not in opened:
                        previous[tuple(neighbor)] = node
                        heappush(opened, (self.manhattan(neighbor, self.end[i])+len(self.getPath(neighbor, previous, i)), neighbor))
                        timeList[i] += 1


            # evaluate path length
            for point in pathList[i]:
                lengthList[i] += 1

            # init the variables to continue iteration
            opened = []
            closed = []
            previous = {}
            visited = []

        # find the shortest path among lengthList
        minLength = min(lengthList)
        bestGoalIndex = int(lengthList.index(minLength))

        # mark 5 on the path
        i = 0
        for path in pathList:
            if i == bestGoalIndex:
                for node in path:
                    self.maze[node[0]][node[1]] = 5
            i += 1
        i = 0

        # find search time of the path
        resultTime = int()
        for time in timeList:
            if i == bestGoalIndex:
                resultTime = time
            i += 1

        # mark 4 on the path to restore the original maze
        for goal in self.end:
            self.maze[goal[0]][goal[1]] = 4

        # make output and write
        output = self.makeOutput(minLength, resultTime)
        with open(sys.argv[2], 'w') as f:
            f.writelines(output)


if __name__ == '__main__':
    # run ASS
    ass=ASS()
    ass.run()