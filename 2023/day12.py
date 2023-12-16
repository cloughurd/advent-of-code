import argparse
from collections import defaultdict
from dataclasses import dataclass
import math
from pathlib import Path
from typing import Dict, List, Tuple


def part1(lines: List[str]) -> int:
    count = 0
    for line in lines:
        sl = SpringLine.from_str(line)
        count += sl.get_combination_count()

def part2(lines: List[str]) -> int:
    pass

@dataclass
class SpringLine:
    row: str
    groups: List[int]

    def get_combination_count(self) -> int:
        combination_count = 1
        pieces = [self.row]
        for g in self.groups:
            pieces = SpringLine._get_group_options(pieces, g)
            combination_count *= len(pieces)
        return combination_count

    @staticmethod
    def _get_group_options(row_pieces: List[str], num_in_group: int) -> List[str]:
        pass

    @classmethod
    def from_str(cls, line: str) -> "SpringLine":
        row, raw_groups = line.split(maxsplit=1)
        groups = [int(x) for x in raw_groups.split(',')]
        return cls(row, groups)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('part', choices=[1, 2], default=1, type=int)
    parser.add_argument('-f', '--file', dest='filename', default='day12.txt')
    args = parser.parse_args()

    with open(Path(__file__).parent / 'inputs' / args.filename, 'r') as f:
        lines = f.readlines()

    if args.part == 2:
        print(part2(lines))
    else:
        print(part1(lines))
