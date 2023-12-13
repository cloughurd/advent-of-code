import argparse
import numpy as np
from pathlib import Path
from typing import List


def part1(lines: List[str]) -> int:
    num_lines = len(lines)
    num_vals = len(lines[0].split())
    nums = np.zeros((num_lines, num_vals, num_vals), dtype=np.int32)
    for i, l in enumerate(lines):
        nums[i, 0, :] = [int(x) for x in l.split()]

    next_vals = np.zeros((num_lines))
    for i in range(num_vals-1):
        nums[:, i+1, :(num_vals-i-1)] = nums[:, i, 1:(num_vals-i)] - nums[:, i, 0:(num_vals-i-1)]
    for j in range(2, num_vals):
        nums[:, num_vals-j, j] = nums[:, num_vals-j, j-1] + nums[:, num_vals-j+1, j-1]
    # np.savetxt('test.txt', nums[0], fmt='%i')

    next_vals = nums[:, 0, -1] + nums[:, 1, -1]
    # np.savetxt('test2.txt', next_vals, fmt='%i')
    return next_vals.sum()

def part2(lines: List[str]) -> int:
    num_lines = len(lines)
    num_vals = len(lines[0].split())
    nums = np.zeros((num_lines, num_vals, num_vals), dtype=np.int32)
    for i, l in enumerate(lines):
        nums[i, 0, :] = [int(x) for x in l.split()]

    prev_vals = np.zeros((num_lines))
    for i in range(num_vals-1):
        nums[:, i+1, (i+1):] = nums[:, i, (i+1):] - nums[:, i, i:-1]
    for j in range(2, num_vals):
        nums[:, num_vals-j, num_vals-j-1] = nums[:, num_vals-j, num_vals-j] - nums[:, num_vals-j+1, num_vals-j]
    # np.savetxt('test.txt', nums[2], fmt='%i')

    prev_vals = nums[:, 0, 0] - nums[:, 1, 0]
    # np.savetxt('test2.txt', prev_vals, fmt='%i')
    return prev_vals.sum()

def form_diff_tree(nums: np.ndarray) -> np.ndarray:
    pass
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('part', choices=[1, 2], default=1, type=int)
    parser.add_argument('-f', '--file', dest='filename', default='day9.txt')
    args = parser.parse_args()

    with open(Path(__file__).parent / 'inputs' / args.filename, 'r') as f:
        lines = f.readlines()

    if args.part == 2:
        print(part2(lines))
    else:
        print(part1(lines))
