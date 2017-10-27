# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
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

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util


class CornerSmartAgent(Agent):
    def __init__(self):
         self.BL = False
         self.TL = False
         self.BR = False
         self.TR = False
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

    # Function run at end of games --- rest target positions so that
    # if we run multiple games using -n 5, they all have the agent
    # starting trying to go to BL.

    def final(self, state):
         self.BL = False
         self.TL = False
         self.BR = False
         self.TR = False
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

        def findNearestCorner(pacmanPos, corners):
            mindist = 100000;
            corner = 1,0
            if len(self.visitedCorners) == 4:
                print "====================== \n\n\n\n"
                for food in self.allFood:
                    distance = util.manhattanDistance(pacman,food)
                    if(distance < value):
                        self.corner = food
                return self.corner

            for c in corners:
                if  c not in self.visitedCorners:
                    temp = util.manhattanDistance(pacman,c)
                    if temp < mindist and c not in self.visitedCorners:
                        mindist = temp
                        corner = c
            return corner

        def rechableCorner(corners):
            toReturn = []
            for i in range(len(corners)):
                if(corners[i] == (0,0)):
                    print "here 1"
                    self.minX = corners[i][0]+1
                    self.minY = corners[i][1]+1
                    toReturn.append((corners[i][0]+1,corners[i][1]+1))
                elif(corners[i][1] == 0):
                    print "here 2 "
                    self.maxX = corners[i][0]-1
                    toReturn.append((corners[i][0]-1, corners[i][1]+1))
                elif(corners[i][0] == 0):
                    print "should be some"
                    self.maxY = corners[i][1]-1
                    toReturn.append((corners[i][0]+1, corners[i][1]-1))
                else:
                    print "here 2"
                    toReturn.append((corners[i][0]-1,corners[i][1]-1))
            return toReturn;

        def getNearestCorner(pacman,corners):
            cornersAmended = rechableCorner(corners)
            if(self.check == False):
                self.rechableCorners = cornersAmended
                self.check = True
            return findNearestCorner(pacman, cornersAmended)

        def getDirection(pacman, dest, legal):
            print "is here"
            if(pacman[1] > dest[1]):
                print "first if"
                if (Directions.SOUTH in legal):
                    return Directions.SOUTH
                else:
                    if self.last in legal and self.last != Directions.STOP:
                        return api.makeMove(self.last, legal)
                    else:
                        self.last = random.choice(legal)
                        return api.makeMove(self.last, legal)

            else:
                print "no clue"
                if (Directions.NORTH in legal):
                    return Directions.NORTH
                else:
                    print "coming here"
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)


        def getPath(pacman, destination, walls):
            print "in get path"

        def isGoal(goalPosition, currentPos):
            if goalPosition == currentPos:
                return True
            else:
                return False

        def getChildren(position, walls):

            #print "x min max , y min max", self.minX, self.maxX, " \n", self.minY, self.maxY

            if position[0] < 0 or position[1] < 0 or position[0] > self.maxX or position[1] > self.maxY:
                return []
            children = [((position[0]+1, position[1]), Directions.EAST), ((position[0]-1, position[1]), Directions.WEST),
            ((position[0], position[1]+1), Directions.NORTH ), ((position[0], position[1]-1), Directions.SOUTH ) ]

            for c in children:

                if c[0] in walls or c[0][0] > self.maxX or c[0][0] < self.minX or c[0][1] > self.maxY or c[0][1] < self.minY:
                    children.remove(c)

            for c in children:
                if c[0][0] < 0 or c[0][1] < 0 or c[0] in walls:
                    #print "here ============================ \n"
                    children.remove(c)
            return children


        def construct_path(state, meta):
              action_list = []
              print "meta", meta

              while True:
                row = meta[state]
                print "row", row
                if row[0] != None:
                  state = row[0]
                  action = row[1]
                  action_list.append(action)
                else:
                  break

              print "returnong action_list" , action_list
              return action_list



        def breadth_first_search(currentPos, goalPosition, walls):


          # a FIFO open_set
          import Queue
          open_set = Queue.Queue()
          openset = []
          # an empty set to maintain visited nodes
          closed_set = set()
          # a dictionary to maintain meta information (used for path formation)
          meta = dict()  # key -> (parent state, action to reach child)

          # initialize
          start = currentPos
          meta[start] = (None, None)
          open_set.put(start)
          openset.append(start)

          while not open_set.empty():

            parent_state = open_set.get()
            openset.pop(0)

            print "goal is: ", goalPosition, "  currentPos: " , currentPos

            if isGoal(goalPosition, parent_state):
                    path = construct_path(parent_state, meta)
                    print "reverse path is: ",
                    return path[::-1]
            for (child_state, action) in getChildren(parent_state, walls):

              if child_state in closed_set:
                continue

              if child_state not in openset:
                meta[child_state] = (parent_state, action)
                open_set.put(child_state)
                openset.append(child_state)


            closed_set.add(parent_state)









        def getOneStep(pacman, destination, walls):
            x, y = pacman
            x1,y1 = destination
            if x > x1:
                if (x-1,y) in walls:
                    #try going up
                    if (x,y+1) not in walls:
                        return Directions.NORTH
                    else:
                        if (x,y-1) not in walls:
                            return Directions.SOUTH
                        else:
                            return Directions.EAST
                else:
                    return Directions.WEST
            elif x1 > x:
                #go east
                if (x+1,y) in walls:
                    #try going up
                    if (x,y+1) not in walls:
                        return Directions.NORTH
                    else:
                        if (x,y-1) not in walls:
                            return Directions.SOUTH
                        else:
                            return Directions.WEST
                else:
                    return Directions.EAST
            elif y > y1:
                #come down
                if (x,y-1) in walls:
                    #try going west
                    if (x-1,y) not in walls:
                        return Directions.WEST
                    else:
                        if (x+1,y) not in walls:
                            return Directions.EAST
                        else:
                            return Directions.NORTH
                else:
                    return Directions.SOUTH
            elif y1 > y:
                if (x,y+1) in walls:
                    #try going west
                    if (x-1,y) not in walls:
                        return Directions.WEST
                    else:
                        if (x+1,y) not in walls:
                            return Directions.EAST
                        else:
                            return Directions.SOUTH
                else:
                    return Directions.NORTH


        def getOneStepToCorner(pacman, corner, walls, legal, theFood, ghostArray):
            distance = util.manhattanDistance(pacman,corner)
            #for bottom left corner only
            print "all food ", self.allFood
            print "corner",corner
            print "pacman", pacman

            if len(ghostArray) > 0:
                print "yes"
                value = 100000;
                for i in range(len(ghostArray)):
                    temp = util.manhattanDistance(pacman,ghostArray[i])
                    if temp < value:
                        value = temp;
                        nearestGhost = ghostArray[i]


                    #print food[0],"   ", food[1] , "-------^^^"

                distance = util.manhattanDistance(pacman,nearestGhost)

                print "pacman ", pacman
                print "ghost", nearestGhost
                x = nearestGhost[0]
                y = nearestGhost[1]
                x1 = pacman[0]
                y1 = pacman[1]

                if (x > x1 and y > y1):
                    print "diagonal 1"
                    if south in legal:
                        return api.makeMove(south, legal)
                    else:
                        if west in legal:
                            return api.makeMove(west, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                elif ( x < x1 and y > y1):
                    print "diagonal 2"
                    if south in legal:
                        print "going south"
                        return api.makeMove(south, legal)
                    else:
                        if east in legal:
                            print "going east"
                            return api.makeMove(east, legal)
                        else:
                            print "going random"
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                elif (x < x1 and y < y1):
                    print "diagonal 3"
                    if north in legal:
                        return api.makeMove(north, legal)
                    else:
                        if east in legal:
                            return api.makeMove(east, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                elif (x > x1 and y < y1):
                    print "diagonal 4"
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
                        print "random from nearest ghost wast"
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
                            print "random from nearest ghost east"
                            pick = random.choice(temp)
                            return api.makeMove(pick, temp)
                elif y1 > y:
                    if north in legal:
                        return api.makeMove(north, legal)
                    else:
                        print "random from nearest ghost north"
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
                        print "random from nearest ghost south"
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
                    print "helloo there, making random move "
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)



            else:

                corners = api.corners(state)
                if(len(theFood) == 0):


                    if(len(self.visitedCorners) > 4 ):
                        print "here we are"

                        value  = 1000000;

                        for food in self.allFood:
                            distance = util.manhattanDistance(pacman,food)
                            if(distance < value):
                                self.corner = food


                    path = breadth_first_search(pacman, self.corner, walls)
                    if(pacman == corner):
                        print "pacman at corner"
                        self.visitedCorners.append(corner)
                        self.corner = getNearestCorner(pacman, corners)
                        path = breadth_first_search(pacman, self.corner, walls)
                        return path.pop(0)
                    else:
                        if path:
                            return path.pop(0)

                    if(pacman[0] > corner[0]):
                        #need to go west
                        print "coming gere"
                        if Directions.WEST in legal:
                            return Directions.WEST
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)

                    elif(pacman[0] == corner[0]):
                        print "needs to visit BL and TL"
                        print self.visitedCorners, " visited corners"
                        if(pacman == corner):
                            print "pacman at corner"
                            self.visitedCorners.append(corner)
                            print "new visited corners", self.visitedCorners
                            #lets visit BL = 1,1
                            if corner == (1,1):
                                if Directions.SOUTH in legal:
                                    return Directions.SOUTH
                                else:
                                    if Directions.NORTH in legal:
                                        return Directions.NORTH
                            elif (corner[1] == 0):
                                if Directions.SOUTH in legal:
                                    return Directions.SOUTH
                                else:
                                    if Directions.NORTH in legal:
                                        return Directions.NORTH
                            elif (corner[0] == 0):
                                if Directions.NORTH in legal:
                                    return Directions.NORTH
                                else:
                                    if Directions.SOUTH in legal:
                                        return Directions.SOUTH
                            else:
                                print "aaaaaa"
                                if Directions.NORTH in legal:
                                    return Directions.NORTH
                                else:
                                    if Directions.SOUTH in legal:
                                        return Directions.SOUTH
                                    else:
                                        pick = random.choice(legal)
                                        return api.makeMove(pick, legal)

                        else:
                            print "hmmmmmmmmmm"
                            return getDirection(pacman, corner, legal)
                    elif (pacman[0] < corner[0]):
                        print "final"
                        index = -1;
                        directions = [Directions.SOUTH, Directions.NORTH, Directions.WEST,Directions.EAST ]
                        if Directions.EAST in legal:
                            return Directions.EAST
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)

                else:
                    print "here"
                    print theFood
                    food = (0,1)
                    value = 100000
                    for i in range(len(theFood)):
                        temp = util.manhattanDistance(pacman,theFood[i])
                        if temp < value:
                            value = temp;
                            food = theFood[i]


                        #print food[0],"   ", food[1] , "-------^^^"

                    distance = util.manhattanDistance(pacman,food)

                    print "coming here"

                    x = food[0]
                    y = food[1]
                    x1 = pacman[0]
                    y1 = pacman[1]

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
                        print "helloo there "
                        pick = random.choice(legal)
                        return api.makeMove(pick, legal)




        walls = api.walls(state)
        corners = api.corners(state)
        legal = api.legalActions(state)
        pacman = api.whereAmI(state)

        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        theFood = api.food(state)

        west = Directions.WEST
        east = Directions.EAST
        south = Directions.SOUTH
        north = Directions.NORTH

        for f in theFood:
            if(f not in self.allFood):
                self.allFood.append(f)

        if(pacman in  self.allFood):
            self.allFood.remove(pacman)

        value = 100000;
        foodCoordinates = (0,0)
        ghostArray = api.ghosts(state);

        #if (len(self.visitedCorners)  < 5):
        self.corner = getNearestCorner(pacman, corners)


        print corners, " are corners"

        direction = getOneStepToCorner(pacman, self.corner, walls, legal, theFood, ghostArray)
        print "pacman", pacman, "corner", self.corner, "walls", walls
        bfs = breadth_first_search(pacman, (1,9), walls)
        #print getChildren(pacman, walls), "--------------------------------"

        print "\n"

        print "corner is: ", self.corner
        print "pacman is: ", pacman
        return api.makeMove(direction, legal)
        '''if Directions.WEST in legal:
            return api.makeMove(Directions.WEST, legal)
        else:
            pick = random.choice(legal)
            return api.makeMove(pick, legal)'''









