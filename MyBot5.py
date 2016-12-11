import hlt_erdman
from hlt_erdman import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random


myID, game_map = hlt_erdman.get_init()
hlt_erdman.send_init("CrapBot")


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

def combine_border_pieces(square):
    border_p1 = square
    border_p2 = square
    heuristic_p0, heuristic_p1, heuristic_p2 = 0, 0, 0
    direction_1, direction_2 = STILL, STILL
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.owner == myID:
            for neighbor_of_neighbor in game_map.neighbors(neighbor):
                if neighbor_of_neighbor != myID:
                    if border_p1.x == square.x and border_p1.y == square.y:
                        border_p1 = neighbor
                        direction_1 = direction
                    else:
                        border_p2 = neighbor
                        direction_2 = direction
    for neighbor in game_map.neighbors(square):
        if neighbor.owner != myID:
            temp_heuristic = heuristic(neighbor)
            if heuristic_p0 < temp_heuristic:
                heuristic_p0 = temp_heuristic
    for neighbor in game_map.neighbors(border_p1):
        if neighbor.owner != myID:
            temp_heuristic = heuristic(neighbor)
            if heuristic_p1 < temp_heuristic:
                heuristic_p1 = temp_heuristic
    for neighbor in game_map.neighbors(border_p2):
        if neighbor.owner != myID:
            temp_heuristic = heuristic(neighbor)
            if heuristic_p2 < temp_heuristic:
                heuristic_p2 = temp_heuristic
    if heuristic_p1 >= heuristic_p2 and heuristic_p1 >= heuristic_p0:
        if game_map.get_target(square, direction_1).owner == myID:
            return direction_1
    if heuristic_p2 >= heuristic_p1 and heuristic_p1 >= heuristic_p0:
        if game_map.get_target(square, direction_2).owner == myID:
            return direction_2       
    return STILL     

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
        return Move(square, combine_border_pieces(square))

    
while True:
    game_map.get_frame()
    moves = [get_move(square) for square in game_map if square.owner == myID]
    hlt_erdman.send_frame(moves)

