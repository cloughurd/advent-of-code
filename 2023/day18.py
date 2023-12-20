import argparse
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Dict, List, Set, Tuple
import numpy as np
import importlib
import shared

DIR_MAP = {
    'U': 'N',
    'R': 'E',
    'D': 'S',
    'L': 'W',
}

def part1(lines: List[str]) -> int:
    row, col = 0, 0
    path = [(row, col)]
    for line in lines:
        direction, count, _ = line.split(maxsplit=2)
        direction = DIR_MAP[direction]
        for i in range(int(count)):
            row, col = shared.move_in_grid(row, col, direction)
            path.append((row, col))
    min_row = min(path, key=lambda x: x[0])[0]
    min_col = min(path, key=lambda x: x[1])[1]
    max_row = max(path, key=lambda x: x[0])[0]
    max_col = max(path, key=lambda x: x[1])[1]
    row_size = max_row - min_row + 1
    col_size = max_col - min_col + 1
    grid = np.zeros(shape=(row_size, col_size))
    for r, c in path:
        grid[r - min_row, c - min_col] = 1
    print(grid)
    print(path)
    np.savetxt('test.txt', grid, fmt='%i')
    return grid.sum()

def part2(lines: List[str]) -> int:
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('part', choices=[1, 2], default=1, type=int)
    parser.add_argument('-f', '--file', dest='filename', default='day18.txt')
    args = parser.parse_args()

    with open(Path(__file__).parent / 'inputs' / args.filename, 'r') as f:
        lines = f.readlines()

    if args.part == 2:
        print(part2(lines))
    else:
        print(part1(lines))