class CornerSeekingAgent(Agent):

    # Constructor
    #
    # Create variables to remember target positions
    def __init__(self):
         self.BL = False
         self.TL = False
         self.BR = False
         self.TR = False

    # Function run at end of games --- rest target positions so that
    # if we run multiple games using -n 5, they all have the agent
    # starting trying to go to BL.

    def final(self, state):
         self.BL = False
         self.TL = False
         self.BR = False
         self.TR = False

    def getAction(self, state):

        # Get extreme x and y values for the grid
        corners = api.corners(state)
        print corners
        # Setup variable to hold the values
        minX = 100
        minY = 100
        maxX = 0
        maxY = 0

        # Sweep through corner coordinates looking for max and min
        # values.
        for i in range(len(corners)):
            cornerX = corners[i][0] # corners[i] => (2,13)[0] => 2 => (2,13)[i][0] => 2
            cornerY = corners[i][1] # corners[i] => (2,13)[1] => 13


            if cornerX < minX:
                minX = cornerX
            if cornerY < minY:
                minY = cornerY
            if cornerX > maxX:
                maxX = cornerX
            if cornerY > maxY:
                maxY = cornerY

        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        print legal
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Where is Pacman now?
        pacman = api.whereAmI(state)
        print pacman
        #
        # If we haven't got to the lower left corner, try to do that
        #

        # Check we aren't there:
        if pacman[0] == minX + 1:
            if pacman[1] == minY + 1:
                print "Got to BL!"
                self.BL = True

        # If not, move towards it, first to the West, then to the South.
        if self.BL == False:
            if pacman[0] > minX + 1:
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
        #
        # Now we've got the lower left corner
        #

        # Move towards the top left corner

        # Check we aren't there:
        if pacman[0] == minX + 1:
           if pacman[1] == maxY - 1:
                print "Got to TL!"
                self.TL = True

        # If not, move West then North.
        if self.TL == False:
            if pacman[0] > minX + 1:
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

        # Now, the top right corner

        # Check we aren't there:
        if pacman[0] == maxX - 1:
           if pacman[1] == maxY - 1:
                print "Got to TR!"
                self.TR = True

        # Move east where possible, then North
        if self.TR == False:
            if pacman[0] < maxX - 1:
                if Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

        # Fromto right it is a straight shot South to get to the bottom right.

        if pacman[0] == maxX - 1:
           if pacman[1] == minY + 1:
                print "Got to BR!"
                self.BR = True
                return api.makeMove(Directions.STOP, legal)
           else:
               print "Nearly there"
               return api.makeMove(Directions.SOUTH, legal)

        print "Not doing anything!"
        return api.makeMove(Directions.STOP, legal)


