import hlt_erdman
from hlt_erdman import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random


myID, game_map = hlt_erdman.get_init()
hlt_erdman.send_init("BorderBot1")


def find_nearest_enemy_direction(square):
    direction = STILL
    max_distance = min(game_map.width, game_map.height) / 2
    #First check for nearby enemies
    for d in (NORTH, EAST, SOUTH, WEST):
        distance = 0
        current = square
        while (current.owner == myID or current.owner == 0) and distance < max_distance:
            distance += 1
            current = game_map.get_target(current, d)   
        if distance < max_distance:
            direction = d
            max_distance = distance
    if direction != STILL:
        return direction
    else:
        direction = NORTH
    #Find nearest border            
    for d in (NORTH, EAST, SOUTH, WEST):
        distance = 0
        current = square
        while current.owner == myID and distance < max_distance:
            distance += 1
            current = game_map.get_target(current, d)
        if distance < max_distance:
            direction = d
            max_distance = distance 
    return direction

def heuristic(square):
    if square.owner == 0 and square.strength > 0:
        return square.production / square.strength
    else:
        # return total potential damage caused by overkill when attacking this square
        return sum(neighbor.strength for neighbor in game_map.neighbors(square) if neighbor.owner not in (0, myID))

def friendly_heuristic(square):
    #Heuristic that can take friendly squares as the argument
    if square is not None:
        target = max((neighbor for neighbor in game_map.neighbors(square)
                                    if neighbor.owner != myID),
                                    default = None,
                                    key = lambda t: heuristic(t))
        if target is not None:
            return heuristic(target)
    return 0
    
def get_move(square):       
    target, direction = max(((neighbor, direction) for direction, neighbor in enumerate(game_map.neighbors(square))
                                if neighbor.owner != myID),
                                default = (None, None),
                                key = lambda t: heuristic(t[0]))
    if target is not None and target.strength < square.strength:
        return Move(square, direction)
    elif square.strength < square.production * 5:
        return Move(square, STILL)

    border = any(neighbor.owner != myID for neighbor in game_map.neighbors(square))
    if not border:
        return Move(square, find_nearest_enemy_direction(square))
    else:
        target, direction = max(((neighbor, direction) for direction, neighbor in enumerate(game_map.neighbors(square))
                                if neighbor.owner == myID),
                                default = (None, None),
                                key = lambda t: friendly_heuristic(t[0]))
        if target is not None and target.owner == myID:
            if friendly_heuristic(target) > friendly_heuristic(square):
                return Move(square, direction)

    return Move(square, STILL)
    
        

    
while True:
    game_map.get_frame()
    moves = [get_move(square) for square in game_map if square.owner == myID]
    hlt_erdman.send_frame(moves)
