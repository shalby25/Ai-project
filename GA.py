import random
import copy
import time

LEVEL_MAP = [
    "#######",
    "#@.$ G#",
    "#.#.#.#",
    "#.$ G #",
    "#######"
]
ROWS = len(LEVEL_MAP)
COLS = len(LEVEL_MAP[0])

WALL = '#'
PLAYER = 'P'
BOX = 'B'
GOAL = 'G'
EMPTY = ' '
MOVES = ['U', 'D', 'L', 'R']

MOVE_NAMES = {
    'U': 'Up',
    'D': 'Down',
    'L': 'Left',
    'R': 'Right'
}

initial_map = [] # CONVERT MAP
GOALS = []

for r in range(ROWS):
    row = []
    for c in range(COLS):
        char = LEVEL_MAP[r][c]

        if char == '#':
            row.append('#')
        elif char == '@':
            row.append('P')
        elif char == '$':
            row.append('B')
        elif char == 'G':
            row.append('G')
            GOALS.append((r, c))
        else:
            row.append(' ')
    initial_map.append(row)

def print_grid(grid):
    for row in grid:
        print("".join(row))
    print()

def find_positions(grid, symbol):
    return [(i, j)
            for i in range(len(grid))
            for j in range(len(grid[0]))
            if grid[i][j] == symbol]

def distance_on_grid(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def apply_move(grid, move):
    grid = copy.deepcopy(grid)
    px, py = find_positions(grid, PLAYER)[0]
    dx, dy = 0, 0
    
    if move == 'U': dx = -1
    if move == 'D': dx = 1
    if move == 'L': dy = -1
    if move == 'R': dy = 1

    nx, ny = px + dx, py + dy

    if grid[nx][ny] == WALL:
        return grid

    if grid[nx][ny] == BOX:
        bx, by = nx + dx, ny + dy
        if grid[bx][by] in [WALL, BOX]:
            return grid
        grid[bx][by] = BOX

    grid[px][py] = EMPTY
    grid[nx][ny] = PLAYER
    return grid

def is_win(grid):
    boxes = find_positions(grid, BOX)
    return all(box in GOALS for box in boxes)

def apply_solution(grid, chromosome):
    grid = copy.deepcopy(grid)
    for move in chromosome:
        grid = apply_move(grid, move)
    return grid

# FITNESS FUNCTION
def fitness(original_grid, chromosome):
    grid = copy.deepcopy(original_grid)
    steps_used = 0

    for move in chromosome:
        new_grid = apply_move(grid, move)
        if new_grid != grid:
            steps_used += 1
        grid = new_grid
        
        if is_win(grid):
            break

    boxes = find_positions(grid, BOX)
    boxes_on_goals = sum(1 for box in boxes if box in GOALS)

    distance_score = 0
    for box in boxes:
        distances = [distance_on_grid(box, g) for g in GOALS]
        distance_score += min(distances)

    fitness_value = (
        boxes_on_goals * 100 - distance_score * 5 - steps_used
    )
    return fitness_value

def genetic_algorithm():
    POP_SIZE = 80
    MIN_CHROM_LEN = 10
    MAX_CHROM_LEN = 50
    GENERATIONS = 300

    population = [
        [random.choice(MOVES) for _ in range(random.randint(MIN_CHROM_LEN, MAX_CHROM_LEN))]
        for _ in range(POP_SIZE)
    ]

    best_solution = None
    best_fitness = float('-inf')

    for _ in range(GENERATIONS):
        population.sort(
            key=lambda c: fitness(initial_map, c),
            reverse=True
        )

        current_fitness = fitness(initial_map, population[0])

        if current_fitness > best_fitness:
            best_fitness = current_fitness
            best_solution = population[0]

        if is_win(apply_solution(initial_map, population[0])):
            break

        new_population = population[:10]

        # Crossover
        while len(new_population) < POP_SIZE:
            p1 = random.choice(population[:20])
            p2 = random.choice(population[:20])

            cut = random.randint(1, min(len(p1), len(p2)) - 1)
            child = p1[:cut] + p2[cut:]

        # Mutation
            if random.random() < 0.15:
                idx = random.randint(0, len(child) - 1)
                child[idx] = random.choice(MOVES)

            if random.random() < 0.2:
                if random.random() < 0.5 and len(child) > MIN_CHROM_LEN:
                    child.pop()
                elif len(child) < MAX_CHROM_LEN:
                    child.append(random.choice(MOVES))

            new_population.append(child)
        population = new_population
    return best_solution, best_fitness

print("... Starting Genetic Algorithm search ...")

solution, best_fitness = genetic_algorithm()
grid = copy.deepcopy(initial_map)

print("\nInitial State:")
print_grid(grid)

for move in solution:
    grid = apply_move(grid, move)
    print(f"Move: {move}")
    print_grid(grid)
    time.sleep(0.3)

    if is_win(grid):
        print("YOU WIN!\n")
        break

print("Solution found.")
print(f"Moves Count: {len(solution)}")
print(f"Best Fitness: {best_fitness}")
print("\nSolution Move Sequence:")
print(" -> ".join(MOVE_NAMES[m] for m in solution))
