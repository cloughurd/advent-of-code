import argparse
from collections import defaultdict
from dataclasses import dataclass
import math
from pathlib import Path
from typing import Dict, List, Tuple


def part1(lines: List[str]) -> int:
    sm = SpaceMap.parse_spacemap(lines, 1)
    adj_map = sm.build_adj_map()
    return sum(adj_map.values()) / 2

def part2(lines: List[str]) -> int:
    sm = SpaceMap.parse_spacemap(lines, 1000000-1)
    adj_map = sm.build_adj_map()
    return sum(adj_map.values()) / 2

@dataclass
class Galaxy:
    row: int
    col: int

    def shortest_path(self, other: "Galaxy", open_rows: List[int], open_cols: List[int], multiplier: int) -> int:
        row_diff = abs(self.row - other.row) + (sum(open_rows[min(self.row, other.row):max(self.row, other.row)]) * multiplier)
        col_diff = abs(self.col - other.col) + (sum(open_cols[min(self.col, other.col):max(self.col, other.col)]) * multiplier)
        return row_diff + col_diff

@dataclass
class SpaceMap:
    open_rows: List[int]
    open_cols: List[int]
    galaxies: List[Galaxy]
    distance_multiplier: int

    def build_adj_map(self) -> Dict[Tuple[int, int], int]:
        distances = {}
        for i, g in enumerate(self.galaxies):
            for j in range(i, len(self.galaxies)):
                dist = g.shortest_path(self.galaxies[j], self.open_rows, self.open_cols, self.distance_multiplier)
                distances[(i, j)] = dist
                distances[(j, i)] = dist
        return distances

    @classmethod
    def parse_spacemap(cls, lines: List[str], multiplier: int) -> "SpaceMap":
        galaxies = []
        open_rows = [1 for x in range(len(lines[0]))]
        open_cols = [1 for x in range(len(lines))]
        for r, line in enumerate(lines):
            c = -1
            while (c := line.find('#', c+1)) != -1:
                open_rows[r] = 0
                open_cols[c] = 0
                galaxies.append(Galaxy(r, c))
        return cls(open_rows, open_cols, galaxies, multiplier)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('part', choices=[1, 2], default=1, type=int)
    parser.add_argument('-f', '--file', dest='filename', default='day11.txt')
    args = parser.parse_args()

    with open(Path(__file__).parent / 'inputs' / args.filename, 'r') as f:
        lines = f.readlines()

    if args.part == 2:
        print(part2(lines))
    else:
        print(part1(lines))
