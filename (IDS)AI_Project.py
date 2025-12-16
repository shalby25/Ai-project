#--Sokoban game code using IDS Algorithm --#

#--Game setup--#
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


#--Extraction(player & boxes)--#
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

#--Extraction(goal postions)--#
def extract_goal_positions():
    goals = set()
    for r in range(ROWS):
        for c in range(COLS):
            if LEVEL_MAP[r][c] == "G":
                goals.add((r, c))
    return goals


GOALS = extract_goal_positions()


#--Wall detection--#
def is_wall(cell):
    r, c = cell                            
    return LEVEL_MAP[r][c] == "#"

#--making sure we`re right or not--#
def goal_test(boxes):
    return boxes == GOALS

#--moving actions--#
def apply_action(state, action):
    (pr, pc), boxes = state
    dr, dc = ACTIONS[action]

    next_player = (pr + dr, pc + dc)

    if is_wall(next_player):
        return None

    if next_player not in boxes:
        return (next_player, boxes)

    box_target = (next_player[0] + dr, next_player[1] + dc)     #next_player[0] = x coordinate , next_player[1] = y coordinate

    if is_wall(box_target) or box_target in boxes:              #"box_target in boxes" (cannot move 2 boxes at the same time)
        return None

    new_boxes = set(boxes)
    new_boxes.remove(next_player)
    new_boxes.add(box_target)

    return (next_player, frozenset(new_boxes))


#--Depth-Limited DFS--#

def limited_dfs(state, depth, path, visited, counter):

    counter[0] += 1

    if goal_test(state[1]):       #"state[1]=boxes"
        return path

    if depth == 0:                          
        return None               #if we reached to deepest point and still no solution

    for action in ACTIONS:                                            #apply thoose steps to every action(up,...,down) 
        next_state = apply_action(state, action)

        if next_state and next_state not in visited:                 #to avoid loops 
            visited.add(next_state)

            result = limited_dfs(                                     #the recursive call
                next_state,
                depth - 1,
                path + [action],
                visited,
                counter
            )

            if result is not None:                                 #if we found a solution
                return result

    return None                                                   #if we did not


#--IDS Algorithm--#
def iterative_deepening_search(max_depth=50):

    start_state = extract_initial_state()
    total_expanded = 0

    for limit in range(max_depth + 1):
        print(f"Searching with depth limit = {limit}")

        visited = {start_state}                         #for every new limit , new visited from start_state
        expanded = [0]                                  #same here

        solution = limited_dfs(
            start_state,
            limit,
            [],
            visited,
            expanded
        )

        total_expanded += expanded[0]

        if solution is not None:
            print("✔ Solution found")
            print(f"✔ Path length: {len(solution)}")
            print(f"✔ Nodes expanded: {total_expanded}")
            return solution

    print("✘ No solution within depth limit")
    return None


#--Entry--#
print("\n--- IDS Sokoban Solver ---\n")
solution_path = iterative_deepening_search()

if solution_path:
    print("\nMovement Sequence:")
    print(" -> ".join(solution_path))
