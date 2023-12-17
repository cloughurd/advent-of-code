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
    return run(lines, False)

def part2(lines: List[str]) -> int:
    return run(lines, True)

def run(lines: List[str], allow_smudge: bool) -> int:
    subset = []
    count_vertical = 0
    count_horizontal = 0
    for i, line in enumerate(lines):
        if line == '\n' or i == len(lines)-1:
            p = Pattern.from_lines(subset)
            if allow_smudge:
                row, col = p.smudge_point
            else:
                row, col = p.mirror_point
            if row != -1:
                count_horizontal += row
            else:
                count_vertical += col
            subset = []
        else:
            subset.append(line)
    return (count_horizontal * 100) + count_vertical

@dataclass
class Pattern:
    data: np.ndarray

    @property
    def smudge_point(self) -> (int, int):
        for i in range(1, self.data.shape[0]):
            dist = min(i, self.data.shape[0]-i)
            if np.abs(self.data[i-dist:i, :] - np.flip(self.data[i:i+dist, :], axis=0)).sum() == 1:
                return i, -1
        for i in range(1, self.data.shape[1]):
            dist = min(i, self.data.shape[1]-i)
            if np.abs(self.data[:, i-dist:i] - np.flip(self.data[:, i:i+dist], axis=1)).sum() == 1:
                return -1, i

    @property
    def mirror_point(self) -> (int, int):
        for i in range(1, self.data.shape[0]):
            dist = min(i, self.data.shape[0]-i)
            if (self.data[i-dist:i, :] == np.flip(self.data[i:i+dist, :], axis=0)).all():
                return i, -1
        for i in range(1, self.data.shape[1]):
            dist = min(i, self.data.shape[1]-i)
            if (self.data[:, i-dist:i] == np.flip(self.data[:, i:i+dist], axis=1)).all():
                return -1, i

    @classmethod
    def from_lines(cls, lines: List[str]) -> 'Pattern':
        num_lines = []
        for line in lines:
            num_lines.append([1 if c == '#' else 0 for c in line.strip()])
        return cls(np.asarray(num_lines))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('part', choices=[1, 2], default=1, type=int)
    parser.add_argument('-f', '--file', dest='filename', default='day13.txt')
    args = parser.parse_args()

    with open(Path(__file__).parent / 'inputs' / args.filename, 'r') as f:
        lines = f.readlines()

    if args.part == 2:
        print(part2(lines))
    else:
        print(part1(lines))
