import argparse
from pathlib import Path
from typing import List, Set, Tuple
import numpy as np

def part1(lines: List[str]) -> int:
    data = np.asarray([[int(x) for x in l] for l in lines])
    paths = np.zeros_like(data)
    row, col, direction = 0, 0,
    while (paths == 0).any():
        # test 3 options (straight, left, right)
        # save minimum
        # iterate
        pass

def part2(lines: List[str]) -> int:
    pass

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
