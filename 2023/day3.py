from collections import defaultdict
from pathlib import Path
import sys
from typing import List

def run(part: int) -> int:
    with open(Path(__file__).parent / 'inputs' / 'day3.txt', 'r') as f:
        schematic = f.readlines()

    total_pn = 0
    current = ''
    is_part_num = False
    potential_gears = defaultdict(list)
    current_stars = set()
    for row, line in enumerate(schematic):
        for idx, char in enumerate(line):
            if char.isdigit():
                current += char
                symbol_found, star_points = is_point_adjacent_to_symbol(schematic, row, idx)
                is_part_num = is_part_num or symbol_found
                current_stars.update(star_points)
            # if not a digit, then check if we've been building up a number
            elif current != '':
                # if so, need to process whether that number was a part number or near gears
                if is_part_num:
                    total_pn += int(current)
                for star_point in current_stars:
                    potential_gears[star_point].append(int(current))
                current = ''
                is_part_num = False
                current_stars = set()
        # don't need to handle the case that we ended a line with a digit since a \n character ends each line

    gear_total = 0
    for num_list in potential_gears.values():
        if len(num_list) == 2:
            gear_total += num_list[0] * num_list[1]
    if part == 2:
        return gear_total

    return total_pn

def is_point_adjacent_to_symbol(schematic: List[str], row: int, idx: int) -> (bool, List[tuple]):
    star_points = []
    symbol_found = False
    for x in [row-1, row, row+1]:
        if x < 0 or x >= len(schematic):
            continue
        for y in [idx-1, idx, idx+1]:
            if y < 0 or y >= len(schematic[x]):
                continue
            val = schematic[x][y]
            if val not in '0123456789.\n':
                symbol_found = True
            if val == '*':
                star_points.append(f'{x}-{y}')
    return symbol_found, star_points



if __name__ == '__main__':
    if len(sys.argv) > 1:
        part = int(sys.argv[1])
    else:
        part = 1
    print(run(part))
