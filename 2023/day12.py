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
    return sum(run(lines, 1))

def part2(lines: List[str]) -> int:
    counts_1 = np.asarray(run(lines, 1))
    counts_2 = np.asarray(run(lines, 2, True))
    mult = counts_2 / counts_1
    return np.sum(counts_1 * (mult ** 4))

def run(lines: List[str], repeater: int, verbose: bool = False) -> int:
    #new_lines = []
    counts = []
    for i, line in enumerate(lines):
        # print('\n\n' + line)
        sl = SpringLine.from_str(line, repeater)
        line_count = sl.get_combination_count()
        # count += line_count
        counts.append(line_count)
        if verbose and i % 5 == 0:
            print(i, line_count, datetime.now())
        # new_lines.append(str(line_count) + '-- ' + line)
    #     if count > 30:
    #         break
    # with open('test.txt', 'w') as f:
    #     f.writelines(new_lines)
    return counts

@dataclass
class SpringLine:
    row: str
    groups: List[int]

    def get_combination_count(self) -> int:
        count = 0
        self._prune_unknowns()
        for potential in self._get_group_options():
            if self._check_valid(potential):
                # print(potential)
                count += 1
        return count

    def _prune_unknowns(self):
        self.row = SpringLine._prune_around_full_groups(self.row, max(self.groups))
        self.row = SpringLine._prune_small_groups(self.row, min(self.groups))
        self.row = SpringLine._prune_edges(self.row, self.groups[0], self.groups[-1])

    @staticmethod
    def _prune_around_full_groups(row: str, max_group: int) -> str:
        i = -1
        while (i := row.find('#'*max_group, i+1)) != -1:
            if i > 0 and row[i-1] == '?':
                row = SpringLine._remove_unknown(row, i-1, '.')
            i = i + max_group
            if i < len(row) and row[i] == '?':
                row = SpringLine._remove_unknown(row, i, '.')
        return row

    @staticmethod
    def _prune_small_groups(row: str, min_group: int) -> str:
        for i in range(1, min_group):
            if row.startswith(('?'*i) + '.'):
                for j in range(i):
                    row = SpringLine._remove_unknown(row, j, '.')
            if row.endswith('.' + ('?'*i)):
                for j in range(i):
                    row = SpringLine._remove_unknown(row, len(row)-j-1, '.')
            row = row.replace('.' + ('?'*i) + '.', '.'*(i+2))
        return row

    @staticmethod
    def _prune_edges(row: str, first_group: int, last_group: int) -> str:
        if row.startswith('?' + ('#'*first_group)):
            row = SpringLine._remove_unknown(row, 0, '.')
        if row.endswith(('#'*last_group) + '?'):
            row = SpringLine._remove_unknown(row, len(row)-1, '.')
        return row

    @staticmethod
    def _remove_unknown(s: str, i: int, replace_with: str) -> str:
        return s[:i] + replace_with + s[i+1:]

    def _check_valid(self, row: str) -> bool:
        groupings = [x for x in row.split('.') if x != '']
        if len(groupings) != len(self.groups):
            return False
        for i in range(len(groupings)):
            if len(groupings[i]) != self.groups[i]:
                return False
        return True

    def _get_group_options(self) -> str:
        num_known_springs = self.row.count('#')
        num_total_springs = sum(self.groups)
        if num_known_springs < num_total_springs:
            unknowns = [i for i, c in enumerate(self.row) if c == '?']
            for potential in combinations(unknowns, num_total_springs-num_known_springs):
                yield SpringLine._replace_unknowns(self.row, potential)
        else:
            yield SpringLine._replace_unknowns(self.row, [])

    @staticmethod
    def _replace_unknowns(row: str, extra_springs: List[int]) -> str:
        for i in extra_springs:
            row = SpringLine._remove_unknown(row, i, '#')
        return row.replace('?', '.')

    @classmethod
    def from_str(cls, line: str, repeater: int) -> "SpringLine":
        row, raw_groups = line.split(maxsplit=1)
        row = SpringLine._repeat_str(row, repeater, '?')
        raw_groups = SpringLine._repeat_str(raw_groups, repeater, ',')
        groups = [int(x) for x in raw_groups.split(',')]
        return cls(row, groups)

    @staticmethod
    def _repeat_str(s: str, n: int, delim: str) -> str:
        new_s = (s + delim) * (n-1)
        return new_s + s


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
