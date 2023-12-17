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
    line = lines[0].strip()
    total = 0
    for step in line.split(','):
        current_value = 0
        for c in step:
            current_value = hash(current_value, c)
        total += current_value
    return total

def part2(lines: List[str]) -> int:
    pass

def hash(current_value: int, new_char: str) -> int:
    current_value += ord(new_char)
    current_value *= 17
    current_value %= 256
    return current_value

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('part', choices=[1, 2], default=1, type=int)
    parser.add_argument('-f', '--file', dest='filename', default='day15.txt')
    args = parser.parse_args()

    with open(Path(__file__).parent / 'inputs' / args.filename, 'r') as f:
        lines = f.readlines()

    if args.part == 2:
        print(part2(lines))
    else:
        print(part1(lines))
