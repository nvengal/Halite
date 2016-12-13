from hlt import *
from networking import *
import time

myID, gameMap = getInit()
sendInit("MyBot4")

def heuristic(in_site, in_loc):
    #If neutral cell
    if in_site.owner == 0 and in_site.strength > 0:
        return in_site.production / in_site.strength
    #If enemy cell
    else:
        total_damage = 0
        #Calculate overkill damage
        for d in CARDINALS:
            neighbor_site = gameMap.getSite(in_loc, d)
            if neighbor_site.owner != 0 and neighbor_site.owner != myID:
                total_damage += neighbor_site.strength
        return total_damage
        
#Check surrounding squares to find highest value move
def best_direction(location):
    max_value = 0
    direction = STILL

    for d in CARDINALS:
        neighbor_site = gameMap.getSite(location, d)
        neighbor_loc = gameMap.getLocation(location, d)
        if neighbor_site.owner != myID:
            value = heuristic(neighbor_site, neighbor_loc)
            if value >= max_value:
                direction = d
                max_value = value

    return direction

#Find the direction of closest border
def closest_border(location):
    direction = NORTH
    max_distance = min(gameMap.width, gameMap.height) / 2

    for d in CARDINALS:
        distance = 0
        current = location
        next_site = gameMap.getSite(current, d)
        while next_site.owner == myID and distance < max_distance:
            distance += 1
            current = gameMap.getLocation(current, d)
            next_site = gameMap.getSite(current)
        if distance < max_distance:
            direction = d
            max_distance = distance

    return direction
    
def move(location):
    site = gameMap.getSite(location)
    border = False

    if site.strength < site.production * 5:
        return Move(location, STILL)

    #Is border cell?
    for d in CARDINALS:
        neighbor_site = gameMap.getSite(location, d)
        if neighbor_site.owner != myID:
            border = True

    #If border what is best move?
    if border:
        pos_direction = best_direction(location)
        neighbor_site = gameMap.getSite(location, pos_direction)
        if neighbor_site.owner != myID:
            if neighbor_site.strength < site.strength:
                return Move(location, pos_direction)

    #If not border radiate outwards
    if not border:
        return Move(location, closest_border(location))

    return Move(location, STILL)

#Move for each owned cell
def determine_moves():
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location))
            #If out of time, finalize moves
            if time.time() - start_time > .98:
                return
    return

#Main
while True:
    start_time = time.time()
    moves = []
    gameMap = getFrame()
    determine_moves()
    sendFrame(moves)

