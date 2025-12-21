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
    else:
        box_pos = (new_pr, new_pc)
        next_to_box_pos = (new_pr + dr, new_pc + dc)
        if is_wall(next_to_box_pos) or next_to_box_pos in box_positions:
            return None
        new_box_positions = set(box_positions)
        new_box_positions.remove(box_pos)
        new_box_positions.add(next_to_box_pos)
        return (box_pos, frozenset(new_box_positions))

def heuristic(box_positions):
    total_dist = 0
    for box in box_positions:
        min_dist = min(abs(box[0]-goal[0]) + abs(box[1]-goal[1]) for goal in GOAL_POSITIONS)
        total_dist += min_dist
    return total_dist

def solve_sokoban_hill_climbing(level_map, max_steps=1000):
    start_state = find_start_state(level_map)
    if is_goal(start_state[1]):
        print("Puzzle already solved")
        return []

    current_state = start_state
    path = []
    nodes_explored = 0

    for step in range(max_steps):
        nodes_explored += 1
        successors = []
        for move_name in MOVES:
            next_state = get_next_state(current_state, move_name)
            if next_state is not None:
                h = heuristic(next_state[1])
                successors.append((h, move_name, next_state))
        if not successors:
            break
        successors.sort(key=lambda x: x[0])
        best_h, best_move, best_state = successors[0]
        if best_h >= heuristic(current_state[1]):
            break
        current_state = best_state
        path.append(best_move)
        if is_goal(current_state[1]):
            print(f"Solution found in {len(path)} moves")
            print(f"Nodes explored: {nodes_explored}")
            return path

    print("Hill Climbing failed (stuck or dead-end)")
    print(f"Nodes explored: {nodes_explored}")
    return None

if __name__ == "__main__":
    print("Starting Hill Climbing search...")
    solution_hc = solve_sokoban_hill_climbing(LEVEL_MAP)
    if solution_hc:
        print("Solution Move Sequence:")
        print(" -> ".join(solution_hc))


