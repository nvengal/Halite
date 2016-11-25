from hlt import *
from networking import *

myID, gameMap = getInit()
sendInit("MyBot")

def find_best_production_zone(location):
    site = gameMap.getSite(location)
    best_production = site.production
    #Search immediate vicinity for highest production
    for d in CARDINALS:
        neighbor_site = gameMap.getSite(location, d)
        if neighbor_site.owner != myID:
            if neighbor_site.production > best_production:
                best_production = neighbor_site.production
                best_direction = d
    if best_production == site.production:
        return STILL
    else:
        return best_direction

def should_attack(location, direction):
    site = gameMap.getSite(location)
    neighbor_site = gameMap.getSite(location, direction)
    #If enemy and weaker, move
    if neighbor_site.owner == myID and neighbor_site.strength < site.strength:
        return True
    #If ally, move
    elif neighbor_site.strength < site.strength:
        return True
    #Else, stay
    else:
        return False
        
def move(location):
    site = gameMap.getSite(location)
    #Search immediate vicinity, if enemy square is weaker, attack
    for d in CARDINALS:
        if gameMap.getSite(location, d).owner != myID:
            if should_attack(location, d):
                return Move(location, d)
    #If unit is weak, charge up
    if site.strength < site.production * 10:
        return Move(location, STILL)
    best_direction = find_best_production_zone(location)
    #If unit has a safe place that is better, move
    if best_direction != STILL:
        if should_attack(location, best_direction):
            return Move(location, best_direction)
    #If unit will not kamikaze, move
    random_direction = SOUTH if random.random() > 0.5 else EAST
    if should_attack(location, random_direction):
        return Move(location, random_direction)
    #If unit has no choice, stay still
    return Move(location, STILL)

while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location))
    sendFrame(moves)
