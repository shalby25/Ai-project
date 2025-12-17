import heapq

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

def find_goals():
    goals = set()
    for r in range(ROWS):
        for c in range(COLS):
            if LEVEL_MAP[r][c] == 'G':
                goals.add((r, c))
    return goals

GOALS = find_goals()

def find_start_state():
    player = None
    boxes = set()

    for r in range(ROWS):
        for c in range(COLS):
            if LEVEL_MAP[r][c] == '@':
                player = (r, c)
            elif LEVEL_MAP[r][c] == '$':
                boxes.add((r, c))

    return (player, frozenset(boxes))

def is_wall(pos):
    r, c = pos
    return LEVEL_MAP[r][c] == '#'

def is_goal(boxes):
    return boxes == GOALS

def get_next_state(state, action):
    (pr, pc), boxes = state
    dr, dc = MOVES[action]

    new_player = (pr + dr, pc + dc)

    if is_wall(new_player):
        return None

    if new_player not in boxes:
        return (new_player, boxes)

    box_target = (new_player[0] + dr, new_player[1] + dc)

    if is_wall(box_target) or box_target in boxes:
        return None

    new_boxes = set(boxes)
    new_boxes.remove(new_player)
    new_boxes.add(box_target)

    return (new_player, frozenset(new_boxes))


def heuristic(boxes):
    h = 0
    for box in boxes:
        h += min(abs(box[0] - goal[0]) + abs(box[1] - goal[1]) for goal in GOALS)
    return h

def solve_sokoban_astar():
    start_state = find_start_state()

    pq = []
    heapq.heappush(pq, (heuristic(start_state[1]), 0, start_state, []))

    visited_cost = {start_state: 0}
    nodes_expanded = 0

    while pq:
        f, g, current_state, path = heapq.heappop(pq)
        nodes_expanded += 1

        if is_goal(current_state[1]):
            print("✔ Solution found using A*")
            print("✔ Path length:", len(path))
            print("✔ Nodes expanded:", nodes_expanded)
            return path

        for action in MOVES:
            next_state = get_next_state(current_state, action)

            if next_state:
                new_g = g + 1

                if next_state not in visited_cost or new_g < visited_cost[next_state]:
                    visited_cost[next_state] = new_g
                    new_f = new_g + heuristic(next_state[1])
                    heapq.heappush(
                        pq,
                        (new_f, new_g, next_state, path + [action])
                    )

    print("✘ No solution found")
    return None

print("\n--- A* Sokoban Solver ---\n")
solution = solve_sokoban_astar()

if solution:
    print("\nMovement Sequence:")
    print(" -> ".join(solution))
