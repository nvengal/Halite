import hlt_erdman
from hlt_erdman import NORTH, EAST, SOUTH, WEST, STILL, Move, Square


myID, game_map = hlt_erdman.get_init()
hlt_erdman.send_init("CurrentBot")

#Focus squares to attack enemy
def tunnel(square, direction, min_path, enemy_id):
    max_distance = min(game_map.width, game_map.height) / 2
    opp_direction= (direction+2)%4
    move_direction = STILL
    touching_enemy = False

    #Check each straight line approach
    for d in (NORTH, EAST, SOUTH, WEST):
        if d != direction and d != opp_direction:
            d_distance = 0
            current = square
            path_strength = 0
            while d_distance < max_distance and current.owner == myID:
                dir_distance = 0
                d_distance += 1
                current = game_map.get_target(current, d)
                path_strength += 1
                while current.owner != enemy_id and dir_distance < max_distance:
                    dir_distance += 1
                    current = game_map.get_target(current, direction)
                    path_strength += 1
                    if current.owner == 0:
                        path_strength += current.strength
                if path_strength < min_path and dir_distance < max_distance:
                    move_direction = d
                    min_path = path_strength
    if min_path < max_distance:
        touching_enemy = True

    return move_direction, touching_enemy

def find_nearest_enemy_direction(square):
    direction = STILL
    max_distance = min(game_map.width, game_map.height) / 2

    touching_enemy = False
    
    #First check for nearby enemies
    for d in (NORTH, EAST, SOUTH, WEST):
        distance = 0
        current = square
        path_strength = 0
        while (current.owner == myID or current.owner == 0) and distance < max_distance:
            distance += 1
            current = game_map.get_target(current, d)
            if current.owner == 0:
                path_strength += current.strength
        if distance < max_distance:
            direction = d
            max_distance = distance
            min_path = path_strength
            enemy_id = current.owner
    if direction != STILL:
        #If inline to attack enemy, move
        if min_path == 0:
            touching_enemy = True
            return direction, touching_enemy
        #Find the direction of the best path to enemy
        move_direction, touching_enemy = tunnel(square, direction, min_path, enemy_id)
        if move_direction != STILL:
            return move_direction, touching_enemy
        else:
            return direction, touching_enemy
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
    return direction, touching_enemy

def heuristic(square):
    if square.owner == 0 and square.strength > 0:
        return square.production / square.strength
    else:
        # return total potential damage caused by overkill when attacking this square
        return sum(neighbor.strength for neighbor in game_map.neighbors(square) if neighbor.owner not in (0, myID))

#Heuristic that can recieve friendly squares as argument
def friendly_heuristic(square):
    if square is not None:
        target = max((neighbor for neighbor in game_map.neighbors(square)
                                    if neighbor.owner != myID),
                                    default = None,
                                    key = lambda t: heuristic(t))
        if target is not None:
            return heuristic(target)
    return 0
    
def get_move(square):

    border = any(neighbor.owner != myID for neighbor in game_map.neighbors(square))

    border_direction, touching_enemy = find_nearest_enemy_direction(square)

    #Only attack border squares if enemy is not found
    if not touching_enemy and border:
        #Search border squares for best attack direction
        target, direction = max(((neighbor, direction) for direction, neighbor in enumerate(game_map.neighbors(square))
                                if neighbor.owner != myID),
                                default = (None, None),
                                key = lambda t: heuristic(t[0]))
        if target is not None and target.strength < square.strength:
            return direction

    #Stand still if squares are weak
    if square.strength < square.production * 5:
        return STILL

    border_target = game_map.get_target(square, border_direction)
    #If an inner square move to location
    if not border and border_target.owner == myID:
        return border_direction

    #If enemy is being attacked, help attack
    elif touching_enemy:
        target, direction = max(((neighbor, direction) for direction, neighbor in enumerate(game_map.neighbors(square))
                                if neighbor.owner != myID and neighbor.strength == 0),
                                default = (None, None),
                                key = lambda t: heuristic(t[0]))
        if target is not None and target.strength < square.strength:
            return direction
        elif target is None and (border_target.owner == myID or border_target.strength == 0):
            return border_direction

    #Any squares that can kill something and haven't should attack
    target, direction = max(((neighbor, direction) for direction, neighbor in enumerate(game_map.neighbors(square))
                            if neighbor.owner != myID),
                            default = (None, None),
                            key = lambda t: heuristic(t[0]))
    if target is not None and target.strength < square.strength:
        return direction

    #Combine border squares that aren't strong enough
    target, direction = max(((neighbor, direction) for direction, neighbor in enumerate(game_map.neighbors(square))
                            if neighbor.owner == myID),
                            default = (None, None),
                            key = lambda t: friendly_heuristic(t[0]))
    if target is not None and target.owner == myID:
        if friendly_heuristic(target) > friendly_heuristic(square):
            return direction
    
    return STILL
    
while True:
    game_map.get_frame()
    max_squares = []
    moves = []
    for square in game_map:
        if square.owner == myID:
            direction = get_move(square)
            target = game_map.get_target(square, direction)
            #If target is full strength ally don't move
            if target in max_squares:
                direction = STILL
                target = square
            #If square is full strength, add location to list
            if square.strength == 255:
                max_squares.append(target)
            moves.append(Move(square, direction))
    hlt_erdman.send_frame(moves)

