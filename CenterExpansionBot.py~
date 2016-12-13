from hlt import *
from networking import *

myID, gameMap = getInit()
sendInit("MyBot2")

def should_attack(location, direction):
    site = gameMap.getSite(location)
    neighbor_site = gameMap.getSite(location, direction)
    #If enemy and weaker, move
    if neighbor_site.owner != myID and neighbor_site.strength < site.strength:
        return True
    #Else, stay
    else:
        return False

#Which direction is away from center
def away_from_center(location):
    center_site = gameMap.getSite(center)
    if location.x < center.x:
        if center_site.owner != myID:
            return EAST
        return WEST
    if location.y > center.y:
        if center_site.owner != myID:
            return NORTH
        return SOUTH
    if location.x > center.x:
        if center_site.owner != myID:
            return WEST
        return EAST
    if location.y < center.y:
        if center_site.owner != myID:
            return SOUTH
        return NORTH
    #Place Holder for Center
    return STILL
    
def move(location):
    site = gameMap.getSite(location)
    #Search immediate vicinity, if enemy square is weaker, attack
    for d in CARDINALS:
        if should_attack(location, d):
            return Move(location, d)
    #If unit is weak, charge up
    if site.strength < site.production * 10:
        return Move(location, STILL)
    #If unit is surrounded by friendlies move away from center
    if gameMap.getSite(location, NORTH).owner == myID and gameMap.getSite(location, EAST).owner == myID and gameMap.getSite(location, SOUTH).owner == myID and gameMap.getSite(location, WEST).owner == myID:
            return Move(location, away_from_center(location))
    return Move(location, STILL)
    
center = Location(0,0)
while True:
    moves = []
    min_x = gameMap.width
    max_x = 0
    min_y = gameMap.height
    max_y = 0
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                if location.x < min_x:
                    min_x = location.x 
                if location.x > max_x:
                    max_x = location.x 
                if location.y < min_y:
                    min_y = location.y 
                if location.y > max_y:
                    max_y = location.y 
                moves.append(move(location))
    center = Location(int((min_x+max_x)/2), int((min_y+max_y)/2))
    sendFrame(moves)
