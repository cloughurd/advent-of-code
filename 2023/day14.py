import argparse
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
import math
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
from datetime import datetime


def part1(lines: List[str]) -> int:
    columns = [Column() for x in range(len(lines[0]))]
    for row, line in enumerate(lines):
        for col, character in enumerate(line):
            if character == '#':
                columns[col].add_cube(row)
            if character == 'O':
                columns[col].add_rock()
    weights = [c.calc_weight(len(lines)) for c in columns]
    return sum(weights)


def part2(lines: List[str]) -> int:
    pass

class Column:
    def __init__(self) -> None:
        self.last_cube: int = -1
        self.buildups: Dict[int, int] = defaultdict(lambda: 0)

    def add_cube(self, i: int):
        self.last_cube = i

    def add_rock(self):
        self.buildups[self.last_cube] += 1

    def calc_weight(self, length: int) -> int:
        weight = 0
        for cube in self.buildups:
            for r in range(self.buildups[cube]):
                weight += length - cube - r - 1
        return weight

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('part', choices=[1, 2], default=1, type=int)
    parser.add_argument('-f', '--file', dest='filename', default='day14.txt')
    args = parser.parse_args()

    with open(Path(__file__).parent / 'inputs' / args.filename, 'r') as f:
        lines = f.readlines()

    if args.part == 2:
        print(part2(lines))
    else:
        print(part1(lines))
