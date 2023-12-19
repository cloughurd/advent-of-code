import argparse
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Hashable, List, Set, Tuple
import numpy as np
import importlib
import shared

def part1(lines: List[str]) -> int:
    data = np.asarray([[int(x) for x in l.strip()] for l in lines])
    paths = np.zeros_like(data)
    paths[0, 0] = 1
    p = Point(0, 0, 'E', 0, 0)
    moves = set()
    while (paths == 0).any():
        new_moves = p.next_moves(data)
        for m in new_moves:
            moves.add(m)
        p = get_min_point(moves)
        moves.remove(p)
        if p.cost < paths[p.row, p.col]:
            paths[p.row, p.col] = p.cost
    print(paths)
    return paths[-1, -1]

def part2(lines: List[str]) -> int:
    pass

MOVES = dict(
            N = ['W', 'N', 'E'],
            E = ['N', 'E', 'S'],
            S = ['E', 'S', 'W'],
            W = ['S', 'W', 'N'],
        )


@dataclass
class Point:
    row: int
    col: int
    direction: str
    cost: int
    num_straight: int

    def next_moves(self, costs: np.ndarray) -> List['Point']:
        moves = []
        for d in MOVES[self.direction]:
            if d == self.direction:
                num_straight = self.num_straight + 1
            else:
                num_straight = 1
            if num_straight > 3:
                continue
            r, c = shared.move_in_grid(self.row, self.col, d)
            if r < 0 or c < 0:
                continue
            try:
                cost = costs[r, c] + self.cost
            except IndexError:
                continue
            moves.append(Point(r, c, d, cost, num_straight))
        return moves

    def __hash__(self) -> int:
        return hash((self.row, self.col, self.direction, self.cost, self.num_straight))

    def __eq__(self, __value: object) -> bool:
        if self.row != __value.row:
            return False
        if self.col != __value.col:
            return False
        if self.direction != __value.direction:
            return False
        if self.cost != __value.cost:
            return False
        if self.num_straight != __value.num_straight:
            return False

    @classmethod
    def dummy(cls) -> 'Point':
        return cls(-1, -1, '', float('inf'), -1)

def get_min_point(points: Dict[Tuple[int, int], Point]) -> Point:
    return sorted(list(points), key=lambda x: x.cost)[0]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('part', choices=[1, 2], default=1, type=int)
    parser.add_argument('-f', '--file', dest='filename', default='day17.txt')
    args = parser.parse_args()

    with open(Path(__file__).parent / 'inputs' / args.filename, 'r') as f:
        lines = f.readlines()

    if args.part == 2:
        print(part2(lines))
    else:
        print(part1(lines))
