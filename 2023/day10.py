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
    2. Convert non-path to .
    '''
    path = get_path(lines)
    count = 0
    for r in range(len(lines)):
        pass

def get_path(lines: List[str]) -> List[Tuple[int, int]]:
    row, col = find_start(lines)
    r, c, d = first_step(lines, row, col)
    path = [(r, c)]
    while (r, c) != (row, col):
        r, c, d = next_step(lines, r, c, d)
        path.append((r, c))
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

def first_step(lines: List[str], row: int, col: int) -> (int, int, str):
    for r, c, d in [_go_north(row, col), _go_east(row, col), _go_south(row, col), _go_west(row, col)]:
        if r < 0 or c < 0:
            continue
        if r >= len(lines) or c >= len(lines):
            continue
        pipe = lines[r][c]
        if pipe in PIPE_MAP[d]:
            return r, c, d
    raise ValueError(f'Could not find valid pipe from starting point ({row}, {col})')

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
