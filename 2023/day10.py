import argparse
import math
from pathlib import Path
from typing import List, Tuple

NORTH = {
    '|': 'N',
    '7': 'W',
    'F': 'E',
}
EAST = {
    '-': 'E',
    '7': 'S',
    'J': 'N',
}
SOUTH = {
    '|': 'S',
    'J': 'W',
    'L': 'E',
}
WEST = {
    '-': 'W',
    'L': 'N',
    'F': 'S',
}
PIPE_MAP = dict(
    N = NORTH,
    E = EAST,
    S = SOUTH,
    W = WEST,
)

def part1(lines: List[str]) -> int:
    path = get_path(lines)
    return math.ceil(len(path) / 2)

def part2(lines: List[str]) -> int:
    '''
    1. Get path
    2. Replace S with pipe
    3. For each row:
        Step through, tracking how many times the path cross the row
        Any non-path space with an odd number of path crosses is on the interior
    '''
    path = get_path(lines)
    start = path[0]
    start_candidate_dirs = [x[2] for x in first_step(lines, *start)]
    start_pipe = get_start_pipe(start_candidate_dirs)
    lines[start[0]] = lines[start[0]].replace('S', start_pipe)
    count = 0
    for row, line in enumerate(lines):
        count += count_internal(line, row, path)
    return count

def count_internal(line: str, row: int, path: List[Tuple[int, int]]) -> int:
    cross_pairs = {
        'L': '7',
        'F': 'J',
    }
    cross_count = 0
    internal_count = 0
    prev_bend = ''
    for col, char in enumerate(line):
        if (row, col) in path:
            if char == '|':
                cross_count += 1
            elif char in cross_pairs:
                prev_bend = char
            elif char in cross_pairs.values():
                if char == cross_pairs[prev_bend]:
                    cross_count += 1
                prev_bend = ''
        else:
            if cross_count % 2 == 1:
                internal_count += 1
    return internal_count


def get_start_pipe(start_dirs: List[str]):
    pipe_options = []
    for d in start_dirs:
        pipes = set()
        for pm in PIPE_MAP.values():
            for pipe, out_dir in pm.items():
                if d == out_dir:
                    pipes.add(pipe)
        pipe_options.append(pipes)
    # get single value out of intersection set
    (single_pipe,) = pipe_options[0].intersection(pipe_options[1])
    return single_pipe

def get_path(lines: List[str]) -> List[Tuple[int, int]]:
    row, col = find_start(lines)
    path = [(row, col)]
    r, c, d = first_step(lines, row, col)[0]
    while (r, c) != (row, col):
        path.append((r, c))
        r, c, d = next_step(lines, r, c, d)
    return path

def next_step(lines: List[str], row:int, col: int, prev_dir: str) -> (int, int, str):
    pipe = lines[row][col]
    new_dir = PIPE_MAP[prev_dir][pipe]
    steps = dict(
        N=_go_north,
        E=_go_east,
        S=_go_south,
        W=_go_west,
    )
    return steps[new_dir](row, col)

def first_step(lines: List[str], row: int, col: int) -> List[Tuple[int, int, str]]:
    candidates = []
    for r, c, d in [_go_north(row, col), _go_east(row, col), _go_south(row, col), _go_west(row, col)]:
        if r < 0 or c < 0:
            continue
        if r >= len(lines) or c >= len(lines):
            continue
        pipe = lines[r][c]
        if pipe in PIPE_MAP[d]:
            candidates.append((r, c, d))
    if len(candidates) != 2:
        raise ValueError(f'Could not start from starting point ({row}, {col})')
    return candidates

def find_start(lines: List[str]) -> (int, int):
    row = 0
    col = -1
    while True:
        col = lines[row].find('S')
        if col != -1:
            break
        row += 1
    return row, col

def _go_north(row: int, col: int) -> (int, int, str):
    return row-1, col, 'N'

def _go_east(row: int, col: int) -> (int, int, str):
    return row, col+1, 'E'

def _go_south(row: int, col: int) -> (int, int, str):
    return row+1, col, 'S'

def _go_west(row: int, col: int) -> (int, int, str):
    return row, col-1, 'W'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('part', choices=[1, 2], default=1, type=int)
    parser.add_argument('-f', '--file', dest='filename', default='day10.txt')
    args = parser.parse_args()

    with open(Path(__file__).parent / 'inputs' / args.filename, 'r') as f:
        lines = f.readlines()

    if args.part == 2:
        print(part2(lines))
    else:
        print(part1(lines))
