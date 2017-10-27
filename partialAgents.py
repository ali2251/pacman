# partialAgent.py
# parsons/15-oct-2017
#
# Version 1
#
# The starting point for CW1.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

#Signatures of the class and Functions not altered
class PartialAgent(Agent):

        # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
         #corner : To record the corner currently trying to visitedCorners
         self.corner = 0,0
         #list of visited Corners
         self.visitedCorners = []
         #list of corner positions which pacman can reach (ie. 1,1 instead of 0,0)
         self.rechableCorners = []
         #To avoid having to recompute corners, since the environment is static, only need to compute once at start
         self.check = False
         #all food locations not yet eaten
         self.allFood = []
         #the maximum x and y coordinates on the grid - the grid must always follow the same semantics for this to work.
         self.maxX = 1000
         self.maxY = 1000
         self.minX = 0
         self.minY = 0
         #To Store last direction used
         self.last = Directions.STOP



    def final(self, state):
         self.corner = 0,0
         self.visitedCorners = []
         self.rechableCorners = []
         self.check = False
         self.allFood = []
         self.last = Directions.STOP
         self.maxX = 1000
         self.maxY = 1000
         self.minX = 0
         self.minY = 0




    def getAction(self, state):

        #To find the nearest corner given the current position and all corners
        def findNearestCorner(pacmanPos, corners):
            #value to minimum distance
            mindist = 100000;
            #corner to return
            corner = 1,0
            #has pacman visited all the corners, if Yes then corner is the food,
            # it already knows where the food is on the board because of allFood
            if len(self.visitedCorners) == 4:
                for food in self.allFood:
                    distance = util.manhattanDistance(pacman,food)
                    if(distance < value):
                        self.corner = food
                return self.corner

            #If havent visited all corners then visit closest corner
            for c in corners:
                if  c not in self.visitedCorners:
                    temp = util.manhattanDistance(pacman,c)
                    if temp < mindist and c not in self.visitedCorners:
                        mindist = temp
                        corner = c
            return corner

        #Function to convert corners from api to rechableCorners so they can be used as targets
        def rechableCorner(corners):
            #the array to return
            toReturn = []
            #Look for every corner and add/subtract from x and y to make the corners rechable
            for i in range(len(corners)):

                if(corners[i] == (0,0)):
                    #will make the corner 1,1 essentially
                    self.minX = corners[i][0]+1
                    self.minY = corners[i][1]+1
                    toReturn.append((corners[i][0]+1,corners[i][1]+1))
                elif(corners[i][1] == 0):
                    self.maxX = corners[i][0]-1
                    toReturn.append((corners[i][0]-1, corners[i][1]+1))
                elif(corners[i][0] == 0):
                    self.maxY = corners[i][1]-1
                    toReturn.append((corners[i][0]+1, corners[i][1]-1))
                else:
                    toReturn.append((corners[i][0]-1,corners[i][1]-1))
            return toReturn;

        #method to return the nearest corner, Its used to encapsulate conversion of the corner
        def getNearestCorner(pacman,corners):
            cornersAmended = rechableCorner(corners)
            if(self.check == False):
                self.rechableCorners = cornersAmended
                self.check = True
            return findNearestCorner(pacman, cornersAmended)

        #utility function to get the direction given a coordinate
        def getDirection(pacman, dest, legal):

            if(pacman[1] > dest[1]):
                if (Directions.SOUTH in legal):
                    return Directions.SOUTH
                else:
                    if self.last in legal and self.last != Directions.STOP:
                        return api.makeMove(self.last, legal)
                    else:
                        self.last = random.choice(legal)
                        return api.makeMove(self.last, legal)
            else:

                if (Directions.NORTH in legal):
                    return Directions.NORTH
                else:

                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

        #To check wheteher a position is the goal position - used in BFS
        def isGoal(goalPosition, currentPos):
            if goalPosition == currentPos:
                return True
            else:
                return False

        #Method which returns the children/rechable-positions given the position.
        def getChildren(position, walls):

            #check for legality
            if position[0] < 0 or position[1] < 0 or position[0] > self.maxX or position[1] > self.maxY:
                return []
            children = [((position[0]+1, position[1]), Directions.EAST), ((position[0]-1, position[1]), Directions.WEST),
            ((position[0], position[1]+1), Directions.NORTH ), ((position[0], position[1]-1), Directions.SOUTH ) ]

            #remove the illegal ones
            for c in children:

                if c[0] in walls or c[0][0] > self.maxX or c[0][0] < self.minX or c[0][1] > self.maxY or c[0][1] < self.minY:
                    children.remove(c)

            for c in children:
                if c[0][0] < 0 or c[0][1] < 0 or c[0] in walls:
                    children.remove(c)
            return children

        #construct path once the goal has been reached
        def construct_path(state, mapOfstates):
              action_list = []

              while True:
                coordinates = mapOfstates[state]
                if coordinates[0] != None:
                  state = coordinates[0]
                  action = coordinates[1]
                  action_list.append(action)
                else:
                  break

              return action_list

        #the definition of the bfs search
        def breadth_first_search(currentPos, goalPosition, walls):
          # a FIFO open_set
          import Queue
          open_set = Queue.Queue()
          openset = []
          # an empty set to maintain visited nodes
          closed_set = set()
          # a dictionary to maintain mapOfLocations information (used for path formation)
          mapOfLocations = dict()  # key -> (parent state, action to reach child)


          start = currentPos
          mapOfLocations[start] = (None, None)
          open_set.put(start)
          openset.append(start)


          while not open_set.empty():

            parent_state = open_set.get()
            openset.pop(0)

            #check if already reached the goal
            if isGoal(goalPosition, parent_state):
                    path = construct_path(parent_state, mapOfLocations)
                    #return the reverse of the path, using slicing to reverse the list
                    return path[::-1]
            for (child_state, action) in getChildren(parent_state, walls):
              #look at each individual child
              if child_state in closed_set:
                continue

              if child_state not in openset:
                mapOfLocations[child_state] = (parent_state, action)
                open_set.put(child_state)
                openset.append(child_state)

            #finished looking at the state
            closed_set.add(parent_state)

        #method which handles what to do when ghost is seen, just like a human it will run from it
        def runFromGhosts():
            value = 100000;
            for i in range(len(ghostArray)):
                temp = util.manhattanDistance(pacman,ghostArray[i])
                if temp < value:
                    value = temp;
                    nearestGhost = ghostArray[i]

            distance = util.manhattanDistance(pacman,nearestGhost)

            x = nearestGhost[0]
            y = nearestGhost[1]
            x1 = pacman[0]
            y1 = pacman[1]

            #check which way the ghost is and go opposite way
            if (x > x1 and y > y1):
                if south in legal:
                    return api.makeMove(south, legal)
                else:
                    if west in legal:
                        return api.makeMove(west, legal)
                    else:
                        pick = random.choice(legal)
                        return api.makeMove(pick, legal)
            elif ( x < x1 and y > y1):
                if south in legal:
                    return api.makeMove(south, legal)
                else:
                    if east in legal:
                        return api.makeMove(east, legal)
                    else:

                        pick = random.choice(legal)
                        return api.makeMove(pick, legal)
            elif (x < x1 and y < y1):
                if north in legal:
                    return api.makeMove(north, legal)
                else:
                    if east in legal:
                        return api.makeMove(east, legal)
                    else:
                        pick = random.choice(legal)
                        return api.makeMove(pick, legal)
            elif (x > x1 and y < y1):
                if west in legal:
                    return api.makeMove(west, legal)
                else:
                    if north in legal:
                        return api.makeMove(north, legal)
                    else:
                        pick = random.choice(legal)
                        return api.makeMove(pick, legal)

            elif x1 > x:
                if east in legal:
                    return api.makeMove(east, legal)
                else:
                    temp = legal
                    if west in temp:
                        temp.remove(west)
                    if(len(temp) == 0):
                        if west in legal:
                            return api.makeMove(west, legal)
                        else:
                            return api.makeMove(Directions.STOP, legal)
                    else:
                        pick = random.choice(temp)
                        return api.makeMove(pick, temp)
            elif x > x1:
                if west in legal:
                    return api.makeMove(west, legal)
                else:
                    temp = legal
                    if east in temp:
                        temp.remove(east)
                    if(len(temp) == 0):
                        if east in legal:
                            return api.makeMove(east, legal)
                        else:
                            return api.makeMove(Directions.STOP, legal)
                    else:
                        pick = random.choice(temp)
                        return api.makeMove(pick, temp)
            elif y1 > y:
                if north in legal:
                    return api.makeMove(north, legal)
                else:
                    temp = legal
                    if south in temp:
                        temp.remove(south)
                    if(len(temp) == 0):
                        if south in legal:
                            return api.makeMove(south, legal)
                        else:
                            return api.makeMove(Directions.STOP, legal)
                    else:
                        pick = random.choice(temp)
                        return api.makeMove(pick, temp)
            elif y > y1:
                if south in legal:
                    return api.makeMove(south, legal)
                else:
                    temp = legal
                    if north in temp:
                        temp.remove(north)
                    if(len(temp) == 0):
                        if north in legal:
                            return api.makeMove(north, legal)
                        else:
                            return api.makeMove(Directions.STOP, legal)
                    else:
                        pick = random.choice(temp)
                        return api.makeMove(pick, temp)
            else:
                pick = random.choice(legal)
                return api.makeMove(pick, legal)

        #the method which calls the BFS and decides whether to visit corners or food depending on whether corners have already been visited
        def getToCornersOrFood():
            # if all corners are visited then visit the food which was left beforehand
            if(len(self.visitedCorners) > 4 ):
                value  = 1000000;
                for food in self.allFood:
                    distance = util.manhattanDistance(pacman,food)
                    if(distance < value):
                        self.corner = food

            #find the path toward the corner or food
            path = breadth_first_search(pacman, self.corner, walls)
            if(pacman == self.corner):
                self.visitedCorners.append(self.corner)
                self.corner = getNearestCorner(pacman, corners)
                path = breadth_first_search(pacman, self.corner, walls)
                if path:
                    return path.pop(0)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

            else:
                if path:
                    return path.pop(0)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

        #Basic hungry agent which eats the food when it can
        def eatFood():
            food = (0,1)
            value = 100000
            #find closest food
            for i in range(len(theFood)):
                temp = util.manhattanDistance(pacman,theFood[i])
                if temp < value:
                    value = temp;
                    food = theFood[i]

            distance = util.manhattanDistance(pacman,food)

            x = food[0]
            y = food[1]
            x1 = pacman[0]
            y1 = pacman[1]

            #check the best direction to go
            if(pacman in self.rechableCorners):
                self.visitedCorners.append(pacman)

            if x1 > x:
                if west in legal:
                    return api.makeMove(west, legal)
            elif x > x1:
                if east in legal:
                    return api.makeMove(east, legal)
            elif y1 > y:
                if south in legal:
                    return api.makeMove(south, legal)
            elif y > y1:
                if north in legal:
                    return api.makeMove(north, legal)
            else:
                #if cant find anything then go random from legal moves
                pick = random.choice(legal)
                return api.makeMove(pick, legal)


        #main function which decides which agent to use
        def getNextDirection(pacman, corner, walls, legal, theFood, ghostArray):
            #global variables
            distance = util.manhattanDistance(pacman,corner)
            corners = api.corners(state)
            #check if there are any ghosts
            if len(ghostArray) > 0:
                return runFromGhosts()
            else:
                #check if any food can be eaten
                if(len(theFood) == 0):
                    return getToCornersOrFood()
                else:
                    #found food, hence eat it
                    return eatFood()



        #getting all the data from the api
        walls = api.walls(state)
        corners = api.corners(state)
        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theFood = api.food(state)
        west = Directions.WEST
        east = Directions.EAST
        south = Directions.SOUTH
        north = Directions.NORTH
        ghostArray = api.ghosts(state);
        value = 100000

        #remove stop from legal
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        #keep a track of all food ever seen
        for f in theFood:
            if(f not in self.allFood):
                self.allFood.append(f)

        #remove all eaten food
        if(pacman in  self.allFood):
            self.allFood.remove(pacman)

        #only recalculate the corner if all 4 havent been visited, all rectangles and squares have maximum of 4 corners
        if (len(self.visitedCorners)  < 5):
            self.corner = getNearestCorner(pacman, corners)
        #get the direction to go from getNextDirection
        direction = getNextDirection(pacman, self.corner, walls, legal, theFood, ghostArray)
        #return with a move
        return api.makeMove(direction, legal)