class HungryAgent(Agent):

    def getAction(self, state):

        print "start"
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Get the current score
        current_score = state.getScore()
        # Get the last action
        west = Directions.WEST
        east = Directions.EAST
        south = Directions.SOUTH
        north = Directions.NORTH
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        #legal = state.getLegalPacmanActions()
        print "Legal moves ABNCDEFH: ", legal

        print "corners are ", api.corners(state)

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        #for i in range(len(theGhosts)):
        #    print theGhosts[i]

        # How far away are the ghosts?
        #print "Distance to ghosts:"
        #for i in range(len(theGhosts)):
        #    print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)

        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)

        theFood = api.food(state)

        value = 100000;
        foodCoordinates = (0,0)
        for i in range(len(theFood)):
            temp = util.manhattanDistance(pacman,theFood[i])
            if temp < value:
                value = temp;
                food = theFood[i]

        #print food[0],"   ", food[1] , "-------^^^"
        distance = util.manhattanDistance(pacman,food)
        if distance > 1:

            last = state.getPacmanState().configuration.direction
            # If we can repeat the last action, do it. Otherwise make a
            # random choice.
            if last in legal:
                return api.makeMove(last, legal)
            else:
                pick = random.choice(legal)
                return api.makeMove(pick, legal)


        x = food[0]
        y = food[1]
        x1 = pacman[0]
        y1 = pacman[1]

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
            print "helloo there "
            pick = random.choice(legal)
            return api.makeMove(pick, legal)



# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)

        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)

        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)
