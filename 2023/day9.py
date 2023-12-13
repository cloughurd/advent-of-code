import argparse
import numpy as np
from pathlib import Path
from typing import List


def part1(lines: List[str]) -> int:
    nums = init_array(lines)
    nums = form_diff_tree(nums, True)
    nums = backfill_change(nums, True)
    # Calculate predictions by adding final value and one above it
    # Sum up predictions
    return np.sum(nums[:, 0, -1] + nums[:, 1, -1])

def part2(lines: List[str]) -> int:
    nums = init_array(lines)
    nums = form_diff_tree(nums, False)
    nums = backfill_change(nums, False)
    # Calculate predictions by subtracting value above from the original start number
    # Sum up predictions
    return np.sum(nums[:, 0, 0] - nums[:, 1, 0])

def init_array(lines: List[str]) -> np.ndarray:
    num_lines = len(lines)
    num_vals = len(lines[0].split())
    nums = np.zeros((num_lines, num_vals, num_vals), dtype=np.int32)
    for i, l in enumerate(lines):
        nums[i, 0, :] = [int(x) for x in l.split()]
    return nums

def form_diff_tree(nums: np.ndarray, fill_left: bool) -> np.ndarray:
    '''
    Given a 3d array where each 2d array looks like this:
        1 2 3
        0 0 0
        0 0 0
    will fill with differences between the numbers above.
    If fill_left is True, each row will be right-padded with 0s in a pyramid like this:
        1 2 3
        1 1 0
        0 0 0
    Otherwise, each row will be left-padded with 0s instead.
    '''
    num_vals = nums.shape[1]
    for i in range(1, num_vals):
        width = num_vals - i
        if fill_left:
            start_idx = 0
            save_idx = start_idx
        else:
            start_idx = i - 1
            save_idx = i
        nums[:, i, save_idx:save_idx+width] = nums[:, i-1, (start_idx+1):(start_idx+1+width)] - nums[:, i-1, start_idx:(start_idx+width)]
    return nums

def backfill_change(nums: np.ndarray, filled_left: bool) -> np.ndarray:
    '''
    Given a 3d array where each 2d array looks like this (filled_left=True on left):
        1 2 3    or     1 2 3
        1 1 0           0 1 1
        0 0 0           0 0 0
    will fill first 0 per row with change from adjacent inward and diagonal.
        1 2 3    or     1 2 3
        1 1 1*         *1 1 1
        0 0 0           0 0 0
    On left, 1 (1, 1) + 0 (2, 1) = 1
    On right, 1 (1, 1) - 0 (2, 1) = 1
    '''
    num_vals = nums.shape[1]
    for i in range(2, num_vals):
        # set_idx is moving away from the starting side, which is left when filled_left and right otherwise
        # read_idx is back towards the starting side,
        if filled_left:
            set_idx = i
            read_idx = set_idx - 1
        else:
            set_idx = num_vals - i - 1
            read_idx = set_idx + 1
        # in either direction, you move from the bottom row up
        same_row = nums[:, num_vals - i, read_idx]
        prev_row = nums[:, num_vals-i+1, read_idx]
        if filled_left:
            change = same_row + prev_row
        else:
            change = same_row - prev_row
        nums[:, num_vals-i, set_idx] = change
    return nums

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
