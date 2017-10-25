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

class PartialAgent(Agent):

        # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
         self.BL = False
         self.TL = False
         self.UR = False
         self.TR = False
         self.Ghost = False
         self.last = Directions.WEST

    # Function run at end of games --- rest target positions so that
    # if we run multiple games using -n 5, they all have the agent
    # starting trying to go to BL.

    def final(self, state):
         self.BL = False
         self.TL = False
         self.UR = False
         self.TR = False
         self.Ghost = False
         self.last = Directions.WEST

    # For now I just move randomly
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.

        theFood = api.food(state)
        pacman = api.whereAmI(state)
        west = Directions.WEST
        east = Directions.EAST
        south = Directions.SOUTH
        north = Directions.NORTH

        value = 100000;
        foodCoordinates = (0,0)
        ghostArray = api.ghosts(state);

        if len(ghostArray) > 0:
            print "yes"
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
                    pick = random.choice(temp)
                    return api.makeMove(pick, temp)
            elif x > x1:
                if west in legal:
                    return api.makeMove(west, legal)
                else:
                    temp = legal
                    if east in temp:
                        temp.remove(east)
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
                    pick = random.choice(temp)
                    return api.makeMove(pick, temp)
            else:
                print "helloo there, making random move "
                pick = random.choice(legal)
                return api.makeMove(pick, legal)




        else:
            corners = api.corners(state)
            print corners, " are corners"
            # Setup variable to hold the values
            minX = 100
            minY = 100
            maxX = 0
            maxY = 0

            if len(theFood) == 0:
                print "distance > 1"
                corners = api.corners(state)
                print corners, " are corners"
                # Setup variable to hold the values
                minX = 100
                minY = 100
                maxX = 0
                maxY = 0

                # Sweep through corner coordinates looking for max and min
                # values.
                value = 100000
                corner = corners[0]
                for i in range(len(corners)):
                    temp = util.manhattanDistance(pacman,corners[i])
                    if temp < value:
                        value = temp;
                        corner = corners[i]


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
                if corner[0] == 0 and corner[1] == 0:
                    if pacman[0] == corner[0] + 1:
                        if pacman[1] == corner[1] + 1:
                            print "Got to BL!"
                            self.BL = True

                    # If not, move towards it, first to the West, then to the South.
                    if self.BL == False:
                        if pacman[0] > corner[0] + 1:
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
                elif corner[0] == 0:


                #
                # Now we've got the lower left corner
                #

                # Move towards the top left corner

                # Check we aren't there:
                    if pacman[0] == corner[0] + 1:
                       if pacman[1] == corner[1] - 1:
                            print "Got to TL!"
                            self.TL = True

                    # If not, move West then North.
                    if self.TL == False:
                        if pacman[0] > corner[0] + 1:
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
                if pacman[0] == corner[0] - 1:
                   if pacman[1] == corner[1] - 1:
                        print "Got to TR!"
                        self.TR = True

                # Move east where possible, then North
                if self.TR == False:
                    if pacman[0] < corner[0] - 1:
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

                if pacman[0] == corner[0] - 1:
                   if pacman[1] == corner[1] + 1:
                        print "Got to BR!"
                        self.BR = True
                        return api.makeMove(Directions.WEST, legal)
                   else:
                       print "Nearly there"
                       return api.makeMove(Directions.SOUTH, legal)


                pick = random.choice(legal)
                return api.makeMove(pick, legal)

            else:
                print theFood
                for i in range(len(theFood)):
                    temp = util.manhattanDistance(pacman,theFood[i])
                    if temp < value:
                        value = temp;
                        food = theFood[i]


                    #print food[0],"   ", food[1] , "-------^^^"

                distance = util.manhattanDistance(pacman,food)
                if pacman[0] == minX + 1:
                    if pacman[1] == minY + 1:
                        print "Got to BL!"
                        self.BL = True
                if pacman[0] == minX + 1:
                   if pacman[1] == maxY - 1:
                        print "Got to TL!"
                        self.TL = True
                if pacman[0] == maxX - 1:
                   if pacman[1] == maxY - 1:
                        print "Got to TR!"
                        self.TR = True
                if pacman[0] == maxX - 1:
                   if pacman[1] == minY + 1:
                        print "Got to BR!"
                        self.BR = True

                print "coming here"

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
