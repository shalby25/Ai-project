LEVEL_MAP = [
    "#######",
    "#@.$.G#",
    "#.#.#.#",
    "#.$.G.#",
    "#######"
]

ROWS = len(LEVEL_MAP)
COLS = len(LEVEL_MAP[0])

ACTIONS = {
    "Up":    (-1, 0),
    "Down":  (1, 0),
    "Left":  (0, -1),
    "Right": (0, 1)
}

def extract_initial_state():
    player = None
    boxes = set()

    for r in range(ROWS):
        for c in range(COLS):
            cell = LEVEL_MAP[r][c]
            if cell == "@":
                player = (r, c)
            elif cell == "$":
                boxes.add((r, c))

    return (player, frozenset(boxes))

def extract_goal_positions():
    goals = set()
    for r in range(ROWS):
        for c in range(COLS):
            if LEVEL_MAP[r][c] == "G":
                goals.add((r, c))
    return goals


GOALS = extract_goal_positions()


def is_wall(cell):
    r, c = cell                            
    return LEVEL_MAP[r][c] == "#"

def goal_test(boxes):
    return boxes == GOALS

def apply_action(state, action):
    (pr, pc), boxes = state
    dr, dc = ACTIONS[action]

    next_player = (pr + dr, pc + dc)

    if is_wall(next_player):
        return None

    if next_player not in boxes:
        return (next_player, boxes)

    box_target = (next_player[0] + dr, next_player[1] + dc)     

    if is_wall(box_target) or box_target in boxes:              
        return None

    new_boxes = set(boxes)
    new_boxes.remove(next_player)
    new_boxes.add(box_target)

    return (next_player, frozenset(new_boxes))

def limited_dfs(state, depth, path, visited, counter):

    counter[0] += 1

    if goal_test(state[1]):       
        return path

    if depth == 0:                          
        return None              

    for action in ACTIONS:                                            
        next_state = apply_action(state, action)

        if next_state and next_state not in visited:                
            visited.add(next_state)

            result = limited_dfs(                                    
                next_state,
                depth - 1,
                path + [action],
                visited,
                counter
            )

            if result is not None:                                 
                return result

    return None                                                 

def iterative_deepening_search(max_depth=50):

    start_state = extract_initial_state()
    total_expanded = 0

    for limit in range(max_depth + 1):
        print(f"Searching with depth limit = {limit}")

        visited = {start_state}                      
        expanded = [0]

        solution = limited_dfs(
            start_state,
            limit,
            [],
            visited,
            expanded
        )

        total_expanded += expanded[0]

        if solution is not None:
            print("Solution found")
            print(f"Path length: {len(solution)}")
            print(f"Nodes expanded: {total_expanded}")
            return solution

    print("No solution within depth limit")
    return None

print("\n--- IDS Sokoban Solver ---\n")
solution_path = iterative_deepening_search()

if solution_path:
    print("\nMovement Sequence:")
    print(" -> ".join(solution_path))

