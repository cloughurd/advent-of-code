import argparse
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
import math
from pathlib import Path
from typing import Dict, List, Set, Tuple
import numpy as np
from datetime import datetime
import sys
from cachetools import LRUCache, cached
from cachetools.keys import hashkey


def part1(lines: List[str]) -> int:
    sys.setrecursionlimit(10000)
    lines = [x.strip() for x in lines]
    return run(lines, 0, 0, 'E')


def part2(lines: List[str]) -> int:
    sys.setrecursionlimit(10000)
    lines = [x.strip() for x in lines]
    num_lines = len(lines)
    num_cols = len(lines[0])
    max_locs = 0
    for i in range(num_lines):
        num_locs = run(lines, i, 0, 'E')
        if num_locs > max_locs:
            max_locs = num_locs
    for i in range(num_lines):
        num_locs = run(lines, i, num_cols-1, 'W')
        if num_locs > max_locs:
            max_locs = num_locs
    for i in range(num_cols):
        num_locs = run(lines, 0, i, 'S')
        if num_locs > max_locs:
            max_locs = num_locs
    for i in range(num_cols):
        num_locs = run(lines, num_lines-1, i, 'N')
        if num_locs > max_locs:
            max_locs = num_locs
    return max_locs

def run(lines: List[str], row: int, col: int, direction: str) -> int:
    memory = set()
    locations = {(row, col)}
    locations.update(move(lines, row, col, direction, locations, memory))
    return len(locations)

def move(lines: List[str], row: int, col: int, direction: str, locations: Set[Tuple[int, int]], memory: Set[Tuple[int, int, str]]) -> Set[Tuple[int, int]]:
    if row < 0 or row >= len(lines):
        return locations
    if col < 0 or col >= len(lines[0]):
        return locations
    if (row, col, direction) in memory:
        return locations
    memory.add((row, col, direction))
    locations.add((row, col))
    tile = lines[row][col]
    directions = get_directions(tile, direction)
    for d in directions:
        r, c = change_point(row, col, d)
        locations.update(move(lines, r, c, d, locations, memory))
    return locations

def change_point(row: int, col: int, direction: str) -> (int, int):
    if direction == 'N':
        return row-1, col
    if direction == 'E':
        return row, col+1
    if direction == 'S':
        return row+1, col
    if direction == 'W':
        return row, col-1
    else:
        raise ValueError(f'Direction "{direction}" is not recognized')

def get_directions(tile: str, direction: str) -> List[str]:
    if tile == '|' and direction in ['E', 'W']:
        return ['N', 'S']
    if tile == '-' and direction in ['N', 'S']:
        return ['E', 'W']
    slash_map = dict(
        N = 'E',
        E = 'N',
        S = 'W',
        W = 'S',
    )
    backslash_map = dict(
        N = 'W',
        E = 'S',
        S = 'E',
        W = 'N',
    )
    if tile == '/':
        return [slash_map[direction]]
    if tile == '\\':
        return [backslash_map[direction]]
    # otherwise, don't change directions
    return [direction]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('part', choices=[1, 2], default=1, type=int)
    parser.add_argument('-f', '--file', dest='filename', default='day16.txt')
    args = parser.parse_args()

    with open(Path(__file__).parent / 'inputs' / args.filename, 'r') as f:
        lines = f.readlines()

    if args.part == 2:
        print(part2(lines))
    else:
        print(part1(lines))
