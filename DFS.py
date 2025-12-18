LEVEL = [
    "#######",
    "#@.$.G#",
    "#.#.#.#",
    "#.$.G.#",
    "#######"
]

MOVES = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

ROWS = len(LEVEL)
COLS = len(LEVEL[0])


def find_initial_state():
    player = None
    boxes = set()
    goals = set()

    for r in range(ROWS):
        for c in range(COLS):
            if LEVEL[r][c] == '@':
                player = (r, c)
            elif LEVEL[r][c] == '$':
                boxes.add((r, c))
            elif LEVEL[r][c] == 'G':
                goals.add((r, c))

    return player, frozenset(boxes), goals


def is_wall(pos):
    r, c = pos
    return LEVEL[r][c] == '#'


def heuristic(boxes, goals):
    """
    Heuristic = sum of Manhattan distances
    from each box to the nearest goal
    """
    h = 0
    for box in boxes:
        h += min(abs(box[0] - g[0]) + abs(box[1] - g[1]) for g in goals)
    return h


def deadlock(box, goals):
    """
    Simple deadlock detection:
    if a box is stuck in a corner and not on a goal
    """
    if box in goals:
        return False

    r, c = box
    if (is_wall((r-1, c)) and is_wall((r, c-1))) or \
       (is_wall((r-1, c)) and is_wall((r, c+1))) or \
       (is_wall((r+1, c)) and is_wall((r, c-1))) or \
       (is_wall((r+1, c)) and is_wall((r, c+1))):
        return True

    return False


def solve_sokoban_creative(max_depth=50):

    player, boxes, goals = find_initial_state()
    start_state = (player, boxes)

    stack = [(start_state, [], 0)]
    visited = set()
    nodes_expanded = 0

    while stack:
        (p, b), path, depth = stack.pop()
        nodes_expanded += 1

        if b == goals:
            print("DFS Solution Found!")
            print("Moves:", " -> ".join(path))
            print("Path length:", len(path))
            print("Nodes expanded:", nodes_expanded)
            return path

        if depth >= max_depth or (p, b) in visited:
            continue

        visited.add((p, b))

        successors = []

        for move, (dr, dc) in MOVES.items():
            new_p = (p[0] + dr, p[1] + dc)

            if is_wall(new_p):
                continue

            new_boxes = set(b)

            if new_p in b:
                new_box = (new_p[0] + dr, new_p[1] + dc)

                if is_wall(new_box) or new_box in b:
                    continue

                if deadlock(new_box, goals):
                    continue

                new_boxes.remove(new_p)
                new_boxes.add(new_box)

            successor_state = (new_p, frozenset(new_boxes))
            score = heuristic(new_boxes, goals)

            successors.append((score, successor_state, move))

        # heuristic-guided ordering (best first, DFS style)
        successors.sort(key=lambda x: x[0], reverse=True)

        for _, next_state, move in successors:
            stack.append((next_state, path + [move], depth + 1))

    print("No solution found")
    print("Nodes expanded:", nodes_expanded)
    return None


solve_sokoban_creative()
