from collections import deque

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
    """Identifies all fixed goal positions."""
    goals = set()
    for r in range(ROWS):
        for c in range(COLS):
            if level_map[r][c] == 'G':
                goals.add((r, c))
    return goals

GOAL_POSITIONS = find_goals(LEVEL_MAP)

def find_start_state(level_map):
    """Extracts initial Player and Box positions."""
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
    """Checks if a position is a wall."""
    r, c = pos
    if 0 <= r < ROWS and 0 <= c < COLS:
        return LEVEL_MAP[r][c] == '#'
    return True

def is_goal(box_positions):
    """Checks if all boxes are on goals."""
    return box_positions.issubset(GOAL_POSITIONS) and len(box_positions) == len(GOAL_POSITIONS)


def get_next_state(current_state, move_dir):
    """Calculates the resulting state after a valid move."""
    (pr, pc), box_positions = current_state
    dr, dc = MOVES[move_dir]
    
    new_pr, new_pc = pr + dr, pc + dc
    
    if is_wall((new_pr, new_pc)):
        return None
    
    if (new_pr, new_pc) not in box_positions:
        return ((new_pr, new_pc), box_positions)
        
    else:
        box_pos = (new_pr, new_pc)
        next_to_box_r, next_to_box_c = new_pr + dr, new_pc + dc
        next_to_box_pos = (next_to_box_r, next_to_box_c)
        
        if is_wall(next_to_box_pos) or next_to_box_pos in box_positions:
            return None
        
        else:
            new_player_pos = box_pos
            new_box_positions = set(box_positions)
            new_box_positions.remove(box_pos)
            new_box_positions.add(next_to_box_pos)
            
            return (new_player_pos, frozenset(new_box_positions))


def solve_sokoban_bfs(level_map):
    
    start_state = find_start_state(level_map)
    
    if is_goal(start_state[1]):
        print("Puzzle already solved!")
        return []

    queue = deque([(start_state, [])])
    
    visited = {start_state}
    
    nodes_explored = 0

    while queue:
        current_state, path = queue.popleft() 
        nodes_explored += 1
        
        if is_goal(current_state[1]):
            print(f" Solution found (Shortest path: {len(path)} moves).")
            print(f" Nodes Explored: {nodes_explored}")
            return path
       
        for move_name, move_delta in MOVES.items():
            
            next_state = get_next_state(current_state, move_name)
            
            if next_state is not None:
                if next_state not in visited:
                    visited.add(next_state)
                    new_path = path + [move_name]
                    queue.append((next_state, new_path))
                    
    print(" Puzzle is unsolvable or too deep for current search scope.")
    print(f"Nodes Explored: {nodes_explored}")
    return None

print("... Starting BFS search ...")
solution = solve_sokoban_bfs(LEVEL_MAP)

if solution:
    print("\nSolution Move Sequence:")

    print(" -> ".join(solution))
