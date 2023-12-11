import numpy as np
from pathlib import Path
import sys
from typing import List


def run(part: int) -> int:
    with open(Path(__file__).parent / 'inputs' / 'day8.txt', 'r') as f:
        directions = f.readlines()
    turns = directions[0].strip()

    nodes = directions[2:]
    node_map = {}
    a_nodes = []
    for n in nodes:
        start = n[0:3]
        left = n[7:10]
        right = n[12:15]

        node_map[start] = (left, right)
        if start.endswith('A'):
            a_nodes.append(start)

    if part == 2:
        node_list = a_nodes
    else:
        node_list = ['AAA']
    turn_count = 0
    z_idx = [-1] * len(node_list)
    while not done(node_list, part):
        turn = turns[turn_count % len(turns)]
        for node_idx, node in enumerate(node_list):
            choices = node_map[node]
            if turn == 'L':
                node = choices[0]
            if turn == 'R':
                node = choices[1]
            node_list[node_idx] = node
            if node.endswith('Z'):
                z_idx[node_idx] = turn_count + 1
        turn_count += 1
        if -1 not in z_idx:
            break
    if not done(node_list, part):
        return np.lcm.reduce(np.asarray(z_idx, dtype=np.int64))
    return turn_count

def done(node_list: List[str], part: int) -> bool:
    if part == 2:
        return all([x.endswith('Z') for x in node_list])
    return node_list[0] == 'ZZZ'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        part = int(sys.argv[1])
    else:
        part = 1
    print(run(part))
