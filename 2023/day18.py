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
    sys.setrecursionlimit(10000)
    path = get_path(lines)
    grid = form_array(path)
    print(grid.size)
    fill_outside(grid, 2)
    np.savetxt('test.txt', grid, fmt='%i')
    return grid.size - (grid == 2).sum()

def part2(lines: List[str]) -> int:
    pass

def get_path(lines: List[str]) -> List[Tuple[int, int]]:
    row, col = 0, 0
    path = [(row, col)]
    for line in lines:
        direction, count, _ = line.split(maxsplit=2)
        direction = DIR_MAP[direction]
        for i in range(int(count)):
            row, col = shared.move_in_grid(row, col, direction)
            path.append((row, col))
    return path

def form_array(path: List[Tuple[int, int]]) -> np.ndarray:
    min_row = min(path, key=lambda x: x[0])[0]
    min_col = min(path, key=lambda x: x[1])[1]
    max_row = max(path, key=lambda x: x[0])[0]
    max_col = max(path, key=lambda x: x[1])[1]
    row_size = max_row - min_row + 1
    col_size = max_col - min_col + 1
    grid = np.zeros(shape=(row_size, col_size), dtype='int8')
    for r, c in path:
        grid[r - min_row, c - min_col] = 1
    return grid

def fill_outside(grid: np.ndarray, fill_val: int):
    # start from top left and fill down
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] != 0:
                continue
            fill = False
            if x == 0:
                fill = True
            elif y == 0:
                fill = True
            elif x == grid.shape[0]-1:
                fill = True
            elif y == grid.shape[1]-1:
                fill = True
            elif (grid[x-1:x+1, y-1:y+1] == fill_val).any():
                fill = True

            if fill:
                grid[x, y] = fill_val
    # restart from bottom right to fill gaps
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            x = grid.shape[0]-1-x
            y = grid.shape[1]-1-y
            if grid[x, y] != 0:
                continue
            fill = False
            if x == 0:
                fill = True
            elif y == 0:
                fill = True
            elif x == grid.shape[0]-1:
                fill = True
            elif y == grid.shape[1]-1:
                fill = True
            elif (grid[x-1:x+1, y-1:y+1] == fill_val).any():
                fill = True

            if fill:
                grid[x, y] = fill_val
            # if x == 0 and grid[x, y] == 0:
            #     grid
            # if grid[i, 0] == 0:
            #     grid[i, 0] = fill_val
    # for i in range(grid.shape[0]):
    #     if grid[i, 0] == 0:
    #         grid[i, 0] = fill_val
    #         spread_fill(grid, i, 0, fill_val)
    #     if grid[i, grid.shape[1]-1] == 0:
    #         grid[i, grid.shape[1]-1] = fill_val
    #         spread_fill(grid, i, grid.shape[1]-1, fill_val)
    # for i in range(grid.shape[1]):
    #     if grid[0, i] == 0:
    #         grid[0, i] = fill_val
    #         spread_fill(grid, 0, i, fill_val)
    #     if grid[grid.shape[0]-1, i] == 0:
    #         grid[grid.shape[0]-1, i] = fill_val
    #         spread_fill(grid, grid.shape[0]-1, i, fill_val)

def spread_fill(grid: np.ndarray, x: int, y: int, fill_val: int):
    marked = []
    for r, c in [(x, y-1), (x+1, y), (x, y+1), (x-1, y), (x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]:
        if r < 0 or c < 0:
            continue
        try:
            if grid[r, c] != 0:
                continue
        except IndexError:
            continue
        grid[r, c] = fill_val
        marked.append((r, c))
    for r, c in marked:
        spread_fill(grid, r, c, fill_val)

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
