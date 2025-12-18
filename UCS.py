from queue import PriorityQueue

LEVEL_MAP = [
    "#######",
    "#@.$ G#",
    "#.#.#.#",
    "#.$ G #",
    "#######"
]

ROWS = len(LEVEL_MAP)    
COLS = len(LEVEL_MAP[0]) 

MOVES = {
    'Up': (-1, 0),
    'Down': (1, 0),
    'Left': (0, -1),
    'Right': (0, 1)
}

def find_goals(level_map):
    goals = set()
    for r in range(ROWS):
        for c in range(COLS):
            if level_map[r][c] == 'G': 
                goals.add((r, c))
    return goals

GOAL_POSITIONS = find_goals(LEVEL_MAP)  

def find_start_state(level_map):
    player_pos = None
    box_positions = set()
    for r in range(ROWS):
        for c in range(COLS):
            char = level_map[r][c]
            if char == '@':
                player_pos = (r, c)  
            elif char == '$':
                box_positions.add((r, c)) 
    return (player_pos, frozenset(box_positions))

def is_wall(pos):
    r, c = pos
    if 0 <= r < ROWS and 0 <= c < COLS:
        return LEVEL_MAP[r][c] == '#'
    return True  

def is_goal(box_positions):
    return box_positions.issubset(GOAL_POSITIONS) and len(box_positions) == len(GOAL_POSITIONS)

def get_next_state(current_state, move_dir):
    (pr, pc), box_positions = current_state
    dr, dc = MOVES[move_dir]
    new_pr, new_pc = pr + dr, pc + dc

    if is_wall((new_pr, new_pc)):
        return None
    if (new_pr, new_pc) not in box_positions:
        return ((new_pr, new_pc), box_positions)
    
    box_pos = (new_pr, new_pc)
    next_to_box_pos = (new_pr + dr, new_pc + dc)
    if is_wall(next_to_box_pos) or next_to_box_pos in box_positions:
        return None

    new_box_positions = set(box_positions)
    new_box_positions.remove(box_pos)
    new_box_positions.add(next_to_box_pos)
    return (box_pos, frozenset(new_box_positions))

def solve_sokoban_ucs(level_map):
    start_state = find_start_state(level_map)

    if is_goal(start_state[1]):
        print("Puzzle already solved!")
        return []

    pq = PriorityQueue() 
    pq.put((0, start_state, []))  
    visited = dict()     
    nodes_explored = 0

    while not pq.empty():
        cost, current_state, path = pq.get()
        nodes_explored += 1

        if is_goal(current_state[1]):
            print(f"\nGoal reached! Total moves: {len(path)}, Nodes Explored: {nodes_explored}")
            print("Solution Move Sequence:")
            print(" -> ".join(path))
            return path

        if current_state in visited:
            if cost < visited[current_state]:
                print(f"Node revisited with lower cost! Cost: {cost}, Path: {' -> '.join(path)}")
            else:
                print(f"Node skipped (already visited with equal/less cost). Cost: {cost}, Path: {' -> '.join(path)}")
                continue
        else:
            print(f"Visiting new node. Cost: {cost}, Path: {' -> '.join(path)}")

        visited[current_state] = cost

        for move_name in MOVES:
            next_state = get_next_state(current_state, move_name)
            if next_state is not None:
                next_cost = cost + 1
                if next_state not in visited or visited[next_state] > next_cost:
                    pq.put((next_cost, next_state, path + [move_name]))

    print("Puzzle is unsolvable or too deep.")
    print(f"Nodes Explored: {nodes_explored}")
    return None

if __name__ == "__main__":
    print("... Starting UCS search ...")
    solution_ucs = solve_sokoban_ucs(LEVEL_MAP)
