LEVEL = [
    "######",
    "#..G.#",
    "#.$..#",
    "#.@..#",
    "#....#",
    "######"
]
MOVES = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
ROWS = len(LEVEL)
COLS = len(LEVEL[0])

def find_start():
    player = None
    box = None
    goal = None
    for r in range(ROWS):
        for c in range(COLS):
            if LEVEL[r][c] == '@':
                player = (r, c)
            elif LEVEL[r][c] == '$':
                box = (r, c)
            elif LEVEL[r][c] == 'G':
                goal = (r, c)
    return player, box, goal

def is_wall(pos):
    r, c = pos
    return LEVEL[r][c] == '#'

def dfs(max_depth=50):
    player, box, goal = find_start()          
    start_state = (player, box)
    stack = [(start_state, [], 0)]        
    visited = set()                     
    nodes = 0                              

    while stack:
        (p, b), path, depth = stack.pop()
        nodes += 1

        if b == goal:
            print("There is a solution!")
            print("moves:", " -> ".join(path))
            print("Number of moves:", len(path))
            print("nodes:", nodes)
            return path

        if depth >= max_depth or (p, b) in visited:
            continue
        visited.add((p, b))

        for move, (dr, dc) in MOVES.items():
            new_p = (p[0]+dr, p[1]+dc)
            
            if is_wall(new_p):
                continue

            if new_p == b:
                new_b = (b[0]+dr, b[1]+dc)
                if is_wall(new_b):  
                    continue
                stack.append(((new_p, new_b), path+[move], depth+1))
            else:
                stack.append(((new_p, b), path+[move], depth+1))

    print("No solution ")
    return None 
dfs()