from hlt import *
from networking import *
import logging

##logging.basicConfig(filename='logging_file.log',level=logging.DEBUG)
##logging.debug('This message should go to the log file')

myID, gameMap = getInit()
sendInit("MyBot3")
#Improvement on moving out from center

def should_attack(location, direction):
    site = gameMap.getSite(location)
    neighbor_site = gameMap.getSite(location, direction)
    #If enemy and weaker, move
    if neighbor_site.owner != myID and neighbor_site.strength < site.strength:
        return True
    #If friendly, moving is okay
    if neighbor_site.owner == myID:
        return True
    #Else, stay
    else:
        return False

#Which direction is away from center
def away_from_center(location):
    center_site = gameMap.getSite(center)
    #Find the shorter dimension
    if border_x < border_y:
        #Choose the right direction
        if location.x > center.x:
            if location.x > center.x + border_x:
                return WEST
            return EAST
        if location.x < center.x:
            if location.x < center.x - border_x:
                return EAST
            return WEST
    if location.y > center.y:
        if location.y > center.y + border_y:
                return NORTH
        return SOUTH
    if location.y < center.y:
        if location.y < center.y - border_y:
                return SOUTH
        return NORTH
    return STILL

#Focus everything into a center point
def into_center(location):
    d_x = gameMap.width/2
    d_y = gameMap.height/2
    if abs(location.x-d_x) > abs(location.y- d_y):
        if location.x < d_x:
            return EAST
        else:
            return WEST
    if location.y < d_y:
        return SOUTH
    return NORTH

def move(location):
    site = gameMap.getSite(location)
    #Search immediate vicinity, if enemy square is weaker, attack
    for d in CARDINALS:
        if should_attack(location, d) and gameMap.getSite(location, d).owner != myID:
            return Move(location, d)
    #If unit is weak, charge up
    if site.strength < site.production * 10:
        return Move(location, STILL)
    #If occupying all four corners, converge onto center
    if gameMap.getSite(Location(0,0)).owner == myID:
        if gameMap.getSite(Location(0,gameMap.height-1)).owner == myID:
            if gameMap.getSite(Location(gameMap.width-1,0)).owner == myID:
                if gameMap.getSite(Location(gameMap.width-1,gameMap.height-1)).owner == myID:
                    return Move(location, into_center(location))
    #Expand out from center of shape
    if should_attack(location, away_from_center(location)):
        return Move(location, away_from_center(location))
    return Move(location, STILL)
    
center = Location(0,0)
while True:
    moves = []
    #Variables to track the boundary of the shape
    min_x = gameMap.width
    max_x = 0
    sum_x = 0
    min_y = gameMap.height
    max_y = 0
    sum_y = 0
    count = 0
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                if x < min_x:
                    min_x = x 
                if x > max_x:
                    max_x = x 
                if y < min_y:
                    min_y = y 
                if y > max_y:
                    max_y = y
                sum_x = sum_x + x
                sum_y = sum_y + y
                count = count + 1
                moves.append(move(location))
    #Calculate rough outline of shape
    center = Location(int((sum_x)/count), int((sum_y)/count))
    border_x = min(abs(min_x-center.x), abs(max_x-center.x))
    border_y = min(abs(min_y-center.y), abs(max_y-center.y))
    sendFrame(moves)
